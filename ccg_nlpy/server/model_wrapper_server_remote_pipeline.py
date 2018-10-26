from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from ccg_nlpy.server.model_wrapper_server import ModelWrapperServer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from ccg_nlpy import remote_pipeline
from ccg_nlpy import local_pipeline
from ccg_nlpy.core.text_annotation import TextAnnotation
import json
from flask import request


class ModelWrapperServerRemote(ModelWrapperServer):
    def __init__(self, model, provided_view, required_views):
        super().__init__(model, provided_view, required_views)
        # We need a pipeline to create views that are required by our model (e.g. NER is needed for WIKIFIER etc.)

    def get_pipeline_instance(self):
        return remote_pipeline.RemotePipeline()

    def get_text_annotation_for_model(self, text, required_views):
        ta_json = self.pipeline.call_server(text=text, views=required_views)
        return ta_json
