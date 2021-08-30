from sys import stdin
import unittest
from InMemoryDb import InMemoryDb as imdb
import io
import sys

class TestInMemoryDb(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInMemoryDb, self).__init__(*args, **kwargs)
        self.buffer = io.StringIO()
        self.old_stdout = sys.stdout
        testString = "SET a foo"
        self.input = io.StringIO(testString)
        self.outputResult = io.StringIO() 
    
    def testSet(self):
        testImdbOject = imdb()
        testImdbOject.processInput(self.input)
        permanentValue = testImdbOject.dataInmemory
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
        self.assertEqual(value, 'NULL')
  
    '''
    def testExample1(self):
        transactionString = "GET a\nSET a foo\nSET b foo\nCOUNT foo\nCOUNT bar\nDELETE a\nCOUNT foo\nSET b baz\nCOUNT foo\nGET b\nGET B"
        transactionExampleList = ['GET a', 'SET a foo', 'SET b foo', 'COUNT foo', 'COUNT bar', 'DELETE a', 'COUNT foo', 'SET b baz', 'COUNT foo', 'GET b', 'GET B']

    
    def testExample4(self):
        transactionString = "SET a foo\nSET b baz\nBEGIN\n\nGET a\nSET a bar\nCOUNT bar\nBEGIN\nCOUNT bar\nDELETE a\nGET a\nCOUNT bar\nROLLBACK\nGET a\nCOUNT bar\nCOMMIT\nGET a\nGET b"
        transactionImdbOject = imdb()
        for line in transactionString.splitlines():
            newInput = io.StringIO(line)
            transactionImdbOject.processInput(newInput)
            newInput.close()
        permanentValue = transactionImdbOject.dataInmemory
        self.assertEqual(permanentValue, {'b': 'baz', 'a': 'bar'})  
    '''

    def testEnd(self):
        endImdbOject = imdb()
        with self.assertRaises(SystemExit):
            endImdbOject.end()

if __name__ == '__main__':
    unittest.main()