import json
import requests
import sys
import os
import logging

from abc import ABCMeta, abstractmethod
from backports.configparser import RawConfigParser

from .core.text_annotation import *
from .download import get_model_path
from . import pipeline_config

logger = logging.getLogger(__name__)

class PipelineBase:
    __metaclass__ = ABCMeta

    def __init__(self, file_name = None):
        """
        Constructor to load configuration of the pipeline base
        """
        if file_name is not None:
            self.config, self.models_downloaded = pipeline_config.get_user_config(file_name)
        else:
            self.config, self.models_downloaded = pipeline_config.get_current_config()


    def doc(self, text="Hello World", pretokenized=False):
        """
        Initialize text annotation of given text

        @param: text, the text to be processed
        @return: TextAnnotation instance of the text, None if text is empty
        """
        if not pretokenized:
            response = self.call_server(text, "TOKENS")

        else:
            response = self.call_server_pretokenized(text, "TOKENS")

        if response is not None:
            return TextAnnotation(response, self)
        else:
            return None


    @abstractmethod
    def call_server(text, views):
        """
        Funtion to get preprocess text annotation from server

        @param: text, the text to generate text annotation on
                views, the views to generate
        @return: raw text of the response from server
        """
        logger.error("This function should be overrided.")
        #raise NotImplementedError()
        return None


    @abstractmethod
    def call_server_pretokenized(pretokenized_text, views):
        """
        Funtion to get preprocess text annotation from server

        @param: pretokenized_text, list of list of tokens of pre-tokenized text
        @return: raw text of the response from server
        """
        logger.error("This function should be overrided.")
        #raise NotImplementedError()
        return None



    @abstractmethod
    def add_additional_views_to_TA(self, textannotation, views):
        """
        Funtion to add additional views to an existing TextAnnotation

        @param: textannotation, the python TA object
                views, the views to generate
        @return: raw text of the response from server -- jsonStr
        """
        logger.error("This function should be overrided.")
        #raise NotImplementedError()
        return None
