from unittest import TestCase

import cogcomp_python_utils

class TestSample(TestCase):
    def test_is_string(self):
        s = cogcomp_python_utils.sample()
        self.assertTrue(isinstance(s, basestring))
