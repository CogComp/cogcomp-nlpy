Sioux 
====================
.. image:: http://morgoth.cs.illinois.edu:8080/buildStatus/icon?job=python-utils
    :target: http://morgoth.cs.illinois.edu:8080/job/python-utils/
.. image:: https://semaphoreci.com/api/v1/projects/9266ef35-d407-40e1-893f-66fbdd38e9d9/1212440/badge.svg
    :target: https://semaphoreci.com/danyaljj/sioux

Run NLP tools on your documents in Python with ease and breeze! 

Installation
------------
1. Make sure `you have "pip" on your system <https://pip.pypa.io/en/stable/installing/>`_. 
2. Install: 
  >>> pip install sioux   
3. Enjoy! 

**Note:** The package should be compatible with Python 2.6+ and Python 3.3+

**Upgrading:** If you want to update your package: 

   pip install --upgrade sioux

If you want to upgrade upgrade it on a specific version replace :code:`pip` in the command above with :code:`pip2` or :code:`pip3`. 

Usage 
-----------
Here is a sample usage showing how yeezily you run Sioux: 

.. code-block:: python
   
   from sioux.pipeliner import Pipeliner
   p = Pipeliner()
   doc = p.doc("Hello, how are you. I am doing fine")
   print(p.get_lemma(doc).getCons()) # will produce ['hello', ',', 'how', 'be', 'you', '.', 'i', 'be', 'do', 'fine']
   print(p.get_pos(doc).getCons()) # will produce ['UH', ',', 'WRB', 'VBP', 'PRP', '.', 'PRP', 'VBP', 'VBG', 'JJ']

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

Development
-----------

For installing this package from Github repository, simply do::

  >>> pip install git+https://github.com/IllinoisCogComp/sioux.git

To build your code::
  
  >>> python setup.py build

To test your code::
  
  >>> python setup.py test

Questions/Suggestions/Comments 
-------------- 
Use comments or pull requests. 

About the name 
-------------- 
It is pronounced similar to "Sue". The *Sioux* are groups of Native American tribes and First Nations peoples in North America, mostly the tribal governments scattered across North Dakota, South Dakota, Nebraska, Minnesota, and Montana in the United States; and Manitoba and southern Saskatchewan in Canada. (`Read more <https://en.wikipedia.org/wiki/Sioux>`_)


