import json


class CgView:
    def __init__(self, decoded="JSON", vName="POS"):

        self.viewName = vName
        self.viewJson = json.loads(decoded)
        self.viewPos = self.getPos(vName)
        self.viewType = self.getViewType()
        if (self.viewPos == -1):
            print("invalid view")

    def getViewType(self):
        fullType = self.viewJson["views"][self.viewPos]["viewData"][0]["viewType"]
        splitByPeriod = fullType.split(".")
        return splitByPeriod[len(splitByPeriod) - 1]

    def getPos(self, vName):
        for i in range(0, (len(self.viewJson["views"]) - 1)):
            if (self.viewJson["views"][i]["viewName"]) == vName:
                return i
        return -1

    def getCons(self, position=None):
        consList = []
        if position is not None:
            consList.append(self.viewJson["views"][self.viewPos]["viewData"][0]["constituents"][position]["label"])
        else:
            for i in range(0, len(self.viewJson["views"][self.viewPos]["viewData"][0]["constituents"])):
                consList.append(self.viewJson["views"][self.viewPos]["viewData"][0]["constituents"][i]["label"])
        return consList

    # why does this not work, but the above does?
    def getConScore(self, position=None):
        scoreArray = []
        if position is not None:
            scoreArray.append(self.viewJson["views"][self.viewPos]["viewData"][0]["constituents"][position]["score"])
        else:
            for i in range(0, len(self.viewJson["views"][0]["viewData"][0]["constituents"])):
                scoreArray.append(self.viewJson["views"][self.viewPos]["viewData"][0]["constituents"][i]["score"])
        return scoreArray

    def getRelations(self, position=None):
        if (self.viewType != "TreeView"):
            print("This view does not support relations")
            return
        else:
            relationArray = []
            if position is not None:
                relationArray.append(
                    self.viewJson["views"][self.viewPos]["viewData"][0]["relations"][position]["relationName"])
            else:
                for i in range(0, len(self.viewJson["views"][self.viewPos]["viewData"][0]["relations"])):
                    relationArray.append(
                        self.viewJson["views"][self.viewPos]["viewData"][0]["relations"][i]["relationName"])
            return relationArray
