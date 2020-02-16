|Build Status|

Falcon ``multipart/form-data`` tests
====================================

This is a collection of extensive tests, long-running benchmarks and other
tests that are too specific to the development of the ``multipart/form-data``
media handler for `the Falcon web framework <https://falconframework.org>`_.

See also `this Gist <https://gist.github.com/vytas7/34c60e5ac3a4bc2f2eb0af2428d77003>`_
for design details, examples and progress updates.

"Normal" functionality is covered with tests that are shipped with the feature
itself. This repository mainly focuses on streamlining three different
scenarios:

* Wrapped part stream read throughput for large files.
* Tiny and/or buffer-misaligned reads.
* Multipart forms with an insane amount of parts (although completely contrived
  for all practical purposes, but that helps in opimizing per-part parsing
  overhead).


.. |Build Status| image:: https://api.travis-ci.org/vytas7/falcon-multipart-tests.svg
   :target: https://travis-ci.org/vytas7/falcon-multipart-tests
