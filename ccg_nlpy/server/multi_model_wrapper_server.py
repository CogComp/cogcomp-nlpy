from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from typing import List
from ccg_nlpy.pipeline_base import PipelineBase

from ccg_nlpy.server.annotator import Annotator

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from ccg_nlpy.core.text_annotation import TextAnnotation
import json
from flask import request


class MultiModelWrapperServer:
    """
    Multilingual counterpart of ModelWrapper Server. Use this to serve multiple related models.
    For example, you can serve a POS tagger in languages A,B,C... simultaneously using this wrapper.
    """

    def __init__(self, models: List[Annotator]):
        self.models = models
        # all models should have the same set of required views
        self.required_views = models[0].get_required_views()
        self.provided_views = [m.get_view_name() for m in models]
        print("provided views", self.provided_views)

        # for each viewname (e.g. POS_Arabic) know which model to call (Arabic_POS_Tagger)
        self.view2model_dict = {}
        for m in self.models:
            m.load_params()
            self.view2model_dict[m.get_view_name()] = m

        # We need a pipeline to create views that are required by our model (e.g. NER is needed for WIKIFIER etc.)
        self.pipeline = self.get_pipeline_instance()
        logging.info("required views: %s", self.get_required_views())
        logging.info("provided views: %s", self.get_provided_views())
        logging.info("ready!")

    def get_required_views(self) -> List[str]:
        return self.required_views

    def get_provided_views(self) -> List[str]:
        return self.provided_views

    def annotate(self):
        # we get something like "?text=<text>&views=<views>". Below two lines extract these.
        text = request.args.get('text')
        views = request.args.get('views')
        logging.info("request args views:%s", views)
        if text is None or views is None:
            return "The parameters 'text' and/or 'views' are not specified. Here is a sample input: ?text=\"This is a " \
                   "sample sentence. I'm happy.\"&views=POS,NER "
        views = views.split(",")

        for view in views:
            if view in self.provided_views:
                # create a text ann with the required views for the model
                docta = self.get_text_annotation_for_model(text=text, required_views=self.required_views)
                # select the correct model
                relevant_model = self.view2model_dict[view]
                # send it to your model for inference
                docta = relevant_model.add_view(docta=docta)
                # make the returned text ann to a json
                ta_json = json.dumps(docta.as_json)
                # print("returning", ta_json)
                return ta_json
        # If we reached here, it means the requested view cannot be provided by this annotator
        return "VIEW NOT PROVIDED"

    def get_pipeline_instance(self) -> PipelineBase:
        """
        Creates a pipeline instance (either local or remote pipeline) to get the views required by the model.
        :return: PipelineBase object (LocalPipeline or RemotePipeline)
        """
        raise NotImplementedError

    def get_text_annotation_for_model(self, text: str, required_views: List[str]) -> TextAnnotation:
        """
        This takes text from the annotate api call and creates a text annotation with the views required by the model.
        :param text: text from the demo interface, coming through the annotate request call
        :param required_views: views required by the model
        :return: text annotation, to be sent to the model's inference on ta method
        """
        raise NotImplementedError
