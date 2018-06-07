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

logger = logging.getLogger(__name__)


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

        # set up JVM and load classes needed
        try:
            import jnius_config
            jnius_config.add_options('-Xmx16G')
            jnius_config.add_classpath(get_model_path() + '/*')
        except Exception as e:
            logger.warning(
                "Couldn't set JVM config; this might be because you're setting up the multiple instances of the local pipeline.")
            logger.warning(str(e))
        try:
            from jnius import autoclass
            self.PipelineFactory = autoclass('edu.illinois.cs.cogcomp.pipeline.main.PipelineFactory')
            self.SerializationHelper = autoclass('edu.illinois.cs.cogcomp.core.utilities.SerializationHelper')
            self.IntPair = autoclass('edu.illinois.cs.cogcomp.core.datastructures.IntPair')
            self.TextAnnotation = autoclass('edu.illinois.cs.cogcomp.core.datastructures.textannotation.TextAnnotation')
            # self.ProtobufSerializer = autoclass('edu.illinois.cs.cogcomp.core.utilities.protobuf.ProtobufSerializer')
            self.Boolean = autoclass('java.lang.Boolean')
            self.JString = autoclass('java.lang.String')
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
        view_list = views.split(',')
        text_annotation = self.pipeline.createBasicTextAnnotation(self.JString(""), self.JString(""),
                                                                  self.JString(text))
        for view in view_list:
            if (len(view.strip()) > 0):
                try:
                    self.pipeline.addView(text_annotation, self.JString(view.strip()))
                except Exception as e:
                    logger.error('Failed to add view ' + view.strip())
                    logger.error(str(e))

        json = self.SerializationHelper.serializeToJson(text_annotation)
        print(json)

        # path = os.path.expanduser('~') + "{0}.ccg_nlpy{0}".format(os.path.sep) + 'temp.temp'
        #
        # self.ProtobufSerializer.writeToFile(text_annotation, self.JString(path))
        # proto_data = None
        # with open(path, 'rb') as f:
        #     proto_data = f.read()
        #
        # message = TextAnnotation_pb2.TextAnnotationProto()
        # message.ParseFromString(proto_data)
        # proto_to_json = json_format.MessageToJson(message)

        return json

    def call_server_with_sentences(self, sentences, views):
        """
        Funtion to get preprocess text annotation from local pipeline

        @param: sentences, the sentences to generate text annotation
                on views, the views to generate
        @return: raw text of the response from local pipeline
        """
        view_list = views.split(',')
        tokens = [token for sent in sentences for token in sent]
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
