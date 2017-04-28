import unittest
import sys
import os

#sys.path.insert(0,'/path/to/mod_directory')
#from sioux import pipeliner as p
from sioux import remote_pipeline

class TestView(unittest.TestCase):
    def setUp(self):
        self.rp = remote_pipeline.RemotePipeline()

    def test_print_view(self):
        ta = self.rp.doc("Hello, how are you. I am Bruce Wayne.")
        pos_print = "POS view: (UH Hello) (, ,) (WRB how) (VBP are) (PRP you) (. .) (PRP I) (VBP am) (NNP Bruce) (NNP Wayne) (. .) "
        ner_print = "NER_CONLL view: (PER Bruce Wayne) "
        pos = self.rp.get_pos(ta)
        ner = self.rp.get_ner_conll(ta)

        self.assertEqual(pos_print, pos.__str__())
        self.assertEqual(ner_print, ner.__str__())

    def test_get_con_with_different_keys(self):
        ta = self.rp.doc("Hello,  how are you. I am Bruce Wayne.")
        pos_tokens = [
            'Hello', ',', 'how', 'are', 'you', '.', 'I', 'am', 'Bruce',
            'Wayne', '.'
        ]

        ner_tokens = ['Bruce Wayne']
        ner_label = ['PER']
        ner_score = [1.0]
        ner_pos = [(8, 10)]

        pos = self.rp.get_pos(ta)
        ner = self.rp.get_ner_conll(ta)

        self.assertEqual(pos.get_cons(None, "tokens"), pos_tokens)
        self.assertEqual(ner.get_cons(None, "tokens"), ner_tokens)

        self.assertEqual(ner.get_cons(None, "label"), ner_label)
        self.assertEqual(ner.get_cons(None, "score"), ner_score)
        self.assertEqual(ner.get_cons(None, "position"), ner_pos)

    def test_view_type(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        pos_view = self.rp.get_view(ta, "POS")
        stanford = self.rp.get_view(ta, "PARSE_STANFORD")
        self.assertEqual(pos_view.get_view_type(), "TokenLabelView")
        self.assertEqual(stanford.get_view_type(), "TreeView")

    def test_relations(self):
        ta = self.rp.doc("Hello,  how are you.\n\n\n I am doing fine")
        dependency = self.rp.get_view(ta, "DEPENDENCY_STANFORD")
        relation_array = ['discourse', 'advmod', 'cop', 'nsubj', 'aux', 'dobj']
        array = []
        for relation in dependency.get_relations():
            array.append(relation['relationName'])
        self.assertEqual(array, relation_array)
