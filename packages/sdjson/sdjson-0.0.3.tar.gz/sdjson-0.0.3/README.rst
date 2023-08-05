****************
sdjson
****************

.. image:: https://travis-ci.com/domdfcoding/singledispatch-json.svg?branch=master
    :target: https://travis-ci.com/domdfcoding/singledispatch-json
    :alt: Build Status
.. image:: https://readthedocs.org/projects/singledispatch-json/badge/?version=latest
    :target: https://singledispatch-json.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/sdjson.svg
    :target: https://pypi.org/project/sdjson/
    :alt: PyPI
.. image:: https://img.shields.io/pypi/pyversions/sdjson.svg
    :target: https://pypi.org/project/sdjson/
    :alt: PyPI - Python Version
.. image:: https://coveralls.io/repos/github/domdfcoding/sdjson/badge.svg?branch=master
    :target: https://coveralls.io/github/domdfcoding/sdjson?branch=master
    :alt: Coverage
.. image:: https://img.shields.io/pypi/l/sdjson
    :alt: PyPI - License
    :target: https://github.com/domdfcoding/singledispatch-json/blob/master/LICENSE

Custom JSON Encoder for Python utilising functools.singledispatch to support custom encoders
for both Python's built-in classes and user-created classes, without as much legwork.

Based on https://treyhunner.com/2013/09/singledispatch-json-serializer/ and Python's ``json`` module.

|

Usage
#########
Creating and registering a custom encoder is as easy as:

>>> import sdjson
>>>
>>> @sdjson.dump.register(MyClass)
>>> def encode_myclass(obj):
...     return dict(obj)
>>>

In this case, `MyClass` can be made JSON-serializable simply by calling
`dict()` on it. If your class requires more complicated logic
to make it JSON-serializable, do that here.

Then, to dump the object to a string:

>>> class_instance = MyClass()
>>> print(sdjson.dumps(class_instance))
'{"menu": ["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"],
"today\'s special": "Lobster Thermidor au Crevette with a Mornay sauce served in a Provencale
manner with shallots and aubergines garnished with truffle pate, brandy and with a fried egg
on top and spam."}'
>>>

Or to dump to a file:

>>> with open("spam.json", "w") as fp:
...     sdjson.dumps(class_instance, fp)
...
>>>

`sdjson` also provides access to ``load``, ``loads`, ``JSONDecoder``,
``JSONDecodeError``, and ``JSONEncoder`` from the ``json`` module,
allowing you to use ``sdjson`` as a drop-in replacement
for ``json``.

If you wish to dump an object without using the custom encoders, you
can pass a different ``JSONEncoder`` subclass, or indeed ``JSONEncoder``
itself to get the stock functionality.

>>> sdjson.dumps(class_instance, cls=sdjson.JSONEncoder)
>>>

.. note:: This module does not currently support custom decoders, but might in the future.
