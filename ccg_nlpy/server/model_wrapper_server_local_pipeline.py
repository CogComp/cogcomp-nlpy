from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from ccg_nlpy.server.model_wrapper_server import ModelWrapperServer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from ccg_nlpy import local_pipeline


class ModelWrapperServerLocal(ModelWrapperServer):
    def __init__(self, model, provided_view, required_views):
        super().__init__(model, provided_view, required_views)

    def get_pipeline_instance(self):
        return local_pipeline.LocalPipeline()

    def get_text_annotation_for_model(self, text, required_views):
        pretokenized_text = [text.split(" ")]
        ta_json = self.pipeline.call_server_pretokenized(pretokenized_text=pretokenized_text, views=required_views)
        return ta_json


