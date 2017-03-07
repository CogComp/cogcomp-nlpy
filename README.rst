Sioux 
====================
.. image:: http://morgoth.cs.illinois.edu:8080/buildStatus/icon?job=python-utils

Run NLP tools on your documents in Python with ease and breeze! 

Installation
------------
 1. Make sure `you have "pip" on your sysem <https://pip.pypa.io/en/stable/installing/>`_. 
 2. Install: 
 
  >>> pip install sioux 
 
 3. Enjoy! 

Here is a sample usage showing how yeezily you run Sioux: 

.. code-block:: python

   p = Pipeliner()
   doc = p.doc("Hello,  how are you. I am doing fine")
   pos_view = p.get_pos(doc)
   println(pos_view) 

Will print the following: 

  ???

**Note:** The package should be compatible with Python 2.6+ and Python 3.3+

Development
-----------

For installing this package from Github repository, simply do::

  >>> pip install git+https://github.com/IllinoisCogComp/python-utils.git

To build your code::
  
  >>> python setup.py build

To test your code::
  
  >>> python setup.py test


About the name 
-------------- 
The *Sioux* are groups of Native American tribes and First Nations peoples in North America, mostly the tribal governments scattered across North Dakota, South Dakota, Nebraska, Minnesota, and Montana in the United States; and Manitoba and southern Saskatchewan in Canada. (`Read more <https://en.wikipedia.org/wiki/Sioux>`_)


