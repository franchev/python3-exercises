import logging
import json
import sys
import collections
import os
import io
import threading
import queue
import time
import fileinput
import select

class InMemoryDb:  
    """
    Class that Implement an in-memory database with the following functions:
    - Reads values from STDIN line by line and executes functions as they happen
    """

    def __init__(self):
        self.dataInmemory = {}
        self.setLogger()
        self.allowed_function_verb_list = ["SET", "GET", "DELETE", "COUNT", "END", "BEGIN"]
        self.allowed_transaction_verb_list = ["SET", "GET", "DELETE", "END", "ROLLBACK", "COMMIT"]
        self.temporary_transaction_list = []
        self.temporary_transaction_dict = {}
        self.transaction_action = False
        self.rollback_triggered = False
        self.transaction_count = 0
    
    def actionVerbValidator(self, action):
        """
        Method that calls other methods to perform actions

        Args: input, transaction_action
        Returns: None
        """
        try:
            combine_allowed_list = set(self.allowed_function_verb_list + self.allowed_transaction_verb_list)
            if action not in combine_allowed_list:
                return False
            else:
                return True
        except Exception as error:
            self.logger.error("Error while performing validating actionVerbs, please review. Please review error: %s" % error)

    
    def performActions(self, input):
        """
        Method that calls other methods to perform actions

        Args: input
        Returns: None
        """
        try:
            action = input[0]
            data = input[1:]

            if action == "END":
                self.end()
            if action == "SET":
                self.set(data)
            if action == "GET":
                self.get(data)
            if action == "DELETE":
                self.delete(data)
            if action == "COUNT":
                self.count(data)
            if action == "ROLLBACK":
                self.rollback()
            if action == "COMMIT":
                self.commit()
        except Exception as error:
            self.logger.error("Error while performing action, please review. Please review error: %s" % error)

    def processInput(self, stdin):
        """
        Method to process input from stdin

        Args: stdin
        Returns: None
        """
        try:
            for line in stdin:
                if not line:
                    self.logger.error("Input cannot be empty")
                    return
                data = line.rsplit()
                actionVerb = data[0]
                if actionVerb == "BEGIN":
                    stdInNew = sys.stdin
                    self.begin(stdInNew)
                elif self.actionVerbValidator(actionVerb):
                    self.performActions(data)    
                else:
                    self.logger.error("function '%s' not allowed, supported fuctions are %s" % (actionVerb, (self.allowed_transaction_verb_list + self.allowed_function_verb_list)))
        except Exception as error:
            self.logger.error("Cannot Process INput. Please review error: %s" % error)

    def setLogger(self):
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
    
    def set(self, data):
        """
        Method to Set the name in the database to the given value 
        SET [name] [value]

        Args: data
        Returns: None
        """
        try:
            if len(data) <= 1:
                self.logger.error("SET requires 2 values, only %d provided. Example SET a foo" % len(data))
                return
            name = data[0]
            value = data[1]
            if not self.transaction_action:
                self.dataInmemory[name] = value
            else:
                self.transaction_count += 1
                self.temporary_transaction_list.append({name: value})
                self.temporary_transaction_dict[name] = value
        except Exception as error:
            self.logger.error("Cannot SET. Please review error: %s" % error)

    def get(self, data):
        """
        Method to Print the value for the given name. If the value is not in the database, prints N​ULL
        GET [name]

        Args: data
        Returns: None
        """
        try:
            if len(data) < 1:
                self.logger.error("GET requires 1 value, only %d provided. Example GET a" % len(data))
                return
            name = data[0]

            def getItem(name, dictionary):
                if name in dictionary:
                    print(dictionary[name])
                else:
                    print("NULL")

            if not self.transaction_action:
                getItem(name, self.dataInmemory)
            else:
                getItem(name, self.temporary_transaction_dict)
        except Exception as error:
            self.logger.error("Cannot Get. Please review error: %s" % error)

    def delete(self, data):
        """
        Method to Delete the value from the database
        DELETE [value] 

        Args: value
        Returns: None
        """
        try:
            if len(data) < 1:
                self.logger.error("DELETE require 1 value, only %d provided. Example DELETE a" % len(data))
                return
            name = data[0]
            if not self.transaction_action:
                if name in self.dataInmemory:
                    del self.dataInmemory[name]
            else:
                if name in self.temporary_transaction_dict:
                    del self.temporary_transaction_dict[name]
        except Exception as error:
            self.logger.error("Cannot DELETE. Please review error: %s" % error)

    def count(self, data):
        """
        Method Returns the number of names that have the given value assigned to them. If that value is not assigned anywhere, prints ​0 
        Count [Value]

        Args: data
        Returns: number of names or 0
        """
        try:
            def countValue(val, dictionary):
                sum = 0
                for key, value in dictionary.items():
                    if value == val:
                        sum += 1
                print(sum)
            
            if len(data) < 1:
                self.logger.error("COUNT require 1 value, only %d provided. Example COUNT foo" % len(data))
                return
            val = data[0]
            if not self.transaction_action:
                countValue(val, self.dataInmemory)
            else:
                countValue(val, self.temporary_transaction_dict)
        except Exception as error:
            self.logger.error("Cannot COUNT. Please review error: %s" % error)

    def begin(self, stdin):
        """
        Method to Begin a transaction

        Args: stdin
        Returns: None
        """
        self.transaction_action = True
        self.temporary_transaction_dict = self.dataInmemory
        for line in stdin:
            data = line.rsplit()
            newAction = data[0]
            if self.actionVerbValidator(newAction):
                self.performActions(data)
            else:
                self.logger.error("function '%s' not allowed, supported fuctions are %s" % (newAction, (self.allowed_transaction_verb_list + self.allowed_function_verb_list))) 

    def rollback(self):
        """
        Method to rollback a transaction 

        Args: None 
        Returns: None 
        """
        try:
            self.rollback_triggered = True
            if self.transaction_count >= len(self.temporary_transaction_list):
                self.temporary_transaction_dict = (self.temporary_transaction_list[0])
                self.transaction_count = 0
            else:
                self.temporary_transaction_dict = {}
        except Exception as error:
            self.logger.error("CANNOT ROLLBACK. Please review error: %s" % error)

    def commit(self):
        """
        Method to commit transaction to memory

        Args: None
        Returns: None
        """
        try:
            self.dataInmemory.update(self.temporary_transaction_dict)
            self.temporary_transaction_dict = {}
            self.temporary_transaction_list = []
            self.transaction_action = False
            self.transaction_count = 0
        except Exception as error:
            self.logger.error("CANNOT COMMIT. Please review error: %s" % error)

    def end(self):
        """
        Method to Exit the database 

        Args: None
        Returns: None
        """
        try:
            self.logger.info("EXITING Database")
            sys.exit(1)
        except Exception as error:
            self.logger.error("CANNOT END, PLEASE PRESS CTRL+C TO FORCE EXIT. Please review error: %s" % error)

if __name__ == "__main__":
    inMemoryDbObject = InMemoryDb()
    inMemoryDbObject.processInput(sys.stdin)