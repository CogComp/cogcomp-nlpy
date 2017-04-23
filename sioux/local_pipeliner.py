import json
import requests
import sys
import os
import logging

from backports.configparser import RawConfigParser

from .basic_pipeliner import *
from google.protobuf import json_format
from .protobuf import TextAnnotation_pb2
from .core.text_annotation import *
from .download import get_model_path
from . import pipeline_config

logger = logging.getLogger(__name__)

class LocalPipeliner(BasicPipeliner):
    def __init__(self, enable_views=None, disable_views=None, file_name = None):
        super(LocalPipeliner,self).__init__(file_name)

        self.PipelineFactory = None
        self.pipeline = None
        self.ProtobufSerializer = None

        enabled_views = pipeline_config.change_temporary_config(self.config, self.models_downloaded, enable_views, disable_views, False, None)

        if enabled_views is not None:
            import jnius_config
            jnius_config.add_options('-Xmx16G')
            jnius_config.add_classpath(get_model_path()+'/*')
            from jnius import autoclass
            try:
                self.PipelineFactory = autoclass('edu.illinois.cs.cogcomp.pipeline.main.PipelineFactory')
                self.SerializationHelper = autoclass('edu.illinois.cs.cogcomp.core.utilities.SerializationHelper')
                self.ProtobufSerializer = autoclass('edu.illinois.cs.cogcomp.core.utilities.protobuf.ProtobufSerializer')
                self.String = autoclass('java.lang.String')
            except:
                logger.error('Fail to load models, please check if your Java version is up to date.')
                return None
            if len(enabled_views) == 0:
                self.pipeline = self.PipelineFactory.buildPipeline()
            else:
                self.pipeline = self.PipelineFactory.buildPipeline(*enabled_views)
        else:
            logger.error("Error encountered when setting up pipeline")
            return None

        logger.info("pipeline has been set up")


    def call_server(self, text, views):
        """
        Funtion to get preprocess text annotation from server

        @param: text, the text to generate text annotation on
                views, the views to generate
        @return: raw text of the response from server
        """
        view_list = views.split(',')
        text_annotation = self.pipeline.createBasicTextAnnotation("", "", text)
        for view in view_list:
            self.pipeline.addView(text_annotation, view.strip())
        #json = SerializationHelper.serializeToJson(text_annotation)

        path = os.path.expanduser('~') + "{0}.sioux{0}".format(os.path.sep) + 'temp.temp'

        self.ProtobufSerializer.writeToFile(text_annotation,path)
        proto_data = None
        with open(path, 'rb') as f:
            proto_data = f.read()

        message = TextAnnotation_pb2.TextAnnotationProto()
        message.ParseFromString(proto_data)
        proto_to_json = json_format.MessageToJson(message)

        return proto_to_json

