import json
'''
    Refactored constructor, all attributes are constructed in constructor rather than on demand (create when get_xxx is called)

    Refactored get_cons such that it will return list of constituents is no key is provided, otherwise, return list of corresponding field (label, score, tuple(start_pos, end_pos), token(?))
'''


class View(object):
    def __str__(self):
        constituent_label_string = ""
        if self.cons_list is None:
            constituent_label_string = "this view does not have constituents in your input text. "
        else:
            tokens = self.get_cons(position=None, key="token")
            labels = self.get_cons(position=None, key="label")
            for i in range(len(labels)):
                constituent_label_string += "(" + labels[i] + " " + tokens[
                    i] + ") "
        return self.view_name + " view: " + constituent_label_string

    def __init__(self, view, tokens):
        self.view_name = view["viewName"]
        self.view_json = view  #could be removed
        self.tokens = tokens

        full_type = self.view_json["viewData"][0]["viewType"]
        split_by_period = full_type.split(".")
        self.view_type = split_by_period[len(split_by_period) - 1]

        self.cons_list = None
        self.relation_array = None

        if "constituents" in self.view_json["viewData"][0]:
            self.cons_list = []
            for constituent in self.view_json["viewData"][0]["constituents"]:
                # Labels of TOKENS view will not be recorded when serializing text annotation in JSON format in pipeline
                # So there is a statement for handling this 
                if self.view_name == 'TOKENS':
                    label = self.tokens[constituent['start']]
                    for index in range(constituent['start']+1, constituent['end']):
                        label += ' '
                        label += self.tokens[index]
                    constituent['label'] = label
                self.cons_list.append(constituent)

        if "relations" in self.view_json["viewData"][0]:
            self.relation_array = []
            for relation in self.view_json["viewData"][0]["relations"]:
                self.relation_array.append(relation)

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
                key, the specific key in constituents that user wants ("score", "label", "position")
        @return: if key is not given, a list of all constituents if position is not given,
                 or a list contains the constituent at specified position if position is given
                 otherwise, a list of specific key in respect to constituents

        key == "token" is a black box option, it is used in "__str__" to print the constituent-label content of the view

        """
        if self.cons_list is None:
            print("This view does not have constituents in your input text")
            return None

        if key is None:
            if position is not None and 0 <= position < len(self.cons_list):
                return [self.cons_list[position]]
            else:
                return self.cons_list
        elif key == "score" or key == "label" or key == "position" or key == "token":
            result_list = []
            if key == "token":
                for constituent in self.cons_list:
                    tokens = ""

                    # end for loop one index earlier such that no extra space at the end
                    for i in range(constituent["start"],
                                   (constituent["end"] - 1)):
                        tokens += self.tokens[i] + " "

                    tokens += self.tokens[constituent["end"] - 1]
                    result_list.append(tokens)
            else:
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

        print("Invalid key in constituent")
        return None

    # why does this not work, but the above does?
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
            print("This view does not support relations")
            return None
        else:
            if position is not None and 0 <= position < len(
                    self.relation_array):
                return [self.relation_array[position]]
            else:
                return self.relation_array
