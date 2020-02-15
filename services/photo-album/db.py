import psycopg2

connection = None

def new_db_connection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432",
            database="photo_album",
        )

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        return connection

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    # finally:
    #     # closing database connection.
    #     if connection:
    #         cursor.close()
    #         connection.close()
    #         print("PostgreSQL connection is closed")


def get_db_connection():
    global connection
    if connection is None:
        connection = new_db_connection()
    return connection
