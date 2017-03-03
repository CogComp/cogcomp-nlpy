import unittest

import cogcomp_python_utils

class TestSample(unittest.TestCase):
    def test_is_string(self):
        s = cogcomp_python_utils.sample()
        self.assertTrue(isinstance(s, basestring))

if __name__ == '__main__':
    unittest.main() 
