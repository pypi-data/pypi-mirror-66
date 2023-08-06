import logging
from abc import ABCMeta
from typing import List, Optional, Dict

from sqlalchemy import select
from twisted.internet.defer import Deferred
from vortex.DeferUtil import vortexLogFailure, deferToThreadWrapWithLogger
from vortex.Payload import Payload
from vortex.VortexFactory import VortexFactory, NoVortexException

from peek_abstract_chunked_index.private.tuples.ACIEncodedChunkTupleABC import \
    ACIEncodedChunkTupleABC
from peek_plugin_base.PeekVortexUtil import peekClientName


class ACIChunkUpdateHandlerABC(metaclass=ABCMeta):
    """ Client Chunked Index Update Controller

    This controller handles sending updates the the client.

    It uses lower level Vortex API

    It does the following a broadcast to all clients:

    1) Sends grid updates to the clients

    2) Sends Lookup updates to the clients

    """

    _ChunkedTuple: ACIEncodedChunkTupleABC = None
    _updateFromServerFilt: Dict = None
    _logger: logging.Logger = None

    def __init__(self, dbSessionCreator):
        self._dbSessionCreator = dbSessionCreator

    def shutdown(self):
        pass

    def sendChunks(self, chunkKeys: List[str]) -> None:
        """ Send Location Indexes

        Send grid updates to the client services

        :param chunkKeys: A list of object buckets that have been updated
        :returns: Nochunked
        """

        if not chunkKeys:
            return

        if peekClientName not in VortexFactory.getRemoteVortexName():
            self._logger.debug("No clients are online to send the chunked chunk to, %s",
                               chunkKeys)
            return

        def send(vortexMsg: bytes):
            if vortexMsg:
                VortexFactory.sendVortexMsg(
                    vortexMsg, destVortexName=peekClientName
                )

        d: Deferred = self._loadChunks(chunkKeys)
        d.addCallback(send)
        d.addErrback(self._sendErrback, chunkKeys)

    def _sendErrback(self, failure, chunkKeys):

        if failure.check(NoVortexException):
            self._logger.debug(
                "No clients are online to send the chunked chunk to, %s", chunkKeys)
            return

        vortexLogFailure(failure, self._logger)

    def _loadChunks(self, chunkKeys: List[str]) -> Optional[bytes]:
        return deferToThreadWrapWithLogger(self._logger) \
            (self._loadChunksWrapped) \
            (chunkKeys)

    def _loadChunksWrapped(self, chunkKeys: List[str]) -> Optional[bytes]:

        session = self._dbSessionCreator()
        try:
            sql = self._makeLoadSql(chunkKeys)

            sqlData = session.execute(sql).fetchall()

            results: List[ACIEncodedChunkTupleABC] = [
                self._ChunkedTuple.sqlCoreLoad(item)
                for item in sqlData
            ]

            deletedChunkKeys = set(chunkKeys) - set([r.ckiChunkKey for r in results])

            for chunkKey in deletedChunkKeys:
                results.append(
                    self._ChunkedTuple.ckiCreateDeleteEncodedChunk(chunkKey)
                )

            if not results:
                return None

            return Payload(filt=self._updateFromServerFilt, tuples=results) \
                .makePayloadEnvelope(compressionLevel=3) \
                .toVortexMsg()

        finally:
            session.close()

    def _makeLoadSql(self, chunkKeys: List[str]):
        table = self._ChunkedTuple.__table__

        return select([table]) \
            .where(self._ChunkedTuple.sqlCoreChunkKeyColumn().in_(chunkKeys))
