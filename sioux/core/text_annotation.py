import json
import logging

from .view import *
from .predicate_argument_view import *

logger = logging.getLogger(__name__)

'''
    For now, this class is implemented as an indirect type
    All the functions can (should) be called indirectly by functions in Pipeliner class
'''


class TextAnnotation:
    '''
        This class is was designed to be a python version of the TextAnnotation class.
        While most of the queries on view are done with View by querying on
        The JSON format of the Text Annotation (since the JSON string obtained from SerializationHelper
         is the same as the JSON format returned from web server)

    '''

    def __init__(self, json_str=None):
        # Adopted Ani's code 
        result_json = json.loads(json_str)

        self.text = result_json["text"]
        self.tokens = result_json["tokens"]
        self.score = result_json["sentences"]["score"]
        self.sentence_end_position = result_json["sentences"][
            "sentenceEndPositions"]

        self.view_dictionary = {}
        for view in result_json["views"]:
            self.view_dictionary[view["viewName"]] = self._view_builder(view)

    def _view_builder(self, view):
        full_type = view["viewData"][0]["viewType"]
        split_by_period = full_type.split(".")
        view_type = split_by_period[len(split_by_period) - 1]
        if view_type == 'PredicateArgumentView':
            return PredicateArgumentView(view, self.tokens)
        else: 
            return View(view, self.tokens)

    # Functions to manipulate the views on text annotation

    def add_view(self, view_name, response):
        result_json = json.loads(response)

        # check if the view is retrieve correctly
        # iterate through all the views presented in response, add the view that hasn't been store,
        # return the view requested
        view_constituents = []
        for view in result_json["views"]:
            name = view["viewName"]
            view_constituents.append(name)
            if view["viewName"] not in self.view_dictionary:
                self.view_dictionary[name] = self._view_builder(view)
        
        requested_view = self.get_view(view_name)
        if requested_view is None:
            # "token" view will always be included
            if len(view_constituents) <= 1:
                print("Invalid view name, please check.")
            else:
                logger.info("The view is the collection of the following views: {0}".format(view_constituents))
                self.view_dictionary[name] = view_constituents
        return requested_view

    def get_view(self, view_name):
        if view_name in self.view_dictionary:
            if type(self.view_dictionary[view_name]) != type([]):
                return self.view_dictionary[view_name]
            else:
                logger.info("The view is the collection of the following views: {0}".format(self.view_dictionary[view_name]))
                return None
        else:
            return None

    def get_views(self):
        return list(self.view_dictionary.keys())

    # Functions to get general information about the text annotation

    def get_text(self):
        return self.text

    # Ani's code
    def get_tokens(self):
        return self.tokens

    def get_score(self):
        return self.score

    def get_sentence_end_token_indices(self):
        return self.sentence_end_position
