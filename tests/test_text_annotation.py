import unittest
import sys
import os

# sys.path.insert(0,'/path/to/mod_directory')
# from ccg_nlpy import pipeliner as p
from ccg_nlpy import remote_pipeline


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
        views = ["NER_CONLL", "POS", "SENTENCE", "TOKENS"]
        self.assertEqual(sorted(ta.get_views), views)

    def test_sent_boundaries(self):
        text = "Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and " \
               "so dedicated, can long endure. We are met on a great battle-field of that war. We have come to " \
               "dedicate a portion of that field, as a final resting place for those who here gave their lives that " \
               "that nation might live. It is altogether fitting and proper that we should do this. "
        ta = self.rp.doc(text)
        boundaries = ta.get_sentence_boundaries
        self.assertEqual(boundaries, [(0, 28), (28, 39), (39, 68), (68, 80)])
