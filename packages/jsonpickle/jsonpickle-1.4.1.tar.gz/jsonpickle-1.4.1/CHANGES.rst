v1.4.1
======
    * Patch release for Python 3.8 `importlib_metadata` support.
      (`#300 <https://github.com/jsonpickle/jsonpickle/issues/300>`_)

v1.4
====
    * Python 3.8 support.
      (`#292 <https://github.com/jsonpickle/jsonpickle/issues/292>`_)
    * ``jsonpickle.encode`` now supports the standard ``indent``
      and ``separators`` arguments, and passes them through to the
      active JSON backend library.
      (`#183 <https://github.com/jsonpickle/jsonpickle/issues/183>`_)
    * We now include a custom handler for `array.array` objects.
      (`#199 <https://github.com/jsonpickle/jsonpickle/issues/199>`_)
    * Dict key order is preserved when pickling dictionaries on Python3.
      (`#193 <https://github.com/jsonpickle/jsonpickle/issues/193>`_)
    * Improved serialization of dictionaries with non-string keys.
      Previously, using an enum that was both the key and a value in
      a dictionary could end up with incorrect references to other
      objects.  The references are now properly maintained for dicts
      with object keys that are also referenced in the dict's values.
      (`#286 <https://github.com/jsonpickle/jsonpickle/issues/286>`_)

    * Improved serialization of pandas.Series objects.
      (`#287 <https://github.com/jsonpickle/jsonpickle/issues/287>`_)

v1.3
====
    * Improved round tripping of default dicts.
      (`#283 <https://github.com/jsonpickle/jsonpickle/pull/283>`_)
      (`#282 <https://github.com/jsonpickle/jsonpickle/issues/282>`_)

    * Better support for cyclical references when encoding with
      ``unpicklable=False``.
      (`#264 <https://github.com/jsonpickle/jsonpickle/pull/264>`_)

v1.2
====
    * Simplified JSON representation for `__reduce__` values.
      (`#261 <https://github.com/jsonpickle/jsonpickle/pull/261>`_)

    * Improved Pandas support with new handlers for more Pandas data types.
      (`#256 <https://github.com/jsonpickle/jsonpickle/pull/256>`_)

    * Prevent stack overflows caused by bugs in user-defined `__getstate__`
      functions which cause infinite recursion.
      (`#260 <https://github.com/jsonpickle/jsonpickle/pull/260>`_)
      (`#259 <https://github.com/jsonpickle/jsonpickle/issues/259>`_)

    * Improved support for objects that contain dicts with Integer keys.
      Previously, jsonpickle could not restore objects that contained
      dicts with integer keys and provided getstate only.
      These objects are now handled robustly.
      (`#247 <https://github.com/jsonpickle/jsonpickle/issues/247>`_).

    * Support for encoding binary data in `base85`_ instead of base64 has been
      added on Python 3. Base85 produces payloads about 10% smaller than base64,
      albeit at the cost of lower throughput.  For performance and backwards
      compatibility with Python 2 the pickler uses base64 by default, but it can
      be configured to use ``base85`` with the new ``use_base85`` argument.
      (`#251 <https://github.com/jsonpickle/jsonpickle/issues/251>`_).

    * Dynamic SQLAlchemy tables in SQLAlchemy >= 1.3 are now supported.
      (`#254 <https://github.com/jsonpickle/jsonpickle/issues/254>`_).

.. _base85: https://en.wikipedia.org/wiki/Ascii85


v1.1
====
    * Python 3.7 `collections.Iterator` deprecation warnings have been fixed.
      (`#229 <https://github.com/jsonpickle/jsonpickle/issues/229>`_).

    * Improved Pandas support for datetime and complex numbers.
      (`#245 <https://github.com/jsonpickle/jsonpickle/pull/245>`_)

v1.0
====
    * *NOTE* jsonpickle no longer supports Python2.6, or Python3 < 3.4.
      The officially supported Python versions are now 2.7 and 3.4+.

    * Improved Pandas and Numpy support.
      (`#227 <https://github.com/jsonpickle/jsonpickle/pull/227>`_)

    * Improved support for pickling iterators.
      (`#216 <https://github.com/jsonpickle/jsonpickle/pull/216>`_)

    * Better support for the stdlib `json` module when `simplejson`
      is not installed.
      (`#217 <https://github.com/jsonpickle/jsonpickle/pull/217>`_)

    * jsonpickle will now output python3-style module names when
      pickling builtins methods or functions.
      (`#223 <https://github.com/jsonpickle/jsonpickle/pull/223>`_)

    * jsonpickle will always flatten primitives, even when ``max_depth``
      is reached, which avoids encoding unicode strings into their
      ``u'string'`` representation.

      (`#207 <https://github.com/jsonpickle/jsonpickle/pull/207>`_,
      `#180 <https://github.com/jsonpickle/jsonpickle/issues/180>`_,
      `#198 <https://github.com/jsonpickle/jsonpickle/issues/198>`_).

    * Nested classes are now supported on Python 3.
      (`#206 <https://github.com/jsonpickle/jsonpickle/pull/206>`_,
      `#176 <https://github.com/jsonpickle/jsonpickle/issues/176>`_).

    * Better support for older (pre-1.9) versions of numpy
      (`#195 <https://github.com/jsonpickle/jsonpickle/pull/195>`_).

