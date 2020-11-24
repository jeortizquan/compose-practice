import sqlite3
from sqlite3 import Error

class QuotesMapper:

    def __init__(self):
        self.database_file = r"../db/quotes.db"

    def connect(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn
    
    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_db_from_scratch(self):
        sql_create_authors_table = """ CREATE TABLE IF NOT EXISTS authors ( 
                                            id integer PRIMARY KEY,
                                            name text NOT NULL
                                    ); """

        sql_create_quotes_table = """CREATE TABLE IF NOT EXISTS quotes (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        author_id integer NOT NULL 
                                        FOREIGN KEY (author_id) REFERENCES authors (id)  
                                    );"""

        # create a database connection
        conn = self.connect(self.database_file)

        # create tables
        if conn is not None:
            # create projects table
            self.create_table(conn, sql_create_authors_table)

            # create tasks table
            self.create_table(conn, sql_create_quotes_table)
        else:
            print("Error while create the database from scratch.")

    def create_author(self, conn, author):
        """
        Create a new project into the projects table
        :param conn:
        :param author:
        :return: author id
        """
        sql = ''' INSERT INTO authors(name)
                  VALUES(?) '''
        cur = conn.cursor()
        cur.execute(sql, author)
        conn.commit()
        return cur.lastrowid

    def create_quote(self, conn, quote):
        """
        Create a new quote
        :param conn:
        :param quote:
        :return: quote id
        """

        sql = ''' INSERT INTO quote(name,author_id)
                  VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, quote)
        conn.commit()
        return cur.lastrowid

    def populate_database(self):
        # create a database connection
        conn = self.connect(self.database_file)
        with conn:
            # create a new author
            author = ('Wayne Dyer');
            author_id = self.create_author(conn, author)

            # quotes
            quote_1 = ('If you change the way you look at things, the things you look at change', author_id)
            quote_2 = ('It’s never crowded along the extra mile.', author_id)
            quote_3 = ('Miracles come in moments. Be ready and willing.', author_id)

            # create quotes
            self.create_quote(conn, quote_1)
            self.create_quote(conn, quote_2)
            self.create_quote(conn, quote_3)