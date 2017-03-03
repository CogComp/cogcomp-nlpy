import json
import requests

from cogcomp_python_utils.CgView import CgView


class CgPipeliner:
    ##initialize pipeliner and makes call to the server to retrieve the  Json file
    def __init__(self, text="Hello World", views="POS"):
        ##
        self.viewNames = views.split(",")
        ##we need to make sure we're not sending blank spaces to the server
        string = text.replace(" ", "%20")
        url = 'http://austen.cs.illinois.edu:8080/annotate?text=' + string + '&views=' + views
        requests.encoding = 'utf-8'
        self.decoded =requests.get(url).text
        ##this is to make sure we don't call the server over and over again to retrieve the information
        self.json = json.loads(self.decoded)
        ##the dictionary that we use to store views
        self.viewDict={}
        for i in range(0, len(self.viewNames)):
            self.viewDict[self.viewNames[i]]=(CgView(self.decoded, self.viewNames[i]))

    def getTokens(self):
        return (self.json['tokens'])
    def getScore(self):
        return self.json["sentences"]["score"]
    def getEndPos(self):
        return self.json["sentences"]["sentenceEndPositions"]
