from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from typing import List

from ccg_nlpy.server.abstract_model import AbstractModel
from ccg_nlpy.server.model_wrapper_server import ModelWrapperServer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from ccg_nlpy import remote_pipeline
from ccg_nlpy.core.text_annotation import TextAnnotation


class ModelWrapperServerRemote(ModelWrapperServer):
    def __init__(self, model: AbstractModel):
        super().__init__(model)

    def get_pipeline_instance(self):
        return remote_pipeline.RemotePipeline()

    def get_text_annotation_for_model(self, text: str, required_views: List[str]):
        required_views = ",".join(required_views)
        ta_json = self.pipeline.call_server(text=text, views=required_views)
        ta = TextAnnotation(json_str=ta_json)
        return ta
