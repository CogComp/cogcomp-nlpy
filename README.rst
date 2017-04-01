Sioux 
====================
.. image:: http://morgoth.cs.illinois.edu:8080/buildStatus/icon?job=python-utils
    :target: http://morgoth.cs.illinois.edu:8080/job/python-utils/
.. image:: https://semaphoreci.com/api/v1/projects/dc68ab4d-d1b7-4405-adca-b0c6af2e1aa0/1223617/badge.svg
    :target: https://semaphoreci.com/danyaljj/sioux-2

Run NLP tools on your documents in Python with ease and breeze! 

Installation
------------
1. Make sure `you have "pip" on your system <https://pip.pypa.io/en/stable/installing/>`_. 
2. Install: 

  pip install sioux

3. Download additional models (if required).

  python -m sioux download

4. Enjoy!

**Note:** The package should be compatible with Python 2.6+ and Python 3.3+

**Upgrading:** If you want to update your package: 

   pip install --upgrade sioux

If you want to upgrade upgrade it on a specific version replace :code:`pip` in the command above with :code:`pip2` or :code:`pip3`. 

Sioux requires trained models to perform NLP tasks such as Part-of-Speech tagging, Chunking, Named Entity Recognition, Semantic Role Labeling etc. To download the models, run the following command:

  python -m sioux download

Usage 
-----------
Here is a sample usage showing how yeezily you run Sioux: 

.. code-block:: python

   from sioux import pipeliner

   doc = pipeliner.doc("Hello, how are you. I am doing fine")
   print(pipeliner.get_lemma(doc)) # will produce (hello Hello) (, ,) (how how) (be are) (you you) (. .) (i I) (be am) (do doing) (fine fine)
   print(pipeliner.get_pos(doc)) # will produce (UH Hello) (, ,) (WRB how) (VBP are) (PRP you) (. .) (PRP I) (VBP am) (VBG doing) (JJ fine)

Annotators 
---------- 
This tool is based on CogComp's `pipeline project <https://github.com/IllinoisCogComp/illinois-cogcomp-nlp/tree/master/pipeline>`_. Essentially anything included in the pipeline should be accessible here. 
Here is a few, as example 

- Tokenizing 
- Lemmatizing 
- Part of Spech tagging (POS) 
- Named Entity Recognition (NER)
- Semantic Role Labeling (SRL)
- ... 

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


