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
from . import utils

logger = logging.getLogger(__name__)

# set up JVM and
import jnius_config
try:
    jnius_config.add_options('-Xmx16G')
    jnius_config.add_classpath(get_model_path() + '/*')
except Exception as e:
    logger.warning(
        "Couldn't set JVM config; this might be because you're setting up the multiple instances of the local pipeline.")
    logger.warning(str(e))

# Don't import jnius before setting jnius_config
# Sec 4.5 : https://media.readthedocs.org/pdf/pyjnius/latest/pyjnius.pdf
from jnius import autoclass


class LocalPipeline(PipelineBase):
    def __init__(self):
        """
        Constructor to set up local pipeline

        @param: file_name, the file name of the custom config file
        """
        super(LocalPipeline, self).__init__()

        self.PipelineFactory = None
        self.pipeline = None
        self.ProtobufSerializer = None

        pipeline_config.log_current_config(self.config, False)

        # load java classes
        try:
            self.PipelineFactory = autoclass('edu.illinois.cs.cogcomp.pipeline.main.PipelineFactory')
            self.SerializationHelper = autoclass('edu.illinois.cs.cogcomp.core.utilities.SerializationHelper')
            self.IntPair = autoclass('edu.illinois.cs.cogcomp.core.datastructures.IntPair')
            self.TextAnnotation = autoclass('edu.illinois.cs.cogcomp.core.datastructures.textannotation.TextAnnotation')
            self.BasicTextAnnotationBuilder = autoclass('edu.illinois.cs.cogcomp.annotation.BasicTextAnnotationBuilder')
            self.BasicAnnotatorService = autoclass('edu.illinois.cs.cogcomp.annotation.BasicAnnotatorService')
            self.Tokenizer = autoclass('edu.illinois.cs.cogcomp.nlp.tokenizer.StatefulTokenizer')
            self.TextAnnotationBuilder = autoclass('edu.illinois.cs.cogcomp.nlp.utility.TokenizerTextAnnotationBuilder')
            # self.ProtobufSerializer = autoclass('edu.illinois.cs.cogcomp.core.utilities.protobuf.ProtobufSerializer')
            self.Boolean = autoclass('java.lang.Boolean')
            self.JString = autoclass('java.lang.String')
            self.JArrayList = autoclass('java.util.ArrayList')
        except Exception as e:
            logger.error('Fail to load models, please check if your Java version is up to date.')
            logger.error(str(e))
            return None
        self.pipeline = self.PipelineFactory.buildPipelineWithAllViews(self.Boolean(True))

        logger.info("pipeline has been set up")

    def call_server(self, text, views):
        """
        Funtion to get preprocess text annotation from local pipeline

        @param: text, the text to generate text annotation on
                views, the views to generate
        @return: raw text of the response from local pipeline
        """
        text = utils.strToBytes(text)
        view_list = views.split(',')
        text_annotation = self.pipeline.createBasicTextAnnotation(
            self.JString(""), self.JString(""), self.JString(text))
        for view in view_list:
            if (len(view.strip()) > 0):
                try:
                    self.pipeline.addView(text_annotation,
                                          self.JString(view.strip()))
                except Exception as e:
                    logger.error('Failed to add view ' + view.strip())
                    logger.error(str(e))

        jsonStr = self.SerializationHelper.serializeToJson(text_annotation)

        return jsonStr


    def add_additional_views_to_TA(self, textannotation, views):
        # Convert python textannotation to JsonStr -> Bytes
        jsonstrBytes = utils.strToBytes(json.dumps(textannotation.as_json))
        jsonStrJava = self.JString(jsonstrBytes)
        javaTA = self.SerializationHelper.deserializeFromJson(jsonStrJava)

        view_list = views.split(',')
        for view in view_list:
            view = view.strip()
            if (len(view) > 0):
                try:
                    self.pipeline.addView(javaTA, self.JString(view))
                except Exception as e:
                    logger.error('Failed to add view ' + view.strip())
                    logger.error(str(e))

        # Deserialize javaTA (woth additional views) to JsonStr
        jsonStr = self.SerializationHelper.serializeToJson(javaTA)

        return jsonStr


    def call_server_pretokenized(self, pretokenized_text, views):
        """
        Funtion to get preprocess text annotation from local pipeline

        @param: pretokenized_text, list of list of tokens of pre-tokenized text
        @return: raw text of the response from local pipeline
        """
        view_list = views.split(',')

        docAl = self.JArrayList()
        for sent in pretokenized_text:
            sentAL = self.JArrayList()
            for w in sent:
                w = utils.strToBytes(w)
                sentAL.add(self.JString(w))

            docAl.add(sentAL)

        text_annotation = self.BasicTextAnnotationBuilder.\
            createTextAnnotationFromListofListofTokens(docAl)

        for view in view_list:
            if (len(view.strip()) > 0):
                try:
                    self.pipeline.addView(text_annotation, self.JString(view.strip()))
                except Exception as e:
                    logger.error('Failed to add view ' + view.strip())
                    logger.error(str(e))

        jsonStr = self.SerializationHelper.serializeToJson(text_annotation)

        return jsonStr


    def doc_split_on_hyphens(self, text):
        tokenizer = self.Tokenizer()
        tab = self.TextAnnotationBuilder(tokenizer)

        text = utils.strToBytes(text)
        text_annotation = tab.createTextAnnotation(self.JString(""),
                                                   self.JString(""),
                                                   self.JString(text))



        jsonStr = self.SerializationHelper.serializeToJson(text_annotation)
        ta_python = TextAnnotation(json_str=jsonStr, pipeline_instance=self)

        return ta_python




    def call_server_with_sentences(self, sentences, views):
        """
        Funtion to get preprocess text annotation from local pipeline

        @param: sentences, the sentences to generate text annotation
                on views, the views to generate. sentences should be
                a list of lists of strings. Each string represents a token
                or word, each constituent list represents a sentence.
        @return: raw text of the response from local pipeline
        """
        view_list = views.split(',')
        tokens = [token for sent in sentences for token in sent]
        text = ' '.join(tokens)
        char_offsets = []
        count = 0
        char_offsets_ints = []
        for token in tokens:
            char_offsets.append(self.IntPair(count, count+len(token)-1+1))
            char_offsets_ints.append((count, count+len(token)-1+1))
            count += len(token)+1
        sentence_end_indices = []
        count = 0
        for sent in sentences:
            sentence_end_indices.append(count+len(sent)-1+1)
            count += len(sent)
        text = utils.strToBytes(text)
        text_annotation = self.TextAnnotation("", "", text, char_offsets, tokens, sentence_end_indices)
        for view in view_list:
            if (len(view.strip()) > 0):
                try:
                    self.pipeline.addView(text_annotation, self.JString(view.strip()))
                except Exception as e:
                    logger.error('Failed to add view ' + view.strip())
                    logger.error(str(e))

        json = self.SerializationHelper.serializeToJson(text_annotation)

        return json
