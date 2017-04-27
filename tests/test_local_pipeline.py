import unittest
import sys
import os

from sioux import local_pipeline
if os.path.exists('annotation-cache'):
    os.remove('annotation-cache')
lp = local_pipeline.LocalPipeline(enable_views=['POS']) 

class TestLocalPipeline(unittest.TestCase):
    def setUp(self):
        self.lp = lp

    def test_tokens(self):
        ta = self.lp.doc("Hello,  how are you.\n\n\n I am doing fine")
        tokens = [
            'Hello', ',', 'how', 'are', 'you', '.', 'I', 'am', 'doing', 'fine'
        ]
        self.assertEqual(self.lp.get_tokens(ta), tokens)

    def test_end_pos(self):
        ta = self.lp.doc("Hello,  how are you.\n\n\n I am doing fine")
        testarr = [6, 10]
        self.assertEqual(self.lp.get_sentence_end_token_indices(ta), testarr)

    def test_score(self):
        ta = self.lp.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(self.lp.get_score(ta), 1.0)

    def test_text(self):
        ta = self.lp.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(
            self.lp.get_text(ta), "Hello,  how are you.\n\n\n I am doing fine")

    def test_enabled_views(self):
        ta = self.lp.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(self.lp.get_pos(ta).view_name, 'POS')

    def test_disabled_views(self):
        ta = self.lp.doc("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(self.lp.get_lemma(ta), None)
