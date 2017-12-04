import pyodbc


class Db:
    """
    Database class
    """

    #
    # Constructor for Database class
    #
    def __init__(self):

        server_name = "Mikes-laptop\SQLExpress"
        db_name = "DiabeticLogger"

        connection_string = "DRIVER={SQL Server Native Client 11.0};"
        connection_string += "SERVER=" + server_name + ";"
        connection_string += "DATABASE=" + db_name + ";"
        connection_string += "UID=sa;"
        connection_string += "PWD=Vampires6!"

        try:
            self.__connection = pyodbc.connect(connection_string, autocommit=True)
            self.__cursor = self.__connection.cursor()

        except pyodbc.Error as ex:
            print(ex.args)

    def __enter__(self):
        """
        Returns a cursor to the database once you enter the WITH statements
        :return: Cursor to database connection
        """
        return self.__cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """
        When a with statement exits this will close and delete the cursor and close the database
        :param exc_type: exception type
        :param exc_value: exception value
        :param traceback: traceback for exception
        """
        self.__cursor.close()
        del self.__cursor
        self.__connection.close()


