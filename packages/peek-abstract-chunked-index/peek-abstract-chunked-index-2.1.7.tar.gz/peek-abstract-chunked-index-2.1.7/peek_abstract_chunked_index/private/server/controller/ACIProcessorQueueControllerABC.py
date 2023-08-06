from abc import ABCMeta, abstractmethod
from collections import deque, namedtuple
from datetime import datetime
from logging import Logger
from typing import List, Deque, Callable

import pytz
from peek_abstract_chunked_index.private.server.controller.ACIProcessorStatusNotifierABC import \
    ACIProcessorStatusNotifierABC
from peek_abstract_chunked_index.private.tuples.ACIProcessorQueueTupleABC import \
    ACIProcessorQueueTupleABC
from sqlalchemy import asc, select, bindparam
from twisted.internet import task, reactor, defer
from twisted.internet.defer import inlineCallbacks, Deferred
from vortex.DeferUtil import deferToThreadWrapWithLogger, vortexLogFailure

ACIProcessorQueueBlockItem = namedtuple("ACIProcessorQueueBlockItem",
                                        ("queueIds", "items", "itemUniqueIds"))


class ACIProcessorQueueControllerABC(metaclass=ABCMeta):
    """ Chunked Index Processor - Queue Controller

    Process the database queue and send chunks of data to the workers
    to process.

    1) Query for queue
    2) Process queue
    3) Delete from queue

    Example code :

        _logger = logger
        _QueueTableDeclarative = LiveDbRawValueQueueTuple

    """

    QUEUE_ITEMS_PER_TASK: int = None  # Example 500
    POLL_PERIOD_SECONDS: float = None  # Example 0.200

    QUEUE_BLOCKS_MAX: int = None  # Example 40
    QUEUE_BLOCKS_MIN: int = None  # Example 8

    WORKER_TASK_TIMEOUT: int = None  # Example 60

    DEDUPE_LOOK_AHEAD_MIN_ROWS = 100000
    DEDUPE_PERIOD_SECONDS: float = 10.0

    _logger: Logger = None
    _QueueDeclarative: ACIProcessorQueueTupleABC = None

    def __init__(self, ormSessionCreator,
                 processorStatusNotifier: ACIProcessorStatusNotifierABC,
                 isProcessorEnabledCallable: Callable = None):
        self._dbSessionCreator = ormSessionCreator
        self._processorStatusNotifier: ACIProcessorStatusNotifierABC = processorStatusNotifier
        self._isProcessorEnabledCallable = isProcessorEnabledCallable

        self._pollLoopingCall = task.LoopingCall(self._poll)
        self._lastDedupeTime = datetime.now(pytz.utc)
        self._queueCount = 0

        self._queueIdsInBuffer = set()
        self._chunksInProgress = set()
        self._lastFetchedId = None

        self._pausedForDuplicate = None
        self._fetchedBlockBuffer: Deque[ACIProcessorQueueBlockItem] = deque()

        assert self.QUEUE_ITEMS_PER_TASK, "ACI, QUEUE_ITEMS_PER_TASK is missing"
        assert self.POLL_PERIOD_SECONDS, "ACI, POLL_PERIOD_SECONDS is missing"
        assert self.QUEUE_BLOCKS_MAX, "ACI, QUEUE_BLOCKS_MAX is missing"
        assert self.QUEUE_BLOCKS_MIN is not None, "ACI, QUEUE_BLOCKS_MIN is missing"
        assert self.WORKER_TASK_TIMEOUT, "ACI, WORKER_TASK_TIMEOUT is missing"
        assert self._logger, "ACI, _logger is missing"
        assert self._QueueDeclarative, "ACI, _QueueDeclarative is missing"

    def isBusy(self) -> bool:
        return self._queueCount != 0

    def start(self):
        self._processorStatusNotifier.setProcessorStatus(True, self._queueCount)
        d = self._pollLoopingCall.start(self.POLL_PERIOD_SECONDS, now=False)
        d.addCallbacks(self._timerCallback, self._timerErrback)

    def _timerErrback(self, failure):
        vortexLogFailure(failure, self._logger)
        self._processorStatusNotifier.setProcessorStatus(False, self._queueCount)
        self._processorStatusNotifier.setProcessorError(str(failure.value))

    def _timerCallback(self, _):
        self._processorStatusNotifier.setProcessorStatus(False, self._queueCount)

    def stop(self):
        if self._pollLoopingCall.running:
            self._pollLoopingCall.stop()

    def shutdown(self):
        self.stop()

    @inlineCallbacks
    def _poll(self):
        # If the Queue processor is paused, then do nothing.
        if self._pausedForDuplicate:
            return

        # If we have a callable that can suspend this processor, then check it.
        if self._isProcessorEnabledCallable and not self._isProcessorEnabledCallable():
            return

        # We queue the grids in bursts, reducing the work we have to do.
        if self._queueCount > self.QUEUE_BLOCKS_MIN:
            return

        fetchedBlocks = yield self._fetchBlocks()
        # Queue the next blocks
        self._fetchedBlockBuffer.extend(fetchedBlocks)

        # If we have nothing to do, exit now
        if not self._fetchedBlockBuffer:
            return

        # Process the block buffer
        while self._fetchedBlockBuffer:
            # Look at the next block to process
            block = self._fetchedBlockBuffer[0]

            # If we're already processing these chunks, then return and try later
            if self._chunksInProgress & block.itemUniqueIds:
                self._pausedForDuplicate = block.itemUniqueIds
                break

            # We're going to process it, remove it from the buffer
            self._fetchedBlockBuffer.popleft()

            # This should never fail
            d = self._runWorkerTask(block)
            d.addErrback(vortexLogFailure, self._logger)

            self._queueCount += 1
            if self._queueCount >= self.QUEUE_BLOCKS_MAX:
                break

        self._processorStatusNotifier.setProcessorStatus(True, self._queueCount)
        yield self._dedupeQueue()

    @inlineCallbacks
    def _runWorkerTask(self, block: ACIProcessorQueueBlockItem):

        startTime = datetime.now(pytz.utc)

        # Add the chunks we're processing to the set
        self._chunksInProgress |= block.itemUniqueIds

        try:
            d = self._sendToWorker(block)
            d.addTimeout(self.WORKER_TASK_TIMEOUT, reactor)

            results = yield d
            yield self._processWorkerResults(results)

            self._logger.debug("Processed %s items, Time Taken = %s",
                               len(block.items), datetime.now(pytz.utc) - startTime)

            # Success, Remove the chunks from the in-progress queue
            self._queueCount -= 1
            self._chunksInProgress -= block.itemUniqueIds
            self._queueIdsInBuffer -= set(block.queueIds)

            # If the queue processor was paused for this chunk then resume it.
            if self._pausedForDuplicate and self._pausedForDuplicate & block.itemUniqueIds:
                self._pausedForDuplicate = None

            # Notify the status controller
            self._processorStatusNotifier.setProcessorStatus(True, self._queueCount)
            self._processorStatusNotifier.addToProcessorTotal(len(block.items))

        except Exception as e:
            if isinstance(e, defer.TimeoutError):
                self._logger.info("Retrying process, Task has timed out.")
            else:
                self._logger.debug("Retrying process : %s", str(e))

            reactor.callLater(2.0, self._sendToWorker, block)
            return

    @abstractmethod
    def _sendToWorker(self, block: ACIProcessorQueueBlockItem) -> Deferred:
        """ Send to Worker

        This method calls the worker tasks, and resturns the deferred.
        Do not wait for the deferred and do any processing of the results here,
        do that instead in _processWorkerResults.

        Example code:

        def _sendToWorker(self, block: _BlockItem) -> Deferred:
            from peek_plugin_livedb._private.worker.tasks.LiveDbItemUpdateTask import \
                updateValues

            # Return the deferred, this is important
            return updateValues.delay(block.queueIds, block.items)

        """

    @abstractmethod
    def _processWorkerResults(self, results):
        """ Process Worker Results

        This method allows the inherting class to do something with the worker results.

        Example code:

        @inlineCallbacks
        def _processWorkerResults(self, results) -> Deferred:
            yield doSomethingWithResult(result)

        """

    def _fetchBlocks(self) -> List[ACIProcessorQueueBlockItem]:
        return deferToThreadWrapWithLogger(self._logger) \
            (self._fetchBlocksWrapped) \
            ()

    def _fetchBlocksWrapped(self) -> List[ACIProcessorQueueBlockItem]:
        queueTable = self._QueueDeclarative.__table__

        toGrab = self.QUEUE_BLOCKS_MAX - self._queueCount
        toGrab *= self.QUEUE_ITEMS_PER_TASK

        session = self._dbSessionCreator()
        try:
            sql = select([queueTable]) \
                .order_by(asc(queueTable.c.id)) \
                .limit(bindparam('b_toGrab'))

            sqlData = session \
                .execute(sql, dict(b_toGrab=toGrab)) \
                .fetchall()

            queueItems = [self._QueueDeclarative.sqlCoreLoad(row)
                          for row in sqlData
                          if row.id not in self._queueIdsInBuffer]

            queueBlocks = []
            for start in range(0, len(queueItems), self.QUEUE_ITEMS_PER_TASK):

                queueIds = []
                latestUpdates = {}
                for item in queueItems[start: start + self.QUEUE_ITEMS_PER_TASK]:
                    queueIds.append(item.id)
                    # NOTE: Do not mess with this "USE LAST ITEM" deduplication strategy
                    # Some plugins include values in their queues and we want the latest
                    # value.
                    latestUpdates[item.ckiUniqueKey] = item

                self._lastFetchedId = queueIds[-1]
                itemUniqueIds = set(latestUpdates.keys())
                items = list(latestUpdates.values())

                self._queueIdsInBuffer.update(queueIds)

                queueBlocks.append(
                    ACIProcessorQueueBlockItem(queueIds, items, itemUniqueIds)
                )

            return queueBlocks

        finally:
            session.close()

    # ---------------
    # Deduplicate methods

    def _dedupeQueue(self):
        gap = (datetime.now(pytz.utc) - self._lastDedupeTime).seconds
        if gap < self.DEDUPE_PERIOD_SECONDS:
            return

        self._lastDedupeTime = datetime.now(pytz.utc)

        return deferToThreadWrapWithLogger(self._logger) \
            (self._dedupeQueueWrapped) \
            ()

    def _dedupeQueueWrapped(self):
        """ Deduplicate Queue

        This method will look ahead and deduplicate the queue before this class loads
        up the data.

        This query will take approximately 32ms for a queue of 10,000

        """
        if not self._lastFetchedId:
            return

        dedupeLimit = self.DEDUPE_LOOK_AHEAD_MIN_ROWS
        sql = self._dedupeQueueSql(self._lastFetchedId, dedupeLimit)
        if not sql:
            return

        self._logger.debug("Duplicating queue for %s",
                           self._QueueDeclarative.tupleType())

        session = self._dbSessionCreator()
        try:
            session.execute(sql)
            session.commit()
        finally:
            session.close()

    @abstractmethod
    def _dedupeQueueSql(self, lastFetchedId: int, dedupeLimit: int):
        """ Deduplicate Queue SQL

        This method will look ahead and deduplicate the queue before this class loads
        up the data.

        Example code #1:

            def _dedupeQueueSql(self, lastFetchedId: int, dedupeLimit: int):
                # Disable the dedupe process
                pass


        Example code #2:

            def _dedupeQueueSql(self, lastFetchedId: int, dedupeLimit: int):
                 return '''
                     with sq_raw as (
                        SELECT "id", "gridKey"
                        FROM pl_diagram."GridKeyCompilerQueue"
                        WHERE id > %(id)s
                        LIMIT %(limit)s
                    ), sq as (
                        SELECT min(id) as "minId", "gridKey"
                        FROM sq_raw
                        GROUP BY "gridKey"
                        HAVING count("gridKey") > 1
                    )
                    DELETE
                    FROM pl_diagram."GridKeyCompilerQueue"
                         USING sq sq1
                    WHERE pl_diagram."GridKeyCompilerQueue"."id" != sq1."minId"
                        AND pl_diagram."GridKeyCompilerQueue"."id" > %(id)s
                        AND pl_diagram."GridKeyCompilerQueue"."gridKey" = sq1."gridKey"
                ''' % {'id': self._lastQueueId, 'limit': dedupeLimit}


        """

    # ---------------
    # Insert into Queue methods
    #
    # These are custom in the controllers, because they can be quite custom.
    # Some don't even have insert methods in the controller, they are done from the
    # worker.
