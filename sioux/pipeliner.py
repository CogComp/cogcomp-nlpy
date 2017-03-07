import json
import requests
import os 

from backports.configparser import RawConfigParser

from .core.text_annotation import *

class Pipeliner(object):
    """
    Constructor of the pipeliner to setup the api address of pipeline server
    """

    def __init__(self):
        config = RawConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.read(dir_path + '/../config/pipeline.cfg')
        self.url = config.get('PipelineServer', 'api')

    def doc(self, text="Hello World"):
        """
        Initialize text annotation of given text

        @param: text, the text to be processed
        @return: TextAnnotation instance of the text
        """
        response = self.call_server(text, "POS")
        text_annotation = TextAnnotation(response)
        return text_annotation

    def get_text(self, text_annotation):
        """
        Wrappers on getting general information about the given text annotation

        @param: text_annotation, TextAnnotation instance to get infromation from
        @return: correspoing information
        """
        return text_annotation.get_text()

    def get_tokens(self, text_annotation):
        return text_annotation.get_tokens()

    def get_score(self, text_annotation):
        return text_annotation.get_score()

    def get_end_pos(self, text_annotation):
        return text_annotation.get_end_pos()

    def get_pos(self, text_annotation):
        """
        Wrapper on getting part-of-speech tagger from given text annotation

        @param: text_annotation, TextAnnotation instance to get POS tagger from
        @return: View instance of POS tagger
        """
        return self.get_view(text_annotation, "POS")

    def get_dependency_parse(self, text_annotation):
        """
        Wrapper on getting the dependency from given text annotation

        @param: text_annotation, TextAnnotation instance to get dependency view from
        @return: View instance of the dependency
        """
        return self.get_view(text_annotation, "DEPENDENCY_STANFORD")

    def get_ner_conll(self, text_annotation):
        """
        Wrapper on getting the NER_CONLL view from given text annotation

        @param: text_annotation TextAnnotation instance to get NER_CONLL view from.
        @return: View Instance of the NER_CONLL view.
        """
        return self.get_view(text_annotation, "NER_CONLL")

    def get_ner_ontonotes(self, text_annotation):
        """
        Wrapper on getting the NER_ONTONOTES view from given text annotation

        @param: text_annotation TextAnnotation instance to get NER_ONTONOTES view from.
        @return: View Instance of the NER_ONTONOTES view.
        """
        return self.get_view(text_annotation, "NER_ONTONOTES")

    def get_stanford_parse(self, text_annotation):
        """
        Wrapper on getting the PARSE_STANFORD view from given text annotation

        @param: text_annotation TextAnnotation instance to get PARSE_STANFORD view from.
        @return: View Instance of the PARSE_STANFORD view.
        """
        return self.get_view(text_annotation, "PARSE_STANFORD")

    def get_srl_verb(self, text_annotation):
        """
        Wrapper on getting the SRL_VERB view from given text annotation

        @param: text_annotation TextAnnotation instance to get SRL_VERB view from.
        @return: View Instance of the SRL_VERB view.
        """
        return self.get_view(text_annotation, "SRL_VERB")

    def get_srl_nom(self, text_annotation):
        """
        Wrapper on getting the SRL_NOM view from given text annotation

        @param: text_annotation TextAnnotation instance to get SRL_NOM view from.
        @return: View Instance of the SRL_NOM view.
        """
        return self.get_view(text_annotation, "SRL_NOM")

    def get_quantities(self, text_annotation):
        """
        Wrapper on getting the QUANTITIES view from given text annotation

        @param: text_annotation TextAnnotation instance to get QUANTITIES view from.
        @return: View Instance of the QUANTITIES view.
        """
        return self.get_view(text_annotation, "QUANTITIES")

    def get_shallow_parse(self, text_annotation):
        """
        Wrapper on getting the SHALLOW_PARSE view from given text annotation

        @param: text_annotation TextAnnotation instance to get SHALLOW_PARSE view from.
        @return: View Instance of the SHALLOW_PARSE view.
        """
        return self.get_view(text_annotation, "SHALLOW_PARSE")

    def get_lemma(self, text_annotation):
        """
        Wrapper on getting the LEMMA view from given text annotation

        @param: text_annotation TextAnnotation instance to get LEMMA view from.
        @return: View Instance of the LEMMA view.
        """
        return self.get_view(text_annotation, "LEMMA")


    def get_view(self, text_annotation, view_name):
        """
        Function to get user specified view from given text annotation

        @param: text_annotation, the TextAnnotation instance to get view from
                view_name, the specified view name for sending to pipeline server
        @return: View instance of the requested view
        """

        view = text_annotation.get_view(view_name)
        if view is None:
            additional_response = self.call_server(text_annotation.get_text(), view_name)
            return text_annotation.add_view(view_name, additional_response)
        return view


    def call_server(self, text, views):
        """
         Funtion to get preprocess text annotation from server

        @param: text, the text to generate text annotation on
                views, the views to generate
        @return: raw text of the response from server
        """
        data = {'text': text, 'views': views}
        return requests.post(self.url, data).text
