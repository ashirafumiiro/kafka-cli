import unittest
import pytest
from app import read_args, send_message, read_messages
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


class TestSendMessage(unittest.TestCase):
    def test_send_message(self):
        args_dict = {'command': 'send', 'channel': 'testing', 'kafka': 'localhost', 'from': 'start'}
        result = send_message(args_dict, testing=True)
        self.assertTrue(result)


class TestReceiveMessages(unittest.TestCase):
    def test_receive_messages(self):
        send_args_dict = {'command': 'send', 'channel': 'testing', 
                            'kafka': 'localhost', 'from': 'start'}
        receive_args_dict = args_dict = {'command': 'receive', 'channel': 'testing', 
                                            'kafka': 'localhost', 'from': 'start'}
        self.assertTrue(send_message(send_args_dict, True))
        self.assertTrue(read_messages(receive_args_dict, testing=True))   
