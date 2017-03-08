import json

'''
    Refactored View constructor, accept a jsonlized object of the view rather than a string
        and remove parameter viewName since all the view related information can be retrieved from the object
    Remove getPos function since View is created on specific view (lost relative position)
        where it used to be constructed with the complete response from server
'''
class View:
    def __init__(self, view):
        self.viewName = view["viewName"]
        self.viewJson = view
        #TODO: complex (need a few line to retrieve) result is built on demand, good practice?
        self.viewType = None
        self.consList = None
        self.scoreArray = None
        self.relationArray = None

    def getViewType(self):
        if self.viewType is None:
            fullType = self.viewJson["viewData"][0]["viewType"]
            splitByPeriod = fullType.split(".")
            self.viewType = splitByPeriod[len(splitByPeriod) - 1]
        return self.viewType

    def getCons(self, position=None):
        if self.consList is None and "constituents" in self.viewJson["viewData"][0]:
            self.consList = []
            for constituent in self.viewJson["viewData"][0]["constituents"]:
                self.consList.append(constituent["label"])
        if self.consList is None:
            print("This view does not have constituents on the text")
            return None

        if position is not None and 0 <= position < len(self.consList):
            return [self.consList[position]]
        else:
            return self.consList

    # why does this not work, but the above does?
    def getConScore(self, position=None):
        if self.scoreArray is None and "constituents" in self.viewJson["viewData"][0]:
            self.scoreArray = []
            for constituent in self.viewJson["viewData"][0]["constituents"]:
                self.scoreArray.append(constituent["score"])
        if self.scoreArray is None:
            print("This view does not have constituents on the text")
            return None

        if position is not None and 0 <= position < len(self.scoreArray):
            return [self.scoreArray[position]]
        else:
            return self.scoreArray

    def getRelations(self, position=None):
        if (self.getViewType() != "TreeView"):
            print("This view does not support relations")
            return None
        else:
            if self.relationArray is None:
                self.relationArray = []
                for relation in self.viewJson["viewData"][0]["relations"]:
                    self.relationArray.append(relation["relationName"])

            if position is not None and 0 <= postion < len(self.relationArray):
                return [self.relationArray[position]]
            else:
                return self.relationArray
