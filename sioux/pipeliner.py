import json
import requests
import sys
import os
import logging

#use for checking Java version
import re
import subprocess

from backports.configparser import RawConfigParser

from .core.text_annotation import *
from .download import get_model_path
from . import pipeline_config

REQUIRED_JAVA_VERSION = 1.8
WEB_SERVER_SUFFIX = '/annotate'

logger = logging.getLogger(__name__)

"""
Constructor of the pipeliner to setup the api address of pipeline server
"""
config, models_downloaded = pipeline_config.get_current_config()

# web server info
url = config['pipeline_server']['api']

# local pipeline info
pipeline = None
PipelineFactory = None
SerializationHelper = None
model_dir = get_model_path() + '/*'

import jnius_config
jnius_config.add_options('-Xmx16G')
jnius_config.add_classpath(model_dir)

pipeline_config.log_current_config(config)

def _init(enabled_views):
    global PipelineFactory
    global SerializationHelper
    global pipeline

    if pipeline is not None:
        logger.warn('Pipeline has been set up previously.')
        return

    if enabled_views is not None:
        version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
        pattern = '\"(\d+\.\d+).*\"'
        user_java_version = float(re.search(pattern, version).groups()[0])
        if user_java_version < REQUIRED_JAVA_VERSION:
            logger.error('Your Java version is {0}, it needs to be {1} or higher to run local pipeline.'.format(user_java_version, REQUIRED_JAVA_VERSION))
            return

        from jnius import autoclass
        PipelineFactory = autoclass('edu.illinois.cs.cogcomp.pipeline.main.PipelineFactory')
        SerializationHelper = autoclass('edu.illinois.cs.cogcomp.core.utilities.SerializationHelper')
        if len(enabled_views) == 0:
            pipeline = PipelineFactory.buildPipeline()
        else:
            pipeline = PipelineFactory.buildPipeline(*enabled_views)

    logger.info("pipeline has been set up")

def init(use_server = None, server_api = None, enable_views = None, disable_views = None):
    global config

    enabled_views = pipeline_config.change_temporary_config(config, models_downloaded, enable_views, disable_views, use_server, server_api)
    _init(enabled_views)


def init_from_file(file_name = None):
    global config
    global models_downloaded
    config, models_downloaded = pipeline_config.get_user_config(file_name)
    enabled_views = pipeline_config.log_current_config(config)
    
    _init(enabled_views)

def change_config(use_server = None, server_api = None, enable_views = None, disable_views = None):
    global config
    pipeline_config.change_temporary_config(config, models_downloaded, enable_views, disable_views, use_server, server_api)

def save_config():
    pipeline_config.set_current_config(config)

def show_config():
    pipeline_config.log_current_config(config)

def doc(text="Hello World"):
    """
    Initialize text annotation of given text

    @param: text, the text to be processed
    @return: TextAnnotation instance of the text
    """
    response = call_server(text, "TOKENS")
    text_annotation = TextAnnotation(response)
    return text_annotation


def get_text(text_annotation):
    """
    Wrappers on getting general information about the given text annotation

    @param: text_annotation, TextAnnotation instance to get infromation from
    @return: correspoing information
    """
    return text_annotation.get_text()


def get_tokens(text_annotation):
    return text_annotation.get_tokens()


def get_score(text_annotation):
    return text_annotation.get_score()


def get_end_pos(text_annotation):
    return text_annotation.get_end_pos()


def get_pos(text_annotation):
    """
    Wrapper on getting part-of-speech tagger from given text annotation

    @param: text_annotation, TextAnnotation instance to get POS tagger from
    @return: View instance of POS tagger
    """
    return get_view(text_annotation, "POS")


def get_dependency_parse(text_annotation):
    """
    Wrapper on getting the dependency from given text annotation

    @param: text_annotation, TextAnnotation instance to get dependency view from
    @return: View instance of the dependency
    """
    return get_view(text_annotation, "DEPENDENCY_STANFORD")


def get_ner_conll(text_annotation):
    """
    Wrapper on getting the NER_CONLL view from given text annotation

    @param: text_annotation TextAnnotation instance to get NER_CONLL view from.
    @return: View Instance of the NER_CONLL view.
    """
    return get_view(text_annotation, "NER_CONLL")


def get_ner_ontonotes(text_annotation):
    """
    Wrapper on getting the NER_ONTONOTES view from given text annotation

    @param: text_annotation TextAnnotation instance to get NER_ONTONOTES view from.
    @return: View Instance of the NER_ONTONOTES view.
    """
    return get_view(text_annotation, "NER_ONTONOTES")


def get_stanford_parse(text_annotation):
    """
    Wrapper on getting the PARSE_STANFORD view from given text annotation

    @param: text_annotation TextAnnotation instance to get PARSE_STANFORD view from.
    @return: View Instance of the PARSE_STANFORD view.
    """
    return get_view(text_annotation, "PARSE_STANFORD")


def get_srl_verb(text_annotation):
    """
    Wrapper on getting the SRL_VERB view from given text annotation

    @param: text_annotation TextAnnotation instance to get SRL_VERB view from.
    @return: View Instance of the SRL_VERB view.
    """
    return get_view(text_annotation, "SRL_VERB")


def get_srl_nom(text_annotation):
    """
    Wrapper on getting the SRL_NOM view from given text annotation

    @param: text_annotation TextAnnotation instance to get SRL_NOM view from.
    @return: View Instance of the SRL_NOM view.
    """
    return get_view(text_annotation, "SRL_NOM")


def get_quantities(text_annotation):
    """
    Wrapper on getting the QUANTITIES view from given text annotation

    @param: text_annotation TextAnnotation instance to get QUANTITIES view from.
    @return: View Instance of the QUANTITIES view.
    """
    return get_view(text_annotation, "QUANTITIES")


def get_shallow_parse(text_annotation):
    """
    Wrapper on getting the SHALLOW_PARSE view from given text annotation

    @param: text_annotation TextAnnotation instance to get SHALLOW_PARSE view from.
    @return: View Instance of the SHALLOW_PARSE view.
    """
    return get_view(text_annotation, "SHALLOW_PARSE")


def get_lemma(text_annotation):
    """
    Wrapper on getting the LEMMA view from given text annotation

    @param: text_annotation TextAnnotation instance to get LEMMA view from.
    @return: View Instance of the LEMMA view.
    """
    return get_view(text_annotation, "LEMMA")


def get_view(text_annotation, view_name):
    """
    Function to get user specified view from given text annotation

    @param: text_annotation, the TextAnnotation instance to get view from
             view_name, the specified view name for sending to pipeline server
    @return: View instance of the requested view
    """
    if pipeline_config.view_enabled(config, view_name) == False:
        logger.error('{} not defined or disabled.'.format(view_name))
        return None

    view = text_annotation.get_view(view_name)
    if view is None:
        additional_response = call_server(text_annotation.get_text(),
                                          view_name)
        return text_annotation.add_view(view_name, additional_response)
    return view


def call_server(text, views):
    """
    Funtion to get preprocess text annotation from server

    @param: text, the text to generate text annotation on
            views, the views to generate
    @return: raw text of the response from server
    """
    if pipeline is None:
        data = {'text': text, 'views': views}
        return requests.post(url+WEB_SERVER_SUFFIX, data).text
    else:
        view_list = views.split(',')
        text_annotation = pipeline.createBasicTextAnnotation("", "", text)
        for view in view_list:
            pipeline.addView(text_annotation, view.strip())
        return SerializationHelper.serializeToJson(text_annotation);

