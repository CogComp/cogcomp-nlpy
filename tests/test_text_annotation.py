import unittest
import sys
import os

#sys.path.insert(0,'/path/to/mod_directory')
#from sioux import pipeliner as p
from sioux import remote_pipeline

class TestTextAnnotation(unittest.TestCase):
    def setUp(self):
        self.rp = remote_pipeline.RemotePipeline()

    def test_tokens(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        tokens = [
            'Hello', ',', 'how', 'are', 'you', '.', 'I', 'am', 'doing', 'fine'
        ]
        self.assertEqual(ta.get_tokens, tokens)

    def test_end_pos(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        testarr = [6, 10]
        self.assertEqual(ta.get_sentence_end_token_indices, testarr)

    def test_score(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(ta.get_score, 1.0)

    def test_text(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(
            ta.get_text, "Hello,  how are you.\n\n\n I am doing fine")

    def test_invalid_constituents(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(ta.get_ner_conll.get_con_score(), None)

    def test_get_views(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        ta.get_pos
        ta.get_ner_conll
        views = ["NER_CONLL", "POS", "TOKENS"]
        self.assertEqual(sorted(ta.get_views), views)
