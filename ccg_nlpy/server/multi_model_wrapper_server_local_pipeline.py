from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from ccg_nlpy.server.multi_model_wrapper_server import MultiModelWrapperServer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from ccg_nlpy import local_pipeline
from ccg_nlpy.core.text_annotation import TextAnnotation


class MultiModelWrapperServerLocal(MultiModelWrapperServer):
    def __init__(self, models):
        super().__init__(models)

    def get_pipeline_instance(self):
        return local_pipeline.LocalPipeline()

    def get_text_annotation_for_model(self, text, required_views):
        pretokenized_text = [text.split(" ")]
        required_views = ",".join(required_views)
        ta_json = self.pipeline.call_server_pretokenized(pretokenized_text=pretokenized_text, views=required_views)
        ta = TextAnnotation(json_str=ta_json)
        return ta
