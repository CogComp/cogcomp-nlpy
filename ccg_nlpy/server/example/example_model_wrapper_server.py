from flask import Flask
from flask_cors import CORS

from ccg_nlpy.server.example.dummy_annotator import DummyAnnotator
from ccg_nlpy.server.model_wrapper_server_local_pipeline import ModelWrapperServerLocal
from ccg_nlpy.server.model_wrapper_server_remote_pipeline import ModelWrapperServerRemote

app = Flask(__name__)
# necessary for testing on localhost
CORS(app)


def main():
    model = DummyAnnotator()  # create your model object here, see the DummyModel class for a minimal example.

    # here the local pipeline is used to create the initial text annotation, best for pretokenized cases, like non-English
    wrapper = ModelWrapperServerLocal(model=model)

    # here the remote pipeline is used to create the initial text annotation, best for English handling demos
    wrapper = ModelWrapperServerRemote(model=model)

    # Expose wrapper.annotate method through a Flask server
    app.add_url_rule(rule='/annotate', endpoint='annotate', view_func=wrapper.annotate, methods=['GET'])
    app.run(host='0.0.0.0', port=4003)
    # On running this main(), you should be able to visit the following URL and see a json text annotation returned
    # http://127.0.0.1:5000/annotate?text="Stephen Mayhew is a person's name"&views=DUMMYVIEW


if __name__ == "__main__":
    main()
