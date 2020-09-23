import json
from configparser import ConfigParser

import psycopg2

class Database:
    def __init__(self, filename):
        self.params = self.config(filename)
        self.conn = self.connect()

    def config(self, filename, section='postgresql'):
        # Create a parser
        parser = ConfigParser()

        # Read config file
        parser.read(filename)

        # Get section, default to PostgreSQL
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def connect(self):
        """Connect to the PostgreSQL database server."""
        conn = None
        try:
            # Read connection parameters
            params = self.params

            # Connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            # Create a cursor
            cur = conn.cursor()

            # Execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # Display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

            # Close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return conn

    def close(self):
        if self.conn:
            self.conn.close()

    def explain_query(self, query):
        """Returns the query plan tree produced by the database optimizer in
        JSON format.
        """
        query = "EXPLAIN (COSTS, FORMAT JSON) {};".format(query)

        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchone()

        cursor.close()

        return rows
