import unittest
import sys
import os

#sys.path.insert(0,'/path/to/mod_directory')
from sioux import pipeliner as p


class TestPipeliner(unittest.TestCase):
    def setUp(self):
        p.init(use_server=True)

    def test_tokens(self):
        ta = p.doc("Hello,  how are you.\n\n\n I am doing fine")
        tokens = [
            'Hello', ',', 'how', 'are', 'you', '.', 'I', 'am', 'doing', 'fine'
        ]
        self.assertEqual(p.get_tokens(ta), tokens)

    def test_end_pos(self):
        ta = p.doc("Hello,  how are you.\n\n\n I am doing fine")
        testarr = [6, 10]
        self.assertEqual(p.get_sentence_end_positions(ta), testarr)

    def test_score(self):
        ta = p.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(p.get_score(ta), 1.0)

    def test_text(self):
        ta = p.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(
            p.get_text(ta), "Hello,  how are you.\n\n\n I am doing fine")

    def test_invalid_constituents(self):
        ta = p.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(p.get_ner_conll(ta).get_con_score(), None)


class TestTextAnnotation(unittest.TestCase):
    def setUp(self):
        p.init(use_server=True)

    def test_get_views(self):
        ta = p.doc("Hello,  how are you.\n\n\n I am doing fine")
        p.get_pos(ta)
        p.get_ner_conll(ta)
        views = ["NER_CONLL", "POS", "TOKENS"]
        self.assertEqual(sorted(ta.get_views()), views)
