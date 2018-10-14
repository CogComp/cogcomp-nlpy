from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from ccg_nlpy import remote_pipeline
from ccg_nlpy.core.text_annotation import TextAnnotation
import json
from flask import request


class ModelWrapperServer:
    def __init__(self, model):
        self.model = model
        self.provided_view = "DUMMYVIEW"
        self.required_views = ["TOKENS", "NER_CONLL"]
        # right now, we let call the model load inside the init of server
        # this could have been done outside. Cannot say which is a better choice.
        # THIS NEEDS TO BE DEFINED IN THE MODEL
        self.model.load_params()
        # We need a pipeline to create views that are required by our model (e.g. NER is needed for WIKIFIER etc.)
        self.pipeline = remote_pipeline.RemotePipeline()
        logging.info("required views: %s", self.get_required_views())
        logging.info("provides view: %s", self.get_view_name())
        logging.info("ready!")

    def get_required_views(self):
        return self.required_views

    def get_view_name(self):
        return self.provided_view

    def annotate(self):
        # we get something like "?text=<text>&views=<views>". Below two lines extract these.
        text = request.args.get('text')
        views = request.args.get('views')
        if text is None or views is None:
            return "The parameters 'text' and/or 'views' are not specified. Here is a sample input: ?text=\"This is a " \
                   "sample sentence. I'm happy.\"&views=POS,NER "
        views = views.split(",")
        if self.provided_view not in views:
            logging.info("desired view not provided by this server.")
            # After discussing with Daniel, this is the proper discipline to handle views not provided by this.
            # The appelles server will fallback to the next remote server.
            return "VIEW NOT PROVIDED"
        # create a text ann with the required views for the model
        required_views = ",".join(self.get_required_views())
        ta_json = self.pipeline.call_server(text=text, views=required_views)
        docta = TextAnnotation(json_str=ta_json)
        # send it to your model for inference
        docta = self.model.inference_on_ta(docta=docta, new_view_name=self.provided_view)
        # make the returned text ann to a json
        ta_json = json.dumps(docta.as_json)
        # print("returning", ta_json)
        return ta_json