v0.9.6
======
    * Better support for SQLAlchemy
      (`#180 <https://github.com/jsonpickle/jsonpickle/issues/180>`_).

    * Better support for NumPy and SciKit-Learn.
      (`#184 <https://github.com/jsonpickle/jsonpickle/issues/184>`_).

    * Better support for dict sub-classes
      (`#156 <https://github.com/jsonpickle/jsonpickle/issues/156>`_).

v0.9.5
======
    * Better support for objects that implement the reduce protocol.
      (`#170 <https://github.com/jsonpickle/jsonpickle/pull/170>`_).
      This backward-incompatible change removes the SimpleReduceHandler.
      Any projects registering that handler for a particular type should
      instead remove references to the handler and jsonpickle will now
      handle those types directly.

v0.9.4
======
    * Arbitrary byte streams are now better supported.
      (`#143 <https://github.com/jsonpickle/jsonpickle/issues/143>`_).

    * Better support for NumPy data types.  The Python3 NumPy support
      is especially robust.

    * Fortran-ordered based NumPy arrays are now properly serialized.

v0.9.3
======
    * UUID objects can now be serialized
      (`#130 <https://github.com/jsonpickle/jsonpickle/issues/130>`_).

    * Added `set_decoder_options` method to allow decoder specific options
      equal to `set_encoder_options`.

    * Int keys can be encoded directly by e.g. demjson by passing
      `numeric_keys=True` and setting its backend options via
      `jsonpickle.set_encoder_options('demjson', strict=False)`.

    * Newer Numpy versions (v1.10+) are now supported.

v0.9.2
======
    * Fixes for serializing objects with custom handlers.

    * We now properly serialize deque objects constructed with a `maxlen` parameter.

    * Test suite fixes

v0.9.1
======

    * Support datetime objects with FixedOffsets.

v0.9.0
======
    * Support for Pickle Protocol v4.

    * We now support serializing defaultdict subclasses that use `self`
      as their default factory.

    * We now have a decorator syntax for registering custom handlers,
      and allow custom handlers to register themselves for all subclasses.
      (`#104 <https://github.com/jsonpickle/jsonpickle/pull/104>`_).

    * We now support serializing types with metaclasses and their
      instances (e.g., Python 3 `enum`).

    * We now support serializing bytestrings in both Python 2 and Python 3.
      In Python 2, the `str` type is decoded to UTF-8 whenever possible and
      serialized as a true bytestring elsewise; in Python 3, bytestrings
      are explicitly encoded/decoded as bytestrings. Unicode strings are
      always encoded as is in both Python 2 and Python 3.

    * Added support for serializing numpy arrays, dtypes and scalars
      (see `jsonpickle.ext.numpy` module).

v0.8.0
======

    * We now support serializing objects that contain references to
      module-level functions
      (`#77 <https://github.com/jsonpickle/jsonpickle/issues/77>`_).

    * Better Pickle Protocol v2 support
      (`#78 <https://github.com/jsonpickle/jsonpickle/issues/78>`_).

    * Support for string __slots__ and iterable __slots__
      (`#67 <https://github.com/jsonpickle/jsonpickle/issues/66>`_)
      (`#68 <https://github.com/jsonpickle/jsonpickle/issues/67>`_).

    * `encode()` now has a `warn` option that makes jsonpickle emit warnings
      when encountering objects that cannot be pickled.

    * A Javascript implementation of jsonpickle is now included
      in the jsonpickleJS directory.

v0.7.2
======

    * We now properly serialize classes that inherit from classes
      that use `__slots__` and add additional slots in the derived class.
    * jsonpickle can now serialize objects that implement `__getstate__()` but
      not `__setstate__()`.  The result of `__getstate__()` is returned as-is
      when doing a round-trip from Python objects to jsonpickle and back.
    * Better support for collections.defaultdict with custom factories.
    * Added support for `queue.Queue` objects.

v0.7.1
======

    * Added support for Python 3.4.
    * Added support for :class:`posix.stat_result`.

