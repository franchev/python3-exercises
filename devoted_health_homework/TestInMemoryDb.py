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
    
    def testEnd(self):
        endImdbOject = imdb()
        with self.assertRaises(SystemExit):
            endImdbOject.end()


    def testTransaction(self):
        pass

if __name__ == '__main__':
    unittest.main()