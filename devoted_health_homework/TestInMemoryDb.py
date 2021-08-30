from sys import stdin
import unittest
from InMemoryDb import InMemoryDb as imdb
import io
import sys
import logging

class TestInMemoryDb(unittest.TestCase):
    """
    Class to Test InMemoryDb class
    """
    def __init__(self, *args, **kwargs):
        super(TestInMemoryDb, self).__init__(*args, **kwargs)
        self.old_stdout = sys.stdout
        testString = "SET a foo"
        self.input = io.StringIO(testString)
        self.outputResult = io.StringIO() 
    
    def testSet(self):
        testImdbOject = imdb()
        testImdbOject.processInput(self.input)
        permanentValue = testImdbOject.dataInmemory
        log = logging.getLogger("TestInMemoryDB")
        log.debug("Test SET")
        self.assertEqual(permanentValue, {'a': 'foo'}) 

    def testGet(self):
        sys.stdout = self.outputResult
        getImdbObject = imdb()
        getImdbObject.processInput(self.input)
        getImdbObject.set(self.input.getvalue())
        getImdbObject.get(['a'])
        value = self.outputResult.getvalue().rstrip()
        sys.stdout =self.old_stdout
        self.assertEqual(value, 'foo')
        
    def testCount(self):
        sys.stdout = self.outputResult
        countImdbObject = imdb()
        countImdbObject.processInput(self.input)
        countImdbObject.count(['foo'])
        value = int(self.outputResult.getvalue().rstrip())
        sys.stdout =self.old_stdout
        self.assertEqual(value, 1) 

    def testDelete(self):
        sys.stdout = self.outputResult
        deleteImdbObject = imdb()
        deleteImdbObject.processInput(self.input) 
        deleteImdbObject.delete(['a'])
        deleteImdbObject.get(['a'])
        value = self.outputResult.getvalue().rstrip()
        sys.stdout =self.old_stdout
        self.assertEqual(value, 'NULL', msg='{0}, {1}')

    def testTransaction(self):
        testTransactionImdbObject = imdb()
        newInput = io.StringIO("SET a foo\nSET a bar\nSET a baz\nROLLBACK")
        testTransactionImdbObject.begin(newInput)
        temporaryValue = testTransactionImdbObject.temporary_transaction_dict
        self.assertEqual(temporaryValue, {'a': 'foo'})  
  
    
    def testExample1(self):
        testExample1ImdbObject = imdb()
        newInput = io.StringIO("SET a foo\nSET b foo\nDELETE a\nSET b baz\n")
        testExample1ImdbObject.processInput(newInput)
        permanentValue = testExample1ImdbObject.dataInmemory
        self.assertEqual(permanentValue, {'b': 'baz'})	

    def testExample2(self):
	    testExample2ImdbObject = imdb()
	    newInput = io.StringIO("SET a foo\nSET a foo\nDELETE a\n")
	    testExample2ImdbObject.processInput(newInput)
	    permanentValue = testExample2ImdbObject.dataInmemory
	    self.assertEqual(permanentValue, {})
    
    def testExample4(self):
        testExample4ImdbObject = imdb()
        beforeTransactionInput= io.StringIO("SET a foo\nSET b baz")
        testExample4ImdbObject.processInput(beforeTransactionInput)
        newTransactionInput= io.StringIO("SET a bar\nDELETE a\nROLLBACK\nCOMMIT\n")
        testExample4ImdbObject.begin(newTransactionInput)
        permanentValue = testExample4ImdbObject.dataInmemory
        self.assertEqual(permanentValue, {'a': 'bar', 'b': 'baz'}) 

    def testEnd(self):
        endImdbOject = imdb()
        with self.assertRaises(SystemExit):
            endImdbOject.end()

if __name__ == '__main__':
    unittest.main()