import unittest
import sys
import os

#sys.path.insert(0,'/path/to/mod_directory')
from sioux.pipeliner import Pipeliner


class TestPipeliner(unittest.TestCase):

    def test_tokens(self):
        p = Pipeliner()
        ta = p.text_annotation("Hello,  how are you.\n\n\n I am doing fine")
                        #"POS,LEMMA,PARSE_STANFORD,QUANTITIES,NER_CONLL,DEPENDENCY_STANFORD,SHALLOW_PARSE")
        tokens=['Hello', ',', 'how', 'are', 'you', '.', 'I', 'am', 'doing', 'fine']
        self.assertEqual(p.get_tokens(ta), tokens)

    def test_end_pos(self):
        p = Pipeliner()
        ta = p.text_annotation("Hello,  how are you.\n\n\n I am doing fine")
                       # "POS,LEMMA,PARSE_STANFORD,QUANTITIES,NER_CONLL,DEPENDENCY_STANFORD,SHALLOW_PARSE")
        testarr = [6, 10]
        self.assertEqual(p.get_end_pos(ta), testarr)

    def test_score(self):
        p = Pipeliner()
        ta = p.text_annotation("Hello,  how are you.\n\n\n I am doing fine")
                        #"POS,LEMMA,PARSE_STANFORD,QUANTITIES,NER_CONLL,DEPENDENCY_STANFORD,SHALLOW_PARSE")
        self.assertEqual(p.get_score(ta), 1.0)

    def test_text(self):
        p = Pipeliner()
        ta = p.text_annotation("Hello,  how are you.\n\n\n I am doing fine")
        self.assertEqual(p.get_text(ta), "Hello,  how are you.\n\n\n I am doing fine")

class TestView(unittest.TestCase):

    def test_ViewType(self):
        p = Pipeliner()
        ta = p.text_annotation("Hello,  how are you.\n\n\n I am doing fine")
        pos_view = p.get_view(ta, "POS")
        stanford = p.get_view(ta, "PARSE_STANFORD")
                        #"POS,LEMMA,PARSE_STANFORD,QUANTITIES,NER_CONLL,DEPENDENCY_STANFORD,SHALLOW_PARSE")
        self.assertEqual(pos_view.getViewType(), "TokenLabelView")
        self.assertEqual(stanford.getViewType(), "TreeView")

    def test_Relations(self):
        p = Pipeliner()
        ta = p.text_annotation("Hello,  how are you.\n\n\n I am doing fine")
        dependency = p.get_view(ta, "DEPENDENCY_STANFORD")
                       # "POS,LEMMA,PARSE_STANFORD,QUANTITIES,NER_CONLL,DEPENDENCY_STANFORD,SHALLOW_PARSE")
        relationArray = ['discourse', 'advmod', 'cop', 'nsubj', 'aux', 'dobj']
        self.assertEqual(dependency.getRelations(), relationArray)
