import unittest

from cogcomp_python_utils.pyjnius_pipeline_wrapper.pipeline_factory import CgPipeline
from cogcomp_python_utils.pyjnius_pipeline_wrapper.text_annotation import TextAnnotation
from cogcomp_python_utils.pyjnius_pipeline_wrapper.CgView import CgView

jar_paths = ['/home/GHLgh/pipeline/illinois-nlp-pipeline-0.1.25/dist/*','/home/GHLgh/pipeline/illinois-nlp-pipeline-0.1.25/lib/*']
config_path = '/home/GHLgh/pipeline/illinois-nlp-pipeline-0.1.25/config/pipeline-config.properties'
p = CgPipeline(jar_paths, config_path)
ta = p.run_pipeline()

class TestTextAnnotation(unittest.TestCase):
    def test_constructor(self):
        self.assertTrue(len(ta.views) > 0)
        self.assertTrue(len(ta.tokens) == 2)
        self.assertTrue(ta.num_of_sentences == 1)
        self.assertTrue(isinstance(ta.viewList[0],CgView))

if __name__ == '__main__':
    unittest.main()
