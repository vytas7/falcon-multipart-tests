Falcon ``multipart/form-data`` tests
====================================

This is a collection of extensive tests, long-running benchmarks and other
tests that are too specific to the development of the ``multipart/form-data``
media handler for `the Falcon web framework <https://falconframework.org>`_.

"Normal" functionality is covered with tests that are shipped with the feature
itself. At the time of writing, the multipart form handling code can be found in
`the _multipart-form-handler-wip_ branch <https://github.com/vytas7/falcon/tree/multipart-form-handler-wip>`_.

This repository mainly focuses on streamlining three different scenarios:

* Wrapped part stream read throughput for large files.
* Tiny and/or buffer-misaligned reads.
* Multipart forms with an insane amount of parts (although completely contrived
  for the practical purposes, but that helps in opimizing per-part parsing
  overhead).
