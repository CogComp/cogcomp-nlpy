import unittest
import sys
import os
import codecs

# import local_pipeline module here because PipelineBase is an abstract class
# and creating an instance of abstract class is not allowed

from sioux import local_pipeline
if os.path.exists('annotation-cache'):
    os.remove('annotation-cache')

class TestPipelineBase(unittest.TestCase):
    def test_user_config(self):
        test_config_folder = os.path.dirname(os.path.realpath(__file__))

        with codecs.open(test_config_folder+'/config.cfg',mode='w',encoding='utf-8') as f:
            f.write(
'''
[local_pipeline_setting]
POS = true
LEMMA = true
NER_CONLL = false
NER_ONTONOTES = false
QUANTITIES = false
SHALLOW_PARSE = false
SRL_VERB = false
DEPENDENCY_STANFORD = false
DEPENDENCY = false
PARSE_STANFORD = false
SRL_PREP = false
[remote_pipeline_setting]
api = http://austen.cs.illinois.edu:8080
''')

        lp = local_pipeline.LocalPipeline(file_name=test_config_folder+'/config.cfg')

        doc = lp.doc("Testing text.")

        pos = doc.get_pos
        lemma = doc.get_lemma
        srl_verb = doc.get_srl_verb
        self.assertEqual(False, pos is None)
        self.assertEqual(False, lemma is None)
        self.assertEqual(True, srl_verb is None)

        self.assertEqual(True, lp.is_view_enabled("POS"))
        self.assertEqual(True, lp.is_view_enabled("LEMMA"))
        self.assertEqual(False, lp.is_view_enabled("SRL_VERB"))
