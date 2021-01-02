# Baseado no Postgres Hook
import psycopg2
from lib.credentials import gide_db_credentials, local_host_credentials


class PostgresConnector:
    def __init__(self):
        self._conn_params = None

    def get_conn(self, conn_params):
        self._conn_params = conn_params

        return psycopg2.connect(self._conn_params)

    @staticmethod
    def connect_using_default_credentials():
        default_conn = gide_db_credentials()
        return psycopg2.connect(default_conn)

    @staticmethod
    def connect_using_localhost_credentials():
        localhost_conn = local_host_credentials()
        return psycopg2.connect(localhost_conn)
