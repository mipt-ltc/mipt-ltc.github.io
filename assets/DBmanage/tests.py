import io
from unittest.mock import patch
from unittest import TestCase
import unittest

import addNewNames 

class Test(unittest.TestCase):
    outList = ['']
    outMsg = ''
    def setup(self):
        def myPrint(msg):
            self.outMsg += msg
        addNewNames.input = lambda: 'yes\n'
        addNewNames.print = myPrint 

    def test_input(self):
        self.setup()
        inputTest()
        self.assertEqual(self.outMsg, 'yoyoy') 
        self.assertEqual(inputTest(), 'yes\n')
        
    def test_WhantToAdd(self):
        self.setup()
        addNewNames.input = lambda: 'y'
        addNewNames.main()
        
        self.assertEqual(self.outMsg, addNewNames.MSGS['createOrUpdate']) 
        self.assertEqual(inputTest(), 'yes\n')


    @patch('builtins.input', return_value='yes\n')
    def test_inputing(self, mock_stdin):
        self.assertEqual(inputTest(), 'yes\n')


#   @patch('builtins.input', return_value='yessss')
#   @unittest.mock.patch('sys.stdin', new_callable=io.StringIO)
#   def test_WantToProcessName(self, mock_stdin, mock_stdout):
#       mock_stdin = 'yesss\n'
#       testFunc()
#       self.assertEqual(mock_stdout.getvalue(), 'no\n')

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()

