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
        @return: TextAnnotation instance of the text, None if text is empty
        """
        response = self.call_server(text, "TOKENS")
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
