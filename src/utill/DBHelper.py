from contextlib import contextmanager
import atexit
from mysql import connector

class DBHelper:
    def __init__(self):
        self._connection_pool = None

    def initialize_connection_pool(self):
      
        db_user = "dw"
        db_pass = "icdw!23"
        db_url = "192.168.22.9"
        self._connection_pool = connector.pooling.MySQLConnectionPool(pool_name="cp",
                                                             pool_size=5,
                                                             autocommit=True,
                                                             user=db_user,
                                                             password=db_pass,
                                                             host=db_url,
                                                             database='icdw')
    @contextmanager
    def get_resource_rdb(self, autocommit=True):
        if self._connection_pool is None:
            self.initialize_connection_pool()

        conn = self._connection_pool.get_connection()
        conn.autocommit = autocommit
        cursor = conn.cursor(dictionary=True)
        
        try:
            yield cursor, conn
        finally:
            cursor.close()
            conn.close()
          

    def shutdown_connection_pool(self):
        if self._connection_pool is not None:
            self._connection_pool._remove_connections()

db_helper = DBHelper()

@atexit.register
def shutdown_connection_pool():
    db_helper.shutdown_connection_pool()