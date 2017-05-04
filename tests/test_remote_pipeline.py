import unittest
import sys
import os
import six

if six.PY2:
    import mock
else:
    import unittest.mock as mock

import sioux
#from sioux import remote_pipeline


class TestRemotePipeline(unittest.TestCase):
    def setUp(self):
        self.lp = sioux.remote_pipeline.RemotePipeline()

    def test_doc(self):
        ta = self.lp.doc("Hello,  how are you.\n\n\n I am doing fine")
        tokens = [
            'Hello', ',', 'how', 'are', 'you', '.', 'I', 'am', 'doing', 'fine'
        ]
        self.assertEqual(ta.get_tokens, tokens)

        testarr = [6, 10]
        self.assertEqual(ta.get_sentence_end_token_indices, testarr)

        self.assertEqual(ta.get_score, 1.0)

        self.assertEqual(ta.get_text, "Hello,  how are you.\n\n\n I am doing fine")

    @mock.patch('sioux.remote_pipeline.requests')
    def test_status_code(self, mock_req):
        class ResponseMock(object):
            def __init__(self, code):
                self.status_code = code
            

        limit = ResponseMock(429)
        undefined_status_code = ResponseMock(233)
        mock_req.post.side_effect = [limit, undefined_status_code]
        try:
            self.lp.doc("Hello World.")
            self.fail("Should raise an exception.")
        except:
            abc = None
        try:
            self.lp.doc("Hello World.")
            self.fail("Should raise another exception.")
        except:
            abc = None

