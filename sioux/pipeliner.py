import json
import requests
from backports.configparser import RawConfigParser
import os 

from .core.text_annotation import *

class Pipeliner:
    '''
    Constructor of the pipeliner to setup the api address of pipeline server
    '''
    def __init__(self):
        config = RawConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config.read(dir_path + '/../config/pipeline.cfg')
        self.url = config.get('PipelineServer', 'api')

    '''
    Initialize text annotation of given text
    @param: text, the text to be processed
    @return: TextAnnotation instance of the text
    '''
    def text_annotation(self, text="Hello World"):
        response = self.call_server(text, "POS")
        text_annotation = TextAnnotation(response)
        return text_annotation

    '''
    Wrappers on getting general information about the given text annotation
    @param: text_annotation, TextAnnotation instance to get infromation from
    @return: correspoing information
    '''
    def get_text(self, text_annotation):
        return text_annotation.get_text()

    def get_tokens(self, text_annotation):
        return text_annotation.get_tokens()

    def get_score(self, text_annotation):
        return text_annotation.get_score()

    def get_end_pos(self, text_annotation):
        return text_annotation.get_end_pos()


    '''
    Wrapper on getting part-of-speech tagger from given text annotation
    @param: text_annotation, TextAnnotation instance to get POS tagger from
    @return: View instance of POS tagger
    '''
    def pos_tag(self, text_annotation):
        return self.get_view(text_annotation, "POS")

    '''
    Wrapper on getting the dependency from given text annotation
    @param: text_annotation, TextAnnotation instance to get dependency view from
    @return: View instance of the dependency
    '''
    def dependency_parser(self, text_annotation):
        return self.get_view(text_annotation, "DEPENDENCY_STANFORD")

    '''
    Function to get user specified view from given text annotation
    @param: text_annotation, the TextAnnotation instance to get view from
            view_name, the specified view name for sending to pipeline server
    @return: View instance of the requested view
    '''
    def get_view(self, text_annotation, view_name):
        view = text_annotation.get_view(view_name)
        if view is None:
            additional_response = self.call_server(text_annotation.get_text(), view_name)
            return text_annotation.add_view(view_name, additional_response)
        return view

    '''
    Funtion to get preprocess text annotation from server
    @param: text, the text to generate text annotation on
            views, the views to generate
    @return: raw text of the response from server
    '''
    def call_server(self, text, views):
        data = {'text': text, 'views': views}
        return requests.post(self.url, data).text
