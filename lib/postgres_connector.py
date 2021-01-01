# Baseado no Postgres Hook
import psycopg2


class PostgresConnector:
    def __init__(self, conn_params):
        self.conn_params = conn_params

    def get_conn(self):
        return psycopg2.connect(self.conn_params)
