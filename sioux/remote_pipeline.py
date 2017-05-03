import json
import requests
import sys
import os
import logging

from backports.configparser import RawConfigParser

from .pipeline_base import *
from google.protobuf import json_format
from .protobuf import TextAnnotation_pb2
from .core.text_annotation import *
from .download import get_model_path
from . import pipeline_config

WEB_SERVER_SUFFIX = '/annotate'

logger = logging.getLogger(__name__)

class RemotePipeline(PipelineBase):
    def __init__(self, server_api=None, file_name=None):
        """
        Constructor to set up remote pipeline
        """
        super(RemotePipeline,self).__init__(file_name)

        # reroute to new API if user provides one
        pipeline_config.change_temporary_config(self.config, self.models_downloaded, None, None, True, server_api)
        self.url = self.config['remote_pipeline_setting']['api']

        logger.info("pipeline has been set up")

    def is_view_enabled(self, view_name):
        """
        Override method because remote pipeline server will have all views enabled
        """
        return True


    def call_server(self, text, views):
        """
        Funtion to get preprocess text annotation from server

        @param: text, the text to generate text annotation on
                views, the views to generate
        @return: raw text of the response from server
        """
        try:
            data = {'text': text, 'views': views}
            response = requests.post(self.url+WEB_SERVER_SUFFIX, data)
            if response.status_code == 200:
                return response.text
            elif response.status_code == 429:
                logger.error("You reached maximum query limit with default remote server (100 queries/day)")
                raise
            else:
                logger.error("Unexpected status code {}, please open an issue on GitHub for further investigation.".format(response.status_code))
        except:
            logger.error("Fail to connect to server.")
            raise

    def test(self, text, views):
        data = {'text': text, 'views': views}
        try:
            response = requests.post(self.url+WEB_SERVER_SUFFIX, data)
            return response
        except:
            logger.error("Fail to connect to server")
            raise
