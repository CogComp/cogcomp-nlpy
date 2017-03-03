import unittest

from cogcomp_python_utils.pyjnius_pipeline_wrapper.pipeline_factory import CgPipeline

class TestPipelineWrapper(unittest.TestCase):
    def test_constructor_without_path(self):
        p = CgPipeline()
        self.assertTrue(isinstance(p.pipeline, basestring))

    def test_constructor_with_path(self):
        jar_paths = ['/home/GHLgh/pipeline/illinois-nlp-pipeline-0.1.25/dist/*','/home/GHLgh/pipeline/illinois-nlp-pipeline-0.1.25/lib/*']
        config_path = '/home/GHLgh/pipeline/illinois-nlp-pipeline-0.1.25/config/pipeline-config.properties'
        p = CgPipeline(jar_paths)
        self.assertTrue(p.pipeline != None)
        q = CgPipeline(jar_paths, config_path)
        self.assertTrue(type(p) == type(q))

    def test_run_pipeline(self):
        jar_paths = ['/home/GHLgh/pipeline/illinois-nlp-pipeline-0.1.25/dist/*','/home/GHLgh/pipeline/illinois-          ne-0.1.25/lib/*']
        config_path = '/home/GHLgh/pipeline/illinois-nlp-pipeline-0.1.25/config/pipeline-config.properties'
        p = CgPipeline(jar_paths, config_path)
        ta = p.run_pipeline()
        self.assertTrue(ta != None)

if __name__ == '__main__':
    unittest.main()
