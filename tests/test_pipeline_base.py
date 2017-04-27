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
[pipeline_setting]
use_pipeline_server = false
[views_setting]
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
[pipeline_server]
api = http://austen.cs.illinois.edu:8080/annotate
''')

        self.lp = local_pipeline.LocalPipeline(file_name=test_config_folder+'/config.cfg')
        doc = self.lp.doc("Testing text.")
        pos = self.lp.get_pos(doc)
        lemma = self.lp.get_lemma(doc)
        srl_verb = self.lp.get_srl_verb(doc)
        self.assertEqual(False, pos is None)
        self.assertEqual(False, lemma is None)
        self.assertEqual(True, srl_verb is None)
