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
        self.assertEqual(p.get_end_pos(ta), testarr)

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


class TestView(unittest.TestCase):
    def setUp(self):
        p.init(use_server=True)

    def test_print_view(self):
        ta = p.doc("Hello, how are you. I am Bruce Wayne.")
        pos_print = "POS view: (UH Hello) (, ,) (WRB how) (VBP are) (PRP you) (. .) (PRP I) (VBP am) (NNP Bruce) (NNP Wayne) (. .) "
        ner_print = "NER_CONLL view: (PER Bruce Wayne) "
        pos = p.get_pos(ta)
        ner = p.get_ner_conll(ta)

        self.assertEqual(pos_print, pos.__str__())
        self.assertEqual(ner_print, ner.__str__())

    def test_get_con_with_different_keys(self):
        ta = p.doc("Hello,  how are you. I am Bruce Wayne.")
        pos_tokens = [
            'Hello', ',', 'how', 'are', 'you', '.', 'I', 'am', 'Bruce',
            'Wayne', '.'
        ]

        ner_tokens = ['Bruce Wayne']
        ner_label = ['PER']
        ner_score = [1.0]
        ner_pos = [(8, 10)]

        pos = p.get_pos(ta)
        ner = p.get_ner_conll(ta)

        self.assertEqual(pos.get_cons(None, "token"), pos_tokens)
        self.assertEqual(ner.get_cons(None, "token"), ner_tokens)

        self.assertEqual(ner.get_cons(None, "label"), ner_label)
        self.assertEqual(ner.get_cons(None, "score"), ner_score)
        self.assertEqual(ner.get_cons(None, "position"), ner_pos)

    def test_view_type(self):
        ta = p.doc("Hello,  how are you.\n\n\n I am doing fine")
        pos_view = p.get_view(ta, "POS")
        stanford = p.get_view(ta, "PARSE_STANFORD")
        self.assertEqual(pos_view.get_view_type(), "TokenLabelView")
        self.assertEqual(stanford.get_view_type(), "TreeView")

    def test_relations(self):
        ta = p.doc("Hello,  how are you.\n\n\n I am doing fine")
        dependency = p.get_view(ta, "DEPENDENCY_STANFORD")
        relation_array = ['discourse', 'advmod', 'cop', 'nsubj', 'aux', 'dobj']
        self.assertEqual(dependency.get_relations(), relation_array)
