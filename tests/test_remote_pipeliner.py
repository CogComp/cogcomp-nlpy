import unittest
import sys
import os

#sys.path.insert(0,'/path/to/mod_directory')
#from sioux import pipeliner as p
from sioux import remote_pipeliner

class TestPipeliner(unittest.TestCase):
    def setUp(self):
        #p.init(use_server=True)
        self.rp = remote_pipeliner.RemotePipeliner()

    def test_tokens(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        tokens = [
            'Hello', ',', 'how', 'are', 'you', '.', 'I', 'am', 'doing', 'fine'
        ]
        self.assertEqual(self.rp.get_tokens(ta), tokens)

    def test_end_pos(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        testarr = [6, 10]
        self.assertEqual(self.rp.get_sentence_end_positions(ta), testarr)

    def test_score(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(self.rp.get_score(ta), 1.0)

    def test_text(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(
            self.rp.get_text(ta), "Hello,  how are you.\n\n\n I am doing fine")

    def test_invalid_constituents(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(self.rp.get_ner_conll(ta).get_con_score(), None)


class TestTextAnnotation(unittest.TestCase):
    def setUp(self):
        self.rp = remote_pipeliner.RemotePipeliner()

    def test_get_views(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.rp.get_pos(ta)
        self.rp.get_ner_conll(ta)
        views = ["NER_CONLL", "POS", "TOKENS"]
        self.assertEqual(sorted(ta.get_views()), views)