v0.7.0
======

    * Added ``handles`` decorator to :class:`jsonpickle.handlers.BaseHandler`,
      enabling simple declaration of a handler for a class.
    * `__getstate__()` and `__setstate__()` are now honored
      when pickling objects that subclass :class:`dict`.
    * jsonpickle can now serialize :class:`collections.Counter` objects.
    * Object references are properly handled when using integer keys.
    * Object references are now supported when using custom handlers.
    * Decimal objects are supported in Python 3.
    * jsonpickle's "fallthrough-on-error" behavior can now be disabled.
    * Simpler API for registering custom handlers.
    * A new "safe-mode" is provided which avoids eval().
      Backwards-compatible deserialization of repr-serialized objects
      is disabled in this mode.  e.g. `decode(string, safe=True)`

v0.6.1
======

    * Python 3.2 support, and additional fixes for Python 3.

v0.6.0
======

    * Python 3 support!
    * :class:`time.struct_time` is now serialized using the built-in
      :class:`jsonpickle.handlers.SimpleReduceHandler`.

v0.5.0
======

    * Non-string dictionary keys (e.g. ints, objects) are now supported
      by passing `keys=True` to :func:`jsonpickle.encode` and
      :func:`jsonpickle.decode`.
    * We now support namedtuple, deque, and defaultdict.
    * Datetimes with timezones are now fully supported.
    * Better support for complicated structures e.g.
      datetime inside dicts.
    * jsonpickle added support for references and cyclical data structures
      in 0.4.0.  This can be disabled by passing `make_refs=False` to
      :func:`jsonpickle.encode`.

0.4.0
=====

    * Switch build from setuptools to distutils
    * Consistent dictionary key ordering
    * Fix areas with improper support for unpicklable=False
    * Added support for cyclical data structures
      (`#16 <https://github.com/jsonpickle/jsonpickle/issues/16>`_).
    * Experimental support for  `jsonlib <http://pypi.python.org/pypi/jsonlib/>`_
      and `py-yajl <http://github.com/rtyler/py-yajl/>`_ backends.
    * New contributers David K. Hess and Alec Thomas

    .. warning::

        To support cyclical data structures
        (`#16 <https://github.com/jsonpickle/jsonpickle/issues/16>`_),
        the storage format has been modified.  Efforts have been made to
        ensure backwards-compatibility.  jsonpickle 0.4.0 can read data
        encoded by jsonpickle 0.3.1, but earlier versions of jsonpickle may be
        unable to read data encoded by jsonpickle 0.4.0.


0.3.1
=====

    * Include tests and docs directories in sdist for distribution packages.

0.3.0
=====

    * Officially migrated to git from subversion. Project home now at
      `<http://jsonpickle.github.com/>`_. Thanks to Michael Jone's
      `sphinx-to-github <http://github.com/michaeljones/sphinx-to-github>`_.
    * Fortified jsonpickle against common error conditions.
    * Added support for:

     * List and set subclasses.
     * Objects with module references.
     * Newstyle classes with `__slots__`.
     * Objects implementing `__setstate__()` and `__getstate__()`
       (follows the :mod:`pickle` protocol).

    * Improved support for Zope objects via pre-fetch.
    * Support for user-defined serialization handlers via the
      jsonpickle.handlers registry.
    * Removed cjson support per John Millikin's recommendation.
    * General improvements to style, including :pep:`257` compliance and
      refactored project layout.
    * Steps towards Python 2.3 and Python 3 support.
    * New contributors Dan Buch and Ian Schenck.
    * Thanks also to Kieran Darcy, Eoghan Murray, and Antonin Hildebrand
      for their assistance!

0.2.0
=====

    * Support for all major Python JSON backends (including json in Python 2.6,
      simplejson, cjson, and demjson)
    * Handle several datetime objects using the repr() of the objects
      (Thanks to Antonin Hildebrand).
    * Sphinx documentation
    * Added support for recursive data structures
    * Unicode dict-keys support
    * Support for Google App Engine and Django
    * Tons of additional testing and bug reports (Antonin Hildebrand, Sorin,
      Roberto Saccon, Faber Fedor,
      `FirePython <http://github.com/darwin/firepython/tree/master>`_, and
      `Joose <http://code.google.com/p/joose-js/>`_)

0.1.0
=====

    * Added long as basic primitive (thanks Adam Fisk)
    * Prefer python-cjson to simplejson, if available
    * Major API change, use python-cjson's decode/encode instead of
      simplejson's load/loads/dump/dumps
    * Added benchmark.py to compare simplejson and python-cjson

0.0.5
=====

    * Changed prefix of special fields to conform with CouchDB
      requirements (Thanks Dean Landolt). Break backwards compatibility.
    * Moved to Google Code subversion
    * Fixed unit test imports

0.0.3
=====

    * Convert back to setup.py from pavement.py (issue found by spidaman)

0.0.2
=====

    * Handle feedparser's FeedParserDict
    * Converted project to Paver
    * Restructured directories
    * Increase test coverage

0.0.1
=====

    Initial release
