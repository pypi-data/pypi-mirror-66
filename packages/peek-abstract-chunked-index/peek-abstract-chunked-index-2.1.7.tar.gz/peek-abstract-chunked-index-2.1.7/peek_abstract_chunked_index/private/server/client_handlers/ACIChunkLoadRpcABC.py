from abc import ABCMeta
from typing import List, Any

from peek_abstract_chunked_index.private.tuples.ACIEncodedChunkTupleABC import \
    ACIEncodedChunkTupleABC
from peek_plugin_base.storage.DbConnection import DbSessionCreator
from sqlalchemy import select


class ACIChunkLoadRpcABC(metaclass=ABCMeta):
    def __init__(self, dbSessionCreator: DbSessionCreator):
        self._dbSessionCreator = dbSessionCreator

    # -------------
    def ckiInitialLoadChunksBlocking(self, offset: int,
                                     count: int,
                                     Declarative: ACIEncodedChunkTupleABC
                                     ) -> List[Any]:
        """ Chunked Key Index - Initial Load Chunks Blocking

        This method is used to load the initial set of chunks from the server
        to the client.

        """
        table = Declarative.__table__
        session = self._dbSessionCreator()
        try:
            sql = select([table]) \
                .order_by(Declarative.sqlCoreChunkKeyColumn()) \
                .offset(offset) \
                .limit(count)

            sqlData = session.execute(sql).fetchall()

            results: List[ACIEncodedChunkTupleABC] = [
                Declarative.sqlCoreLoad(item)
                for item in sqlData
            ]

            return results

        finally:
            session.close()
