import unittest
import pytest


class TestReadArgs(unittest.TestCase):


    def test_read_args(self):
        args = ['app.py', 'send', '-c', 'main', '-k', 'localhost:5050', '--from', 'latest']
        pass


