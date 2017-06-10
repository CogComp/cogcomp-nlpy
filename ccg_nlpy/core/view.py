import json
import logging

logger = logging.getLogger(__name__)

class View(object):
    def __str__(self):
        """
        Special method to print the view in (label, tokens) format
        """
        constituent_label_string = ""
        if self.cons_list is None:
            constituent_label_string = "this view does not have constituents in your input text. "
        else:
            for cons in self.cons_list:
                constituent_label_string += "(" + cons['label'] + " " + cons['tokens'] + ") "
        return self.view_name + " view: " + constituent_label_string

    # The three following functions are used to make View class be able to iterate and index
    def __iter__(self):
        index = 0
        while index < len(self.cons_list):
            yield self.cons_list[index]
            index += 1

    def __getitem__(self, index):
        return self.cons_list[index]

    def __len__(self):
        return len(self.cons_list)


    def __init__(self, view, tokens):
        """
        Constructor for the view

        @param: view, the decoded JSON object containing information of the view
                tokens, List of tokens in the view
        """
        self.view_name = view["viewName"]
        self.tokens = tokens

        # get view_type: TreeView, PredicateArgument, TokenLabelView, ...
        full_type = view["viewData"][0]["viewType"]
        split_by_period = full_type.split(".")
        self.view_type = split_by_period[len(split_by_period) - 1]

        self.cons_list = None
        self.relation_array = None

        if "constituents" in view["viewData"][0]:
            self.cons_list = []
            for constituent in view["viewData"][0]["constituents"]:
                # Labels of TOKENS view will not be recorded when serializing text annotation in JSON format in pipeline
                # So there is a statement for handling this 
                cons_tokens = self.tokens[constituent['start']]
                for index in range(constituent['start']+1, constituent['end']):
                    cons_tokens += ' '
                    cons_tokens += self.tokens[index]
                if self.view_name == 'TOKENS':
                    constituent['label'] = cons_tokens
                constituent['tokens'] = cons_tokens
                self.cons_list.append(constituent)

        if "relations" in view["viewData"][0]:
            self.relation_array = []
            for relation in view["viewData"][0]["relations"]:
                self.relation_array.append(relation)
            self._link_constituents()

    def _link_constituents(self):
        """
        Helper function to build connection between constituents based on relation
        This function will be called only when relations exist
        """
        for relation_index in range(len(self.relation_array)):
            relation = self.relation_array[relation_index]
            src = self.cons_list[relation['srcConstituent']]
            target = self.cons_list[relation['targetConstituent']]
            if 'outgoing_relations' not in src:
                src['outgoing_relations'] = []
            if 'incoming_relations' not in target:
                target['incoming_relations'] = []
            src['outgoing_relations'].append(relation_index)
            target['incoming_relations'].append(relation_index)

    def get_view_type(self):
        """
        Function to get type of the view

        @return view type of the view
        """
        return self.view_type

    def get_cons(self, position=None, key=None):
        """
        Function to get a list of constituents in the view

        @param: position, the index of the specific constituent that user wants
                key, the specific key in constituents that user wants ("score", "label", "position","tokens")
        @return: if key is not given, a list of all constituents if position is not given,
                 or a list contains the constituent at specified position if position is given
                 otherwise, a list of specific key in respect to constituents

        """
        if self.cons_list is None:
            logger.warn("This view does not have constituents in your input text")
            return None

        if key is None:
            if position is not None and 0 <= position < len(self.cons_list):
                return [self.cons_list[position]]
            else:
                return self.cons_list
        elif key == "score" or key == "label" or key == "position" or key == "tokens":
            result_list = []
            if position is not None and 0 <= position < len(
                    self.cons_list):
                if key == "position":
                    result_list.append((self.cons_list[position]["start"],
                                        self.cons_list[position]["end"]))
                else:
                    result_list.append(self.cons_list[position][key])
            else:
                for constituent in self.cons_list:
                    if key == "position":
                        result_list.append(
                            (constituent["start"], constituent["end"]))
                    else:
                        result_list.append(constituent[key])
            return result_list

        logger.warn("Invalid key in constituent")
        return None

    def get_con_score(self, position=None):
        """
        Wrapper function to get a list of scores of constituents in the view

        @param: position, the index of the specific constituent that user wants score from
        @return: list of scores of all constituents if position is not given,
                 otherwise return a list contains the score of the constituent at specified position

        """
        return self.get_cons(position, "score")

    def get_con_label(self, position=None):
        """
        Wrapper function to get a list of labels of constituents in the view 

        @param: position, the index of the specific constituent that user wants label from 
        @return: list of labels of all constituents if position is not given, 
                 otherwise return a list contains the label of the constituent at specified position 
        """
        return self.get_cons(position, "label")

    def get_con_position(self, position=None):
        """
        Wrapper function to get a list of positions of constituents in the view in respect to tokens of the text

        @param: position, the index of the specific constituent that user wants token position from
        @return: list of position tuples (start_pos, end_pos) of all constituents if position is not given, 
                 otherwise return a list contains the token position of the constituent at specified position 
        """
        return self.get_cons(position, "position")

    def get_relations(self, position=None):
        """
        Funtion to get the relation array if the view supports relations

        @param: position, the index of the specific relation that user wants
        @return: list of relations if position is not given,
                 otherwise return a list contains the relation at specified position
        """
        if self.relation_array is None:
            logger.warn("This view does not support relations")
            return None
        else:
            if position is not None and 0 <= position < len(
                    self.relation_array):
                return [self.relation_array[position]]
            else:
                return self.relation_array

    def get_overlapping_constituents(self, start_token_index, end_token_index):
        """
        Function to get a list of constituents in the view that overlap with the indices provided

        @param: start_token_index, the starting index of the range for overlapping
                end_token_index, the ending index of the range for overlapping
        @return: List of overlapping constituents if the indice are valid, None otherwise
        """
        if start_token_index > end_token_index:
            logger.warn("Invalid token indices given, please provide proper indices.")
            return None
        view_overlapping_span = []
        for cons in self.cons_list:
            if((cons['start'] <= start_token_index and cons['end'] >= start_token_index) or
                    (cons['start'] <= end_token_index and cons['end'] >= end_token_index) or
                    (cons['start'] >= start_token_index and cons['end'] <= end_token_index) or
                    (cons['start'] <= start_token_index and cons['end'] >= end_token_index)):
                view_overlapping_span.append(cons)
        return view_overlapping_span
