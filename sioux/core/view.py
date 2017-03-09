import json

'''
    Refactored constructor, all attributes are constructed in constructor rather than on demand (create when get_xxx is called)

    Refactored get_cons such that it will return list of constituents is no key is provided, otherwise, return list of corresponding field (label, score, tuple(start_pos, end_pos), token(?))
'''
class View:
    def __str__(self):
        constituent_label_string = ""
        if self.cons_list is None:
            constituent_label_string = "this view does not have constituents on the text"
        else:
            tokens = self.get_cons(position=None, key="token")
            labels = self.get_cons(position=None, key="label")
            for i in range(len(labels)):
                constituent_label_string += "(" + labels[i] + " " + tokens[i] + ") "
        return self.view_name + " view: " + constituent_label_string

    def __init__(self, view, tokens):
        self.view_name = view["viewName"]
        self.view_json = view #could be removed
        self.tokens = tokens

        full_type = self.view_json["viewData"][0]["viewType"]
        split_by_period = full_type.split(".")
        self.view_type = split_by_period[len(split_by_period) - 1]

        self.cons_list = None
        self.relation_array = None

        if "constituents" in self.view_json["viewData"][0]:
            self.cons_list = []
            for constituent in self.view_json["viewData"][0]["constituents"]:
                self.cons_list.append(constituent)

        if self.view_type == "TreeView":
            self.relation_array = []
            for relation in self.view_json["viewData"][0]["relations"]:
                self.relation_array.append(relation["relationName"])

    def get_view_type(self):
        return self.view_type

    '''
        key == "token" is a black box option, it is used in "__str__" to print the constituent-label content of the view
    '''
    def get_cons(self, position=None, key=None):
        if self.cons_list is None:
            print("This view does not have constituents on the text")
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
                    for i in range(constituent["start"], (constituent["end"]-1)):
                        tokens += self.tokens[i]+" "

                    tokens += self.tokens[constituent["end"]-1]
                    result_list.append(tokens)
            else:
                if position is not None and 0 <= position < len(self.cons_list):
                    if key == "position":
                        result_list.append((self.cons_list[position]["start"], self.cons_list[position]["end"]))
                    else:
                        result_list.append(self.cons_list[position][key])
                else:
                    for constituent in self.cons_list:
                        if key == "position":
                            result_list.append((constituent["start"], constituent["end"]))
                        else:
                            result_list.append(constituent[key])
            return result_list

        print("Invalid key in constituent")
        return None

    # why does this not work, but the above does?
    def get_con_score(self, position=None):
        return self.get_cons(position, "score")

    def get_con_label(self, position=None):
        return self.get_cons(position, "label")

    def get_con_position(self, position=None):
        return self.get_cons(position, "position")

    def get_relations(self, position=None):
        if self.view_type != "TreeView":
            print("This view does not support relations")
            return None
        else:
            if position is not None and 0 <= postion < len(self.relation_array):
                return [self.relation_array[position]]
            else:
                return self.relation_array
