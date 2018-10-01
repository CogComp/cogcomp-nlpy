from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import sys
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import argparse
from flask import Flask, flash, redirect, render_template, request, session, abort
from ccg_nlpy import local_pipeline
from ccg_nlpy import remote_pipeline
from ccg_nlpy.core.text_annotation import TextAnnotation
import copy
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
# necessary for testing on localhost
CORS(app)


class DummyModel:
    def __init__(self):
        pass

    def load_params(self):
        logging.info("loading model params ...")
        logging.info("required views: %s", self.required_views())
        logging.info("provides view: %s", self.get_view_name())

    def required_views(self):
        return ["TOKENS", "NER_CONLL"]

    def get_view_name(self):
        provided_view_name = "DUMMYVIEW"
        return provided_view_name

    def inference_on_ta(self, docta, new_view_name):
        # This upcases each token. Test for TokenLabelView
        # new_view = copy.deepcopy(docta.get_view("TOKENS"))
        # tokens = docta.get_tokens
        # for token, cons in zip(tokens, new_view.cons_list):
        #     cons["label"] = token.upper()

        # This replaces each NER with its upcased tokens. Test for SpanLabelView
        new_view = copy.deepcopy(docta.get_view("NER_CONLL"))
        for nercons in new_view.cons_list:
            nercons["label"] = nercons["tokens"].upper()
        new_view.view_name = new_view_name
        docta.view_dictionary[new_view_name] = new_view
        return docta


class ServerWrapper:
    def __init__(self, model):
        self.model = model
        self.provided_view = model.get_view_name()
        # right now, we let call the initialization inside the init of server
        # this could have been done outside. Cannot say which is a better choice.
        self.model.load_params()
        # We need a pipeline to create views that are required by our model (e.g. NER is needed for WIKIFIER etc.)
        self.pipeline = remote_pipeline.RemotePipeline()
        logging.info("ready!")

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
        required_views = ",".join(model.required_views())
        ta_json = self.pipeline.call_server(text=text, views=required_views)
        docta = TextAnnotation(json_str=ta_json)
        # send it to your model for inference
        docta = self.model.inference_on_ta(docta=docta, new_view_name=self.provided_view)
        # make the returned text ann to a json
        ta_json = json.dumps(docta.as_json)
        # print("returning", ta_json)
        return ta_json


if __name__ == "__main__":
    model = DummyModel()  # create your model object here
    wrapper = ServerWrapper(model=model)
    app.add_url_rule(rule='/annotate', endpoint='annotate', view_func=wrapper.annotate, methods=['GET'])
    app.run(host='localhost', port=5000)
