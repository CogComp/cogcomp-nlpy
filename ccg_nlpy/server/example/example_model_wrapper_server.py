from flask import Flask
from flask_cors import CORS

from ccg_nlpy.server.example.dummy_model import DummyModel
from ccg_nlpy.server.model_wrapper_server_local_pipeline import ModelWrapperServerLocal
from ccg_nlpy.server.model_wrapper_server_remote_pipeline import ModelWrapperServerRemote

app = Flask(__name__)
# necessary for testing on localhost
CORS(app)


def main():
    model = DummyModel()  # create your model object here
    # The model should have two methods
    # 1) method load_params() that loads the relevant model parameters into memory.
    # 2) method inference_on_ta(docta, new_view_name) that takes a text annotation and view name,
    # creates the view in the text annotation, and returns it.
    # See the DummyModel class for a minimal example.
    # here the local pipeline is used to create the initial text annotation, best for pretokenized cases, like non-English
    wrapper = ModelWrapperServerLocal(model=model, provided_view="DUMMYVIEW", required_views=["TOKENS", "NER_CONLL"])
    # here the remote pipeline is used to create the initial text annotation, best for English handling demos
    # wrapper = ModelWrapperServerRemote(model=model, provided_view="DUMMYVIEW", required_views=["TOKENS", "NER_CONLL"])
    app.add_url_rule(rule='/annotate', endpoint='annotate', view_func=wrapper.annotate, methods=['GET'])
    app.run(host='localhost', port=5000)
    # On running this main(), you should be able to visit the following URL and see a json text annotation returned
    # http://127.0.0.1:5000/annotate?text="Stephen Mayhew is a person's name"&views=DUMMYVIEW


if __name__ == "__main__":
    main()
