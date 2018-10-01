import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import copy

# A dummy model that is used with the model wrapper server You need to define two methods load_params and
# inference_on_ta when writing your own model, for it to be compatible with the model wrapper server.
class DummyModel:
    def __init__(self):
        pass

    def load_params(self):
        logging.info("loading model params ...")

    def inference_on_ta(self, docta, new_view_name):
        # This upcases each token. Test for TokenLabelView
        # new_view = copy.deepcopy(docta.get_view("TOKENS"))
        # tokens = docta.get_tokens
        # for token, cons in zip(tokens, new_view.cons_list):
        #     cons["label"] = token.upper()

        # This replaces each NER with its upcased tokens. Test for SpanLabelView
        new_view = copy.deepcopy(docta.get_view("NER_CONLL"))
        for nercons in new_view.cons_list:
            nercons["label"] = nercons["tokens"].upper()
        new_view.view_name = new_view_name
        docta.view_dictionary[new_view_name] = new_view
        return docta
