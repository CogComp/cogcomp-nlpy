import unittest
import sys
import os

from ccg_nlpy import TextAnnotation

class TestView(unittest.TestCase):
    def setUp(self):
        with open('sample_text_annotation.json', 'r') as myfile:
            data = myfile.read()
        self.ta = TextAnnotation(json_str=data)

    def test_print_view(self):
        print(self.ta.as_json)
