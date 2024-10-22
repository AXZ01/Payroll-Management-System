import pyodbc
from utils.DBPropertyUtil import DBPropertyUtil


class DBConnUtil:
    @staticmethod
    def get_connection(config_file):
        try:
            # Get the connection string from the properties file
            connection_string = DBPropertyUtil.get_connection_string(
                config_file)

            # Connect to the database using pyodbc
            conn = pyodbc.connect(connection_string)
            return conn
        except pyodbc.Error as ex:
            # Handle connection errors
            sqlstate = ex.args[0]
            error_message = ex.args[1]
            print(f"Database connection failed with error: SQLState: {sqlstate}, Error: {error_message}")
            return None
