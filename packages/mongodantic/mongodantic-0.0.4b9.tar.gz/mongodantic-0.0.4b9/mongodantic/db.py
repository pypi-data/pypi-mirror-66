import os
from typing import Optional
from pymongo import MongoClient


class DBConnection(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBConnection, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.connection_string = os.environ.get('MONGODANTIC_CONNECTION_STR')
        self.db_name = os.environ.get('MONGODANTIC_DBNAME')
        self.max_pool_size = int(os.environ.get('MONGODANTIC_POOL_SIZE', 100))
        self.ssl = True if int(os.environ.get('MONGODANTIC_SSL', 0)) else False
        self.ssl_cert_path = os.environ.get('MONGODANTIC_SSL_CERT_PATH')
        self.server_selection_timeout_ms = int(os.environ['MONGODANTIC_SERVER_SELECTION_TIMEOUT_MS']) if os.environ.get(
            'MONGODANTIC_SERVER_SELECTION_TIMEOUT_MS') else 50000
        self.connect_timeout_ms = int(os.environ['MONGODANTIC_CONNECT_TIMEOUT_MS']) if \
            os.environ.get('MONGODANTIC_CONNECT_TIMEOUT_MS') else 50000
        self.socket_timeout_ms = int(os.environ['MONGODANTIC_SOCKET_TIMEOUT_MS']) if \
            os.environ.get('MONGODANTIC_SOCKET_TIMEOUT_MS') else 60000
        self._mongo_connection = self.__init_mongo_connection()
        self.database = self._mongo_connection.get_database(self.db_name)

    def __init_mongo_connection(self) -> MongoClient:
        connection_params = dict(
            connect=True,
            serverSelectionTimeoutMS=self.server_selection_timeout_ms,
            maxPoolSize=self.max_pool_size,
            connectTimeoutMS=self.connect_timeout_ms,
            socketTimeoutMS=self.socket_timeout_ms,
            retryWrites=True,
            retryReads=True,
        )
        if self.ssl:
            connection_params['tlsCAFile'] = self.ssl_cert_path
            connection_params['tlsAllowInvalidCertificates'] = self.ssl,
        return MongoClient(
            self.connection_string,
            **connection_params
        )

    def _reconnect(self):
        self._mongo_connection = self.__init_mongo_connection()
        self.database = self._mongo_connection.get_database(self.db_name)
        return self
