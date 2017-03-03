from unittest import TestCase
import sys
from cogcomp_python_utils.CgPipeliner import CgPipeliner


class TestPipeliner(TestCase):

    def test_tokens(self):
        s = CgPipeliner("Hello,  how are you.\n\n\n I am doing fine",
                        "POS,LEMMA,PARSE_STANFORD,QUANTITIES,NER_CONLL,DEPENDENCY_STANFORD,SHALLOW_PARSE")
        tokens=['Hello', ',', 'how', 'are', 'you', '.', 'I', 'am', 'doing', 'fine']
        self.assertEqual(s.getTokens(), tokens)

    def test_EndPos(self):
        s = CgPipeliner("Hello,  how are you.\n\n\n I am doing fine",
                        "POS,LEMMA,PARSE_STANFORD,QUANTITIES,NER_CONLL,DEPENDENCY_STANFORD,SHALLOW_PARSE")
        testarr = [6, 10]
        self.assertEqual(s.getEndPos(), testarr)

    def test_Score(self):
        s = CgPipeliner("Hello,  how are you.\n\n\n I am doing fine",
                        "POS,LEMMA,PARSE_STANFORD,QUANTITIES,NER_CONLL,DEPENDENCY_STANFORD,SHALLOW_PARSE")
        self.assertEqual(s.getScore(), 1.0)

class TestView(TestCase):

    def test_ViewType(self):
        s = CgPipeliner("Hello,  how are you.\n\n\n I am doing fine",
                        "POS,LEMMA,PARSE_STANFORD,QUANTITIES,NER_CONLL,DEPENDENCY_STANFORD,SHALLOW_PARSE")
        self.assertEqual(s.viewDict["POS"].getViewType(), "TokenLabelView")
        self.assertEqual(s.viewDict["PARSE_STANFORD"].getViewType(), "TreeView")

    def test_Relations(self):
        s = CgPipeliner("Hello,  how are you.\n\n\n I am doing fine",
                        "POS,LEMMA,PARSE_STANFORD,QUANTITIES,NER_CONLL,DEPENDENCY_STANFORD,SHALLOW_PARSE")
        relationArray = ['discourse', 'advmod', 'cop', 'nsubj', 'aux', 'dobj']
        self.assertEqual(s.viewDict["DEPENDENCY_STANFORD"].getRelations(), relationArray)
