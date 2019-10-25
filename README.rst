|Build Status|

Falcon ``multipart/form-data`` tests
====================================

This is a collection of extensive tests, long-running benchmarks and other
tests that are too specific to the development of the ``multipart/form-data``
media handler for `the Falcon web framework <https://falconframework.org>`_.

"Normal" functionality is covered with tests that are shipped with the feature
itself. At the time of writing, the multipart form handling code can be found
in the
`multipart-form-handler <https://github.com/vytas7/falcon/tree/multipart-form-handler>`_
branch.

This repository mainly focuses on streamlining three different scenarios:

* Wrapped part stream read throughput for large files.
* Tiny and/or buffer-misaligned reads.
* Multipart forms with an insane amount of parts (although completely contrived
  for all practical purposes, but that helps in opimizing per-part parsing
  overhead).


.. |Build Status| image:: https://api.travis-ci.org/vytas7/falcon-multipart-tests.svg
   :target: https://travis-ci.org/vytas7/falcon-multipart-tests
