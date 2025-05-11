import sqlite3


class DatabaseHandler:

    def __init__(self, db_path: str):
        """
        Initializes the DatabaseHandler with the path to the SQLite database.

        Args:
            db_path: The path to the SQLite database file.
        """
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """
        Establishes a connection to the SQLite database.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def disconnect(self):
        """
        Closes the connection to the SQLite database.
        """
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, query: str, params: tuple = None) -> list:
        """
        Executes an SQL query.

        Args:
            query: The SQL query to execute.
            params: Optional parameters to pass to the query (to prevent SQL injection).

        Returns:
            A list of tuples representing the result of the query.
        """
        try:
            if not self.conn:
                self.connect()  # Ensure connection is active

            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()  # Save changes to the database
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            if self.conn:
                self.disconnect()  # Close connection after use