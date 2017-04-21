Additional Notes for Developers
===============================

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

  >>> pip install git+https://github.com/CogComp/sioux.git

To build your code::

  >>> python setup.py build

To test your code (runs against modules in the repository)::

  >>> python setup.py test

To install package locally and run the test::

  >>> pip install .
  >>> pytest

The `pytest` command discovers all unit tests and runs them against the installed `sioux` package.

**Note**: Do not create *__init__.py* files inside the *tests/* directory. `Read more. <http://doc.pytest.org/en/latest/goodpractices.html>`_

Versionining
------------

We use the `bumpversion <https://github.com/peritus/bumpversion>`_ python plugin to increment package version. Package version information is stored in `sioux/version.py`.

Update version using the following command in the root directory. Replace <part> with `patch`, `minor` or `major` accordingly.

  >>> bumpversion <part> sioux/version.py

Note: The bumpversion command also creates a commit with the version change. You can run it with a :code:`--dry-run --verbose` option to verify changes.
