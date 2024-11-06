from abc import ABC, abstractmethod
import os
import dotenv
from pathlib import Path
import psycopg
from psycopg_pool import ConnectionPool
from contextlib import contextmanager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv(".env")

class Database(ABC):
    def __init__(self, driver):
        self.driver = driver
        self.pool = None

    @abstractmethod
    def create_pool(self):
        raise NotImplementedError()

    @abstractmethod
    def get_connection(self):
        raise NotImplementedError()

class PgDatabase(Database):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PgDatabase, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if not self.initialized:
            super().__init__(psycopg)
            self.create_pool()
            self.initialized = True

    def create_pool(self):
        """Create a connection pool with configurable parameters"""
        try:
            conninfo = (
                f"host={os.getenv('DB_HOST')} "
                f"port={int(os.getenv('DB_PORT', '5432'))} "
                f"dbname={os.getenv('DB_NAME')} "
                f"user={os.getenv('DB_USERNAME')} "
                f"password={os.getenv('DB_PASSWORD')}"
            )
            
            self.pool = ConnectionPool(
                conninfo=conninfo,
                min_size=int(os.getenv('DB_POOL_MIN_SIZE', '1')),
                max_size=int(os.getenv('DB_POOL_MAX_SIZE', '10')),
                timeout=float(os.getenv('DB_POOL_TIMEOUT', '30')),
                max_waiting=int(os.getenv('DB_POOL_MAX_WAITING', '5')),
                num_workers=int(os.getenv('DB_POOL_NUM_WORKERS', '3'))
            )
            logger.info("Connection pool created successfully")
        except Exception as e:
            logger.error(f"Error creating connection pool: {e}")
            raise

        
    @contextmanager
    def get_connection(self):
        """Get a connection from the pool"""
        conn = None
        cur = None
        try:
            conn = self.pool.getconn()
            cur = conn.cursor()
            yield conn, cur
        except Exception as e:
            logger.error(f"Error getting connection from pool: {e}")
            raise
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                self.pool.putconn(conn)

    def close_pool(self):
        """Close all connections in the pool"""
        if self.pool is not None:
            self.pool.close()
            logger.info("Connection pool has been closed")