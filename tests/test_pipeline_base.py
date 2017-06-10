import unittest
import sys
import os
import codecs

# import local_pipeline module here because PipelineBase is an abstract class
# and creating an instance of abstract class is not allowed

from ccg_nlpy import remote_pipeline

class TestPipelineBase(unittest.TestCase):
    def test_user_config(self):
        test_config_folder = os.path.dirname(os.path.realpath(__file__))

        with codecs.open(test_config_folder+'/config.cfg',mode='w',encoding='utf-8') as f:
            f.write(
'''
[remote_pipeline_setting]
api = someaddress
''')

        rp = remote_pipeline.RemotePipeline(file_name=test_config_folder+'/config.cfg')
        self.assertEqual("someaddress",rp.url)

