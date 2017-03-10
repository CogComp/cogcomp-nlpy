import json
from .view import *
'''
    For now, this class is implemented as an indirect type
    All the functions can (should) be called indirectly by functions in Pipeliner class
'''


class TextAnnotation:
    '''
        This class is was designed to be a python version of the TextAnnotation class.
        While most of the queries on view are done with View by querying on
        The JSON format of the Text Annotation (since the JSON string obtained from SerializationHelper
         is the same as the JSON format returned from web server)

    '''

    def __init__(self, json_str=None):
        # Adopted Ani's code 
        result_json = json.loads(json_str)

        self.text = result_json["text"]
        self.tokens = result_json["tokens"]
        self.score = result_json["sentences"]["score"]
        self.sentence_end_position = result_json["sentences"][
            "sentenceEndPositions"]

        self.view_dictionary = {}
        for view in result_json["views"]:
            self.view_dictionary[view["viewName"]] = View(view, self.tokens)

    # Functions to manipulate the views on text annotation

    def add_view(self, view_name, response):
        result_json = json.loads(response)

        # check if the view is retrieve correctly
        # if view does not exist, the first view in views will be "token"
        if (result_json["views"][0]["viewName"] == view_name):
            new_view = View(result_json["views"][0], self.tokens)
            self.view_dictionary[view_name] = new_view
            return new_view
        else:
            print("Invalid view name, please check.")
            return None

    def get_view(self, view_name):
        if view_name in self.view_dictionary:
            return self.view_dictionary[view_name]
        else:
            return None

    def get_views(self):
        return list(self.view_dictionary.keys())

    # Functions to get general information about the text annotation

    def get_text(self):
        return self.text

    # Ani's code
    def get_tokens(self):
        return self.tokens

    def get_score(self):
        return self.score

    def get_end_pos(self):
        return self.sentence_end_position
