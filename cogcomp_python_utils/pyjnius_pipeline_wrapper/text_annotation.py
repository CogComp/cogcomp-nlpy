import json
from CgView import CgView

class TextAnnotation:
    '''
        This class is was designed to be a python version of the TextAnnotation class.
        However, it is not a complete recreation of the class because the class itself is too complex
        and it interacts with other classes heavily.
        So there are only couple functions that extract information directly from Text Annotation Java object

        While the most of the query on view can be done with CgView by querying on
        The JSON format of the Text Annotation (since the JSON string obtained from SerializationHelper
         is the same as the JSON format returned from web server)

    '''
    def __init__(self, text_annotation = None, json_str = None):
        self.text_annotation = text_annotation
        self.views = (self.text_annotation.getAvailableViews()).toArray()
        self.tokens = self.text_annotation.getTokens()
        self.num_of_sentences = self.text_annotation.getNumberOfSentences()
        self.sentences = []
        for i in range(self.num_of_sentences):
            self.sentences.append(self.text_annotation.getSentence(i).getText())

        # Adopted Ani's code 
        self.json= json.loads(json_str)
        self.viewList=[]
        for i in range(len(self.views)):
            self.viewList.append(CgView(json_str,self.views[i]))

    def get_view(self, view_name):
        for i in range(len(self.views)):
            if self.viewList[i].viewName == view_name:
                return self.viewList[i]
        return None

    # Ani's code
    def getScore(self):
        return self.json["sentences"]["score"]
    def getEndPos(self):
        return self.json["sentences"]["sentenceEndPositions"]

    ''' Functions that can be used without json, keep them until getting further instruction '''
    def get_available_views(self):
        return self.views
        
    def get_tokens(self):
        return self.tokens

    def get_sentence(self, index):
        return self.sentences[index]

    def get_sentences(self):
        return self.sentences

    def get_num_of_sentence(self):
        return self.num_of_sentences

    def get_view_score(self, view_name):
        return self.text_annotation.getView(view_name).getScore()
