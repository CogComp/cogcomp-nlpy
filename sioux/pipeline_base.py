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


    def doc(self, text="Hello World"):
        """
        Initialize text annotation of given text

        @param: text, the text to be processed
        @return: TextAnnotation instance of the text
        """
        response = self.call_server(text, "TOKENS")
        text_annotation = TextAnnotation(response, self)
        return text_annotation


    def is_view_enabled(self, view_name):
        """
        Function to check if specified view is enabled
    
        @param:  view_name, the specified view name to check if it is enabled
        @return: View instance of the requested view
        """
        if pipeline_config.view_enabled(self.config, view_name) == False:
            logger.error('{} not defined or disabled.'.format(view_name))
            return False
        else:
            return True

    def test(self):
        return type(self)

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
