# -*- coding: utf-8 -*-

import unittest
import sys
import os
import six

if six.PY2:
    import mock
else:
    import unittest.mock as mock

import ccg_nlpy
#from ccg_nlpy import remote_pipeline

PYTHONMAJORVERSION = sys.version_info[0]


class TestRemotePipeline(unittest.TestCase):
    def setUp(self):
        self.lp = ccg_nlpy.remote_pipeline.RemotePipeline()

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

    @mock.patch('ccg_nlpy.remote_pipeline.requests')
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

    # def test_unicode(self):
    #     ta = self.lp.doc("Édgar Ramírez")
    #
    #     tokens = ['Édgar', 'Ramírez']
    #     self.assertEqual(ta.get_tokens, tokens)
    #
    #     self.assertEqual(ta.get_text, "Édgar Ramírez")

    def test_doc_illigal_characters(self):
        ta = self.lp.doc("Hillary Clinton\'s Candidacy Reveals Generational Schism Among Women https://t.co/6u3lmN7nIL Édgar Ramírez")

        tokens_py2 = [u'Hillary', u'Clinton', u"'s", u'Candidacy', u'Reveals',
                      u'Generational', u'Schism', u'Among', u'Women',
                      u'https://t.co/6u3lmN7nIL', u'\xc9dgar', u'Ram\xedrez']

        tokens_py3 = ['Hillary', 'Clinton', "'s", 'Candidacy', 'Reveals',
                      'Generational', 'Schism', 'Among', 'Women',
                      'https://t.co/6u3lmN7nIL', 'Édgar', 'Ramírez']


        print("NITISH")

        if PYTHONMAJORVERSION <= 2:
            self.assertEqual(ta.get_tokens, tokens_py2)
        else:
            self.assertEqual(ta.get_tokens, tokens_py3)

        # self.assertEqual(ta.get_text,
        #                  "Hillary Clinton\'s Candidacy Reveals Generational Schism Among Women https://t.co/6u3lmN7nIL")
