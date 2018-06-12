import json
import logging

from .view import *
from .predicate_argument_view import *

logger = logging.getLogger(__name__)

class TextAnnotation(object):
    '''
        This class is was designed to be a python version of the TextAnnotation class.
        While most of the queries on view are done with View by querying on
        The JSON format of the Text Annotation (since the JSON string obtained from SerializationHelper
         is the same as the JSON format returned from web server)

    '''

    def __init__(self, json_str=None, pipeline_instance=None):
        result_json = json.loads(json_str)

        self.pipeline = pipeline_instance
        self.corpusId = result_json["corpusId"].strip()
        self.id = result_json["id"].strip()
        self.text = result_json["text"].strip()
        if len(self.text) <= 0:
            logger.warn("Creating empty TextAnnotation.")
            self.empty = True
        else:
            self.empty = False
        self.tokens = result_json["tokens"]
        self.score = result_json["sentences"]["score"]
        self.sentences = result_json["sentences"]
        self.sentence_end_position = self.sentences["sentenceEndPositions"]
        if "tokenOffsets" in result_json:
            self.char_offsets = result_json["tokenOffsets"]
        else:
            self.char_offsets = self._extract_char_offset(self.text, self.tokens)
        self.view_dictionary = {}
        for view in result_json["views"]:
            self.view_dictionary[view["viewName"]] = self._view_builder(view)

    def _view_builder(self, view):
        full_type = view["viewData"][0]["viewType"]
        split_by_period = full_type.split(".")
        view_type = split_by_period[len(split_by_period) - 1]
        if view_type == 'PredicateArgumentView':
            return PredicateArgumentView(view, self.tokens)
        else: 
            return View(view, self.tokens)

    def _extract_char_offset(self, sentence, tokens):
        """
        a function to extract char offsets given tokens and raw string
        Originally implemented in
        https://github.com/CogComp/cogcomp-nlp/blob/12cf80eabc92fe69ff7a53709f6d6e91fb00687d/core-utilities/src/main/java/edu/illinois/cs/cogcomp/core/utilities/TokenUtils.java#L27
        """
        offsets = []

        tokenId = 0
        characterId = 0

        tokenCharacterStart = 0
        tokenLength = 0

        while (characterId < len(sentence)
                 and sentence[characterId].isspace()):
            characterId = characterId + 1

        while (characterId < len(sentence)):
            if (tokenLength == len(tokens[tokenId])):
                offsets.append((tokenCharacterStart, characterId))

                while (characterId < len(sentence) and sentence[characterId].isspace()):
                    characterId = characterId + 1

                tokenCharacterStart = characterId
                tokenLength = 0
                tokenId = tokenId + 1

            else:
                assert sentence[characterId] == tokens[tokenId][tokenLength], sentence[characterId] + " expected, found " + tokens[tokenId][tokenLength] + " instead in sentence: " + sentence;
                tokenLength = tokenLength + 1
                characterId = characterId + 1

        if (characterId == len(sentence) and len(offsets) == len(tokens) - 1):
            offsets.append((tokenCharacterStart, len(sentence)))

        assert len(offsets) == len(tokens), offsets

        return offsets

    # Functions to manipulate the views on text annotation

    @property 
    def get_pos(self):
        """
        Wrapper on getting part-of-speech tagger from given text annotation
        @param: text_annotation, TextAnnotation instance to get POS tagger from
        @return: View instance of POS tagger
        """
        return self.get_view("POS")

    @property
    def get_dependency_parse(self):
        """
        Wrapper on getting the dependency from given text annotation
        @param: text_annotation, TextAnnotation instance to get dependency view from
        @return: View instance of the dependency
        """
        return self.get_view("DEPENDENCY")

    @property
    def get_stanford_dependency_parse(self):
        """
        Wrapper on getting the dependency from given text annotation
        @param: text_annotation, TextAnnotation instance to get dependency view from
        @return: View instance of the dependency
        """
        return self.get_view("DEPENDENCY_STANFORD")

    @property
    def get_ner_conll(self):
        """
        Wrapper on getting the NER_CONLL view from given text annotation
        @param: text_annotation TextAnnotation instance to get NER_CONLL view from.
        @return: View Instance of the NER_CONLL view.
        """
        return self.get_view("NER_CONLL")

    @property 
    def get_ner_ontonotes(self):
        """
        Wrapper on getting the NER_ONTONOTES view from given text annotation
        @param: text_annotation TextAnnotation instance to get NER_ONTONOTES view from.
        @return: View Instance of the NER_ONTONOTES view.
        """
        return self.get_view("NER_ONTONOTES")

    @property 
    def get_stanford_parse(self):
        """
        Wrapper on getting the PARSE_STANFORD view from given text annotation
        @param: text_annotation TextAnnotation instance to get PARSE_STANFORD view from.
        @return: View Instance of the PARSE_STANFORD view.
        """
        return self.get_view("PARSE_STANFORD")

    @property 
    def get_srl_verb(self):
        """
        Wrapper on getting the SRL_VERB view from given text annotation
        @param: text_annotation TextAnnotation instance to get SRL_VERB view from.
        @return: View Instance of the SRL_VERB view.
        """
        return self.get_view("SRL_VERB")

    @property 
    def get_srl_nom(self):
        """
        Wrapper on getting the SRL_NOM view from given text annotation
        @param: text_annotation TextAnnotation instance to get SRL_NOM view from.
        @return: View Instance of the SRL_NOM view.
        """
        return self.get_view("SRL_NOM")

    @property
    def get_srl_prep(self):
        """
        Wrapper on getting the SRL_PREP view from given text annotation
        @param: text_annotation TextAnnotation instance to get SRL_PREP view from.
        @return: View Instance of the SRL_PREP view.
        """
        return self.get_view("SRL_PREP")

    @property
    def get_srl_comma(self):
        """
        Wrapper on getting the SRL_COMMA view from given text annotation
        @param: text_annotation TextAnnotation instance to get SRL_COMMA view from.
        @return: View Instance of the SRL_COMMA view.
        """
        return self.get_view("SRL_COMMA")

    @property 
    def get_quantities(self):
        """
        Wrapper on getting the QUANTITIES view from given text annotation
        @param: text_annotation TextAnnotation instance to get QUANTITIES view from.
        @return: View Instance of the QUANTITIES view.
        """
        return self.get_view("QUANTITIES")

    @property 
    def get_shallow_parse(self):
        """
        Wrapper on getting the SHALLOW_PARSE view from given text annotation
        @param: text_annotation TextAnnotation instance to get SHALLOW_PARSE view from.
        @return: View Instance of the SHALLOW_PARSE view.
        """
        return self.get_view("SHALLOW_PARSE")

    @property 
    def get_lemma(self):
        """
        Wrapper on getting the LEMMA view from given text annotation
        @param: text_annotation TextAnnotation instance to get LEMMA view from.
        @return: View Instance of the LEMMA view.
        """
        return self.get_view("LEMMA")

    def add_view(self, view_name, response):
        result_json = json.loads(response)

        # check if the view is retrieve correctly
        # iterate through all the views presented in response, add the view that hasn't been store,
        # return the view requested
        requested_view = None
        view_constituents = []
        for view in result_json["views"]:
            name = view["viewName"]
            view_constituents.append(name)
            if name not in self.view_dictionary:
                self.view_dictionary[name] = self._view_builder(view)

            if name == view_name:
                requested_view = self.view_dictionary[name]
        
        if requested_view is None:
            # "token" view will always be included
            if len(view_constituents) <= 1:
                logger.error("Invalid view name, please check.")
            else:
                logger.info("The view is the collection of the following views: {0}".format(view_constituents))
                self.view_dictionary[name] = view_constituents
        return requested_view

    def get_view(self, view_name):
        if self.empty:
            logger.error("No valid views on empty TextAnnotation.")
            return None
        if view_name not in self.view_dictionary:
            additional_response = self.pipeline.call_server(self.text, view_name)
            self.add_view(view_name, additional_response)

        if type(self.view_dictionary[view_name]) != type([]):
            return self.view_dictionary[view_name]
        else:
            logger.info("The view is the collection of the following views: {0}".format(self.view_dictionary[view_name]))
            return None

    @property
    def get_views(self):
        return list(self.view_dictionary.keys())

    # Functions to get general information about the text annotation

    @property
    def get_text(self):
        return self.text

    @property
    def get_tokens(self):
        return self.tokens

    @property
    def get_token_char_offsets(self):
        """
        Returns char offsets for tokens.
        For example, if the input string is:
        "Hello, how are you. I am doing fine"
        which is tokenized into this list:  [u'Hello', u',', u'how', u'are', u'you', u'.', u'I', u'am', u'doing', u'fine']
        calling this function should return the following list of pairs:

        [(0, 5), (5, 6), (7, 10), (11, 14), (15, 18), (18, 19), (20, 21), (22, 24), (25, 30), (31, 35)]
        """
        return self.char_offsets

    @property
    def get_score(self):
        return self.score

    @property
    def get_sentence_end_token_indices(self):
        return self.sentence_end_position

    @property
    def as_json(self):
        output = {
            "corpusId": self.corpusId,
            "id": self.id,
            "text": self.text,
            "tokens": self.tokens,
            "tokenOffsets": self.char_offsets,
            "sentences": self.sentences,
            "views": [v.as_json for v in self.view_dictionary.values()]
        }
        return output
