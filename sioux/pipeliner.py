import json
import requests
import os

from backports.configparser import RawConfigParser

from .core.text_annotation import *
"""
Constructor of the pipeliner to setup the api address of pipeline server
"""
config = RawConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(dir_path + '/config/pipeline.cfg')
url = config.get('PipelineServer', 'api')

# assuming that the path to jar files is specified in config file
pipeline = None
PipelineFactory = None
SerializationHelper = None
if config.has_section('jar_path'):
    import jnius_config
    jnius_config.add_options('-Xmx16G')
    for item in config.items('jar_path'):
        jnius_config.add_classpath(item[1])

def init(user_config = None, using_web_server = False):
    if using_web_server == False:
        from jnius import autoclass
        PipelineFactory = autoclass('edu.illinois.cs.cogcomp.nlp.pipeline.IllinoisPipelineFactory')
        SerializationHelper = autoclass('edu.illinois.cs.cogcomp.core.utilities.SerializationHelper')
        if user_config is not None:
            ResourceManager = autoclass('edu.illinois.cs.cogcomp.core.utilities.configuration.ResourceManager')
            userConfig = ResourceManager("userconfig.properties")
            pipeline = PipelineFactory.buildPipeline(userConfig)
        else:
            pipeline = PipelineFactory.buildPipeline()
    print("pipeline has been set up")

def doc(text="Hello World"):
    """
    Initialize text annotation of given text

    @param: text, the text to be processed
    @return: TextAnnotation instance of the text
    """
    response = call_server(text, "POS")
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
        return requests.post(url, data).text
    else:
        view_list = views.split(',')
        text_annotation = pipeline.createBasicTextAnnotation("", "", text)
        for view in view_list:
            pipeline.addView(text_annotation, view.strip())
        return SerializationHelper.serializeToJson(text_annotation);

