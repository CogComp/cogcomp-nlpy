import logging
from typing import List

from ccg_nlpy.server.annotator import Annotator

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import copy


# A dummy model that is used with the model wrapper server You need to define two methods load_params and
# inference_on_ta when writing your own model, for it to be compatible with the model wrapper server.
class DummyAnnotator(Annotator):
    def __init__(self):
        self.provided_view = "DUMMYVIEW"
        # self.required_views = ["TOKENS", "NER_CONLL"]
        self.required_views = ["TOKENS"]

    def get_required_views(self) -> List[str]:
        return self.required_views

    def get_view_name(self) -> str:
        return self.provided_view

    def load_params(self):
        logging.info("loading model params ...")

    def add_view(self, docta):
        # This upcases each token. Test for TokenLabelView
        new_view = copy.deepcopy(docta.get_view("TOKENS"))
        tokens = docta.get_tokens
        for token, cons in zip(tokens, new_view.cons_list):
            cons["label"] = token.upper()

        # # This replaces each NER with its upcased tokens. Test for SpanLabelView
        # new_view = copy.deepcopy(docta.get_view("NER_CONLL"))
        # for nercons in new_view.cons_list:
        #     nercons["label"] = nercons["tokens"].upper()

        new_view.view_name = self.provided_view
        docta.view_dictionary[self.provided_view] = new_view
        return docta
