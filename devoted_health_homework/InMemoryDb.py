import logging
import json
import sys
import collections
import os
import io

class InMemoryDb:  
    """
    Class that Implement an in-memory database with the following functions:
    - Reads values from STDIN line by line and executes functions as they happen
    """

    def __init__(self):
        self.dataInMemory = io.StringIO()
        self.set_logger()
        self.allowed_function_verb_list = ["SET", "GET", "DELETE", "COUNT", "END", "BEGIN", "ROLLBACK", "COMMIT"]

    def set_logger(self):
        """
        Method to set logger for this application. This is to be used to troubleshoot issues with this application.

        Args: None
        Returns: None
        """
        logger = logging.getLogger('InMemoryDb_logger')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger
    
    def usage(self):
        print("""
        These are the functions that are allowed with this program. Please review the examples folder for further help.
        SET [name] [value]
        Explanation: Sets the name in the database to the given value
        GET [name]
        Explanation: Prints the value for the given name. If the value is not in the database, prints N​ ULL
        DELETE [name]
        Explanation: Deletes the value from the database
        COUNT [value]
        Explanation: Returns the number of names that have the given value assigned to them. If that value is not assigned anywhere, prints ​0
        END
        Explanation: Exists the database
        
        * The database can also support transactions:
            BEGIN
            Explanation: Begins a new transaction
            ROLLBACK
            Explanation: Rolls back the most recent transaction. If there is no transaction to rollback, prints T​ RANSACTION NOT FOUND
            COMMIT
            Explanation: Commits all of the Open transactions
        """)

    def processInput(self, input):
        """
        Method to process input from stdin then perform next call

        Args: input
        Returns: None
        """
        self.input = input.rsplit()
        action = self.input[0]

        if action in self.allowed_function_verb_list:
            if action == "SET":
                self.SET()
            if action == "GET":
                self.GET()
            if action == "DELETE":
                self.DELETE()
            if action == "COUNT":
                self.COUNT()
            if action == "END":
                self.END()
        else:
            self.logger.info("Function \"%s\" is not in the list of allowed functions: %s" % (action, ",".join(self.allowed_function_verb_list)))

    def SET(self, name, value):
        """
        Method to Set the name in the database to the given value 
        SET [name] [value]

        Args: name, value 
        Returns: None
        """
        print("SET value")

    def GET(self, name):
        """
        Method to Print the value for the given name. If the value is not in the database, prints N​ULL
        GET [name]

        Args: name
        Returns: None
        """
        self.dataInMemory.write(input)
        #print(self.dataInMemory.getvalue())
        #print('Python.', file=self.dataInMemory)
        #print(self.dataInMemory.getvalue())
        print("GET value")

    def DELETE(self, value):
        """
        Method to Delete the value from the database
        DELETE [value] 

        Args: value
        Returns: None
        """
        print("DELETE value")

    def COUNT(self, value):
        """
        Method Returns the number of names that have the given value assigned to them. If that value is not assigned anywhere, prints ​0 
        Count [Value]

        Args: value
        Returns: number of names or 0
        """
        print("COUNT value")

    def END(self):
        """
        Method to Exit the database 

        Args: None
        Returns: None
        """
        self.logger.info("EXITING Database")
        self.dataInMemory.close()
        sys.exit(0)
    
if __name__ == "__main__":
    inMemoryDbObject = InMemoryDb()
    for line in sys.stdin:
        inMemoryDbObject.processInput(line) 
    