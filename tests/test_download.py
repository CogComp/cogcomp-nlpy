import unittest
import sys
import os
import codecs

from ccg_nlpy import download

test_config_folder = os.path.dirname(os.path.realpath(__file__))

class TestDownload(unittest.TestCase):
    def test_recover_model_config(self):
        if os.path.exists(test_config_folder+'/config.cfg'):
            os.remove(test_config_folder+'/config.cfg')
        download.get_root_directory = lambda : test_config_folder
        self.assertEqual(os.path.exists(test_config_folder+'/config.cfg'),False)
        download.recover_model_config()
        self.assertEqual(os.path.exists(test_config_folder+'/config.cfg'),True) 

    def tearDown(self):
        if os.path.exists(test_config_folder+'/config.cfg'):
            os.remove(test_config_folder+'/config.cfg')
