# InMemoryDB
A python class that Implement an in-memory database that performs certain functions. The database is a command line program that reads values from STDIN line by line and executes the functions as they happen. Please review the Usage Section for how to use.

## Usage
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

- The database can also support transactions:
    BEGIN
    Explanation: Begins a new transaction
    ROLLBACK
    Explanation: Rolls back the most recent transaction. If there is no transaction to rollback, prints T​ RANSACTION NOT FOUND
    COMMIT
    Explanation: Commits all of the Open transactions