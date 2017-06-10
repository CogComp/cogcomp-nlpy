import logging
from google.protobuf import json_format

from .core.text_annotation import TextAnnotation
from .protobuf import TextAnnotation_pb2

logging.basicConfig(level=logging.INFO)

def load_document_from_json(file_name):
    """
    Load a TextAnnotation document from a JSON file.

    Returns a TextAnnotation instance.
    """

    json_data = None
    with open(file_name, 'rb') as f:
        json_data = f.read()

    return TextAnnotation(json_data)


def load_document_from_protobuf(file_name):
    """
    Load a TextAnnotation document from a protocol buffer encoded file.

    Returns a TextAnnotation instance.
    """

    proto_data = None
    with open(file_name, 'rb') as f:
        proto_data = f.read()

    message = TextAnnotation_pb2.TextAnnotationProto()
    message.ParseFromString(proto_data)

    # Currently convering the protobuf object to a JSON string and pass it to TextAnnotation
    # TODO - Parse protobuf directly instead of JSON when TextAnnotation is more mature.
    return TextAnnotation(json_format.MessageToJson(message))
