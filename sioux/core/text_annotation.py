import json
import logging

from .view import *
from .predicate_argument_view import *

logger = logging.getLogger(__name__)

class TextAnnotation(object):
    '''
        This class is was designed to be a python version of the TextAnnotation class.
        While most of the queries on view are done with View by querying on
        The JSON format of the Text Annotation (since the JSON string obtained from SerializationHelper
         is the same as the JSON format returned from web server)

    '''

    def __init__(self, json_str=None, pipeline_instance=None):
        result_json = json.loads(json_str)

        self.pipeline = pipeline_instance

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

    @property 
    def get_pos(self):
        """
        Wrapper on getting part-of-speech tagger from given text annotation
        @param: text_annotation, TextAnnotation instance to get POS tagger from
        @return: View instance of POS tagger
        """
        return self.get_view("POS")

    @property
    def get_dependency_parse(self):
        """
        Wrapper on getting the dependency from given text annotation
        @param: text_annotation, TextAnnotation instance to get dependency view from
        @return: View instance of the dependency
        """
        return self.get_view("DEPENDENCY")

    @property
    def get_stanford_dependency_parse(self):
        """
        Wrapper on getting the dependency from given text annotation
        @param: text_annotation, TextAnnotation instance to get dependency view from
        @return: View instance of the dependency
        """
        return self.get_view("DEPENDENCY_STANFORD")

    @property
    def get_ner_conll(self):
        """
        Wrapper on getting the NER_CONLL view from given text annotation
        @param: text_annotation TextAnnotation instance to get NER_CONLL view from.
        @return: View Instance of the NER_CONLL view.
        """
        return self.get_view("NER_CONLL")

    @property 
    def get_ner_ontonotes(self):
        """
        Wrapper on getting the NER_ONTONOTES view from given text annotation
        @param: text_annotation TextAnnotation instance to get NER_ONTONOTES view from.
        @return: View Instance of the NER_ONTONOTES view.
        """
        return self.get_view("NER_ONTONOTES")

    @property 
    def get_stanford_parse(self):
        """
        Wrapper on getting the PARSE_STANFORD view from given text annotation
        @param: text_annotation TextAnnotation instance to get PARSE_STANFORD view from.
        @return: View Instance of the PARSE_STANFORD view.
        """
        return self.get_view("PARSE_STANFORD")

    @property 
    def get_srl_verb(self):
        """
        Wrapper on getting the SRL_VERB view from given text annotation
        @param: text_annotation TextAnnotation instance to get SRL_VERB view from.
        @return: View Instance of the SRL_VERB view.
        """
        return self.get_view("SRL_VERB")

    @property 
    def get_srl_nom(self):
        """
        Wrapper on getting the SRL_NOM view from given text annotation
        @param: text_annotation TextAnnotation instance to get SRL_NOM view from.
        @return: View Instance of the SRL_NOM view.
        """
        return self.get_view("SRL_NOM")

    @property
    def get_srl_prep(self):
        """
        Wrapper on getting the SRL_PREP view from given text annotation
        @param: text_annotation TextAnnotation instance to get SRL_PREP view from.
        @return: View Instance of the SRL_PREP view.
        """
        return self.get_view("SRL_PREP")

    @property
    def get_srl_comma(self):
        """
        Wrapper on getting the SRL_COMMA view from given text annotation
        @param: text_annotation TextAnnotation instance to get SRL_COMMA view from.
        @return: View Instance of the SRL_COMMA view.
        """
        return self.get_view("SRL_COMMA")

    @property 
    def get_quantities(self):
        """
        Wrapper on getting the QUANTITIES view from given text annotation
        @param: text_annotation TextAnnotation instance to get QUANTITIES view from.
        @return: View Instance of the QUANTITIES view.
        """
        return self.get_view("QUANTITIES")

    @property 
    def get_shallow_parse(self):
        """
        Wrapper on getting the SHALLOW_PARSE view from given text annotation
        @param: text_annotation TextAnnotation instance to get SHALLOW_PARSE view from.
        @return: View Instance of the SHALLOW_PARSE view.
        """
        return self.get_view("SHALLOW_PARSE")

    @property 
    def get_lemma(self):
        """
        Wrapper on getting the LEMMA view from given text annotation
        @param: text_annotation TextAnnotation instance to get LEMMA view from.
        @return: View Instance of the LEMMA view.
        """
        return self.get_view("LEMMA")

    def add_view(self, view_name, response):
        result_json = json.loads(response)

        # check if the view is retrieve correctly
        # iterate through all the views presented in response, add the view that hasn't been store,
        # return the view requested
        requested_view = None
        view_constituents = []
        for view in result_json["views"]:
            name = view["viewName"]
            view_constituents.append(name)
            if name not in self.view_dictionary:
                self.view_dictionary[name] = self._view_builder(view)

            if name == view_name:
                requested_view = self.view_dictionary[name]
        
        if requested_view is None:
            # "token" view will always be included
            if len(view_constituents) <= 1:
                print("Invalid view name, please check.")
            else:
                logger.info("The view is the collection of the following views: {0}".format(view_constituents))
                self.view_dictionary[name] = view_constituents
        return requested_view

    def get_view(self, view_name):
        if view_name not in self.view_dictionary:
            additional_response = self.pipeline.call_server(self.text, view_name)
            self.add_view(view_name, additional_response)

        if type(self.view_dictionary[view_name]) != type([]):
            return self.view_dictionary[view_name]
        else:
            logger.info("The view is the collection of the following views: {0}".format(self.view_dictionary[view_name]))
            return None

    @property
    def get_views(self):
        return list(self.view_dictionary.keys())

    # Functions to get general information about the text annotation

    @property
    def get_text(self):
        return self.text

    @property
    def get_tokens(self):
        return self.tokens

    @property
    def get_score(self):
        return self.score

    @property
    def get_sentence_end_token_indices(self):
        return self.sentence_end_position
