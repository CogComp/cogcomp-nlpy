Sioux 
====================
.. image:: http://morgoth.cs.illinois.edu:8080/buildStatus/icon?job=python-utils
    :target: http://morgoth.cs.illinois.edu:8080/job/python-utils/
.. image:: https://semaphoreci.com/api/v1/projects/dc68ab4d-d1b7-4405-adca-b0c6af2e1aa0/1223617/badge.svg
    :target: https://semaphoreci.com/danyaljj/sioux-2

Run NLP tools such as Part-of-Speech tagging, Chunking, Named Entity Recognition, etc on your documents in Python with ease and breeze! 

Installation
------------
1. Make sure `you have "pip" on your system <https://pip.pypa.io/en/stable/installing/>`_. 
2. Install: 

  pip install sioux

3. Enjoy!

**Note:** The package should be compatible with Python 2.6+ and Python 3.3+

**Upgrading:** If you want to update your package: 

   pip install --upgrade sioux

If you want to upgrade upgrade it on a specific version replace :code:`pip` in the command above with :code:`pip2` or :code:`pip3`. 

Getting Started 
-----------
Here is a sample usage showing how yeezily you run Sioux: 

.. code-block:: python

   from sioux import pipeliner

   pipeliner.init()
   doc = pipeliner.doc("Hello, how are you. I am doing fine")
   print(pipeliner.get_lemma(doc)) # will produce (hello Hello) (, ,) (how how) (be are) (you you) (. .) (i I) (be am) (do doing) (fine fine)
   print(pipeliner.get_pos(doc)) # will produce (UH Hello) (, ,) (WRB how) (VBP are) (PRP you) (. .) (PRP I) (VBP am) (VBG doing) (JJ fine)

The default/easy usage has some restrictions as will deliniate in the next section. See the next section to 

Structure   
----------------------------- 
Sioux enables you accesss `CogComp pipeline <https://github.com/CogComp/cogcomp-nlp/tree/master/pipeline>`_ in different forms. The figure below summarizes these approaches: 

.. figure:: https://cloud.githubusercontent.com/assets/2441454/24839367/ab7368e0-1d1e-11e7-98e9-cfc002a967aa.png
   :scale: 50 %

**(A) Use pipeline locally:** In this setting, Sioux will download the trained models and files required to run the pipeline locally. Since everything is run on your machine, it will probably require a lot of memory (the amount depends on which annotations you use). If you have a single big machine (i.e. memory > 15GB) for your expeirments, this is probably a good option for you. 

To download the models, run the following command:

  python -m sioux download

If you have downloaded the models through command :code:`python -m sioux download`, this tool will be running the pipeline locally, with all the annotators disabled.

**(B) Use pipeline server:** In this setting, Sioux sends calls to a remote machine. Hence there is not much memory burden on your system. Instead all the heavy-lifting is on the remote server. 

**(B.1) Default remote server:**  This is the deault setting in Sioux. The requests are sent to our remote server, hence requires a network connection. This option is there to demostrate how things work, but it is not a viable solution for your big experiments. If you are a busy nlp user, you have to use any of the other options. 

**(B.2) Start your own (remote) server:** If you have a big (remote) machine, this is probably a good option for you. 
You'll have to read the instructions on how to install the pipeline server in the [pipeline project documentation](https://github.com/CogComp/cogcomp-nlp/tree/master/pipeline#using-pipeline-webserver). In summary, you have to clone our ["Cogconp-NLP"](https://github.com/CogComp/cogcomp-nlp/) java project, and run `pipeline/scripts/runWebserver.sh` to initiates the server



By default,

* If you have downloaded the models through command :code:`python -m sioux download`, this tool will be running the pipeline locally (A), with all the annotators disabled.
* If you haven't downloaded the models, it will be communicating with a default remote pipeline server (B.1). 

If you want to change specific behaviors, such as activating or deactivating specific components, you can specify the parameters while initializing pipeliner module.

.. code-block:: python
   
   pipeliner.init(enable_views=['POS','LEMMA']) 
   # function declaration: init(use_server = None, server_api = None, enable_views = None, disable_views = None)
   # "use_server" will takes True/False. Will use local server (B), if False; otherwise will use the remote server (B). 
   # "server_api" is the address of the server as string. An example: http://www.fancyUrlName.com:8080
   # "enable_views" will takes a list of the view names to be used as strings, each string is the name of the view. This parameter is important only if you're using the local pipeline (A). 
 

**Note:** This tool is based on CogComp's `pipeline project <https://github.com/IllinoisCogComp/illinois-cogcomp-nlp/tree/master/pipeline>`_. Essentially annotator included in the pipeline should be accessible here. 
 
   
Setting from Configuration file 
---------------
You can set settings on how to run Sioux via a local option too, rather than setting it programmatically. 
Here is how to: 

.. code-block:: python

   pipeliner.init_from_file('path_to_custom_config_file')

   
The default keys and values (true/false) when models have been downloaded are specified below. If you want to use custom config file, please provide a file in similar format.


.. code-block:: bash

    [pipeline_setting]
    use_pipeline_server = false

    [views_setting]
    POS = false
    LEMMA = false
    NER_CONLL = false
    NER_ONTONOTES = false
    QUANTITIES = false
    SHALLOW_PARSE = false
    SRL_VERB = false
    DEPENDENCY_STANFORD = false
    DEPENDENCY = false
    PARSE_STANFORD = false
    SRL_PREP = false

    [pipeline_server]
    api = ADDRESS_OF_THE_SERVER # example: http://fancyUrlName.com:8080/
    

Loading TextAnnotation
-----------------------------
Documents stored as `TextAnnotation` can be read in the following formats:

- JSON

.. code-block:: python

    import sioux

    doc = sioux.load_document_from_json('text_annotation.json')
    print(doc.get_views())

- Protocol Buffers

.. code-block:: python

    import sioux

    doc = sioux.load_document_from_protobuf('text_annotation.pb')
    print(doc.get_views())

Development
-----------

For installing this package from Github repository, simply do::

  >>> pip install git+https://github.com/IllinoisCogComp/sioux.git

To build your code::
  
  >>> python setup.py build

To test your code (runs against modules in the repository)::
  
  >>> python setup.py test

To install package locally and run the test::

  >>> pip install .
  >>> pytest
  
The `pytest` command discovers all unit tests and runs them against the installed `sioux` package.

**Note**: Do not create *__init__.py* files inside the *tests/* directory. `Read more. <http://doc.pytest.org/en/latest/goodpractices.html>`_

Questions/Suggestions/Comments 
-------------- 
Use comments or pull requests. 

About the name 
-------------- 
It is pronounced similar to "Sue". The *Sioux* are groups of Native American tribes and First Nations peoples in North America, mostly the tribal governments scattered across North Dakota, South Dakota, Nebraska, Minnesota, and Montana in the United States; and Manitoba and southern Saskatchewan in Canada. (`Read more <https://en.wikipedia.org/wiki/Sioux>`_)


