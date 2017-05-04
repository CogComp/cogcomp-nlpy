import unittest
import sys
import os
import six
import codecs

if six.PY2:
    import mock
else:
    import unittest.mock as mock

#sys.path.insert(0,'/path/to/mod_directory')
import sioux

test_config_folder = os.path.dirname(os.path.realpath(__file__))

class TestPipelineConfig(unittest.TestCase):

    def setUp(self):
        with codecs.open(test_config_folder+'/config.cfg',mode='w',encoding='utf-8') as f:
            f.write(
'''
[remote_pipeline_setting]
api = http://austen.cs.illinois.edu:7080
''')

    @mock.patch('sioux.pipeline_config.download')
    def test_get_current_config_without_models(self, mock_dl):
        mock_dl.get_model_path.return_value = 'not_exists_folder_path'
        config, models = sioux.pipeline_config.get_current_config()
        self.assertEqual(False, models)
        self.assertEqual(config['remote_pipeline_setting']['api'], 'http://austen.cs.illinois.edu:8080')

    @mock.patch('sioux.pipeline_config.download')
    def test_get_current_config_with_models(self, mock_dl):
        mock_dl.get_root_directory.return_value = test_config_folder
        mock_dl.get_model_path.return_value = test_config_folder
        config, models = sioux.pipeline_config.get_current_config()
        self.assertEqual(True, models)
        self.assertEqual(config['remote_pipeline_setting']['api'], 'http://austen.cs.illinois.edu:7080')

    @mock.patch('sioux.pipeline_config.download')
    def test_get_user_config(self, mock_dl):
        # such that will use package config if user provided file does not exist
        mock_dl.get_model_path.return_value = 'not_exists_folder_path'
        config, models = sioux.pipeline_config.get_user_config(test_config_folder+'/config.cfg')
        self.assertEqual(config['remote_pipeline_setting']['api'], 'http://austen.cs.illinois.edu:7080')

        # try provided not exist file name
        config, pack = sioux.pipeline_config.get_user_config('super_strange_file_name')
        self.assertEqual(config['remote_pipeline_setting']['api'], 'http://austen.cs.illinois.edu:8080')

    @mock.patch('sioux.pipeline_config.download')
    def test_change_temporary_config(self,mock_dl):
        mock_dl.get_root_directory.return_value = test_config_folder
        mock_dl.get_model_path.return_value = test_config_folder

        config, models = sioux.pipeline_config.get_user_config(test_config_folder+'/config.cfg')
        self.assertEqual(config['remote_pipeline_setting']['api'], 'http://austen.cs.illinois.edu:7080')
        sioux.pipeline_config.change_temporary_config(config, models, False, 'another_address')
        self.assertEqual(models, True)
        self.assertEqual(config['remote_pipeline_setting']['api'], 'another_address')

    def tearDown(self):
        if os.path.exists(test_config_folder+'/config.cfg'):
            os.remove(test_config_folder+'/config.cfg')
