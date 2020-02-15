import psycopg2
from psycopg2 import pool
import logging

postgreSQL_pool = None

def init_conn_pool():
  logger = logging.getLogger("logger")
  global postgreSQL_pool
  try:
      postgreSQL_pool = pool.SimpleConnectionPool(
        1, 20,
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432",
        database="photo_album"
      )

      if (postgreSQL_pool):
        logger.info("Connection pool created successfully")
      else:
        logger.error("Failed to create connection pool")

  except (Exception, psycopg2.DatabaseError) as error :
      logger.error("Error while connecting to PostgreSQL", error)

  finally:
      #closing database connection.
      # use closeall method to close all the active connection if you want to turn of the application
      # if (postgreSQL_pool):
      #     postgreSQL_pool.closeall
      # print("PostgreSQL connection pool is closed")
      pass


init_conn_pool()


def get_connection():
    return postgreSQL_pool.getconn()


def put_connection(conn):
  postgreSQL_pool.putconn(conn)
