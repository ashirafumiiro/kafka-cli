import unittest
import pytest
from app import read_args
import os


class TestReadArgs(unittest.TestCase):

    def test_read_args_with_no_arguments(self):
        with self.assertRaises(SystemExit):
            read_args()
    
    def test_supplying_send_command(self):
        output = os.popen("python -c 'import app; print(app.read_args())' "+\
            "send --channel test --kafka localhost")
        self.assertEqual(output.read(), "{'command': 'send', 'channel': 'test', 'kafka': 'localhost', 'from': 'start'}\n")
    
    def test_supplying_receive_command(self):
        output = os.popen("python -c 'import app; print(app.read_args())' "+\
            "receive --channel test --kafka localhost")
        self.assertEqual(output.read(), "{'command': 'receive', 'channel': 'test', 'kafka': 'localhost', 'from': 'start'}\n")

    def test_supplying_invalid_command(self):
        output = os.popen("python -c 'import app; print(app.read_args())' "+\
            "invalid_cmd --channel test --kafka localhost")
        output = output.read()
        self.assertTrue(output == '')  # An error occured


