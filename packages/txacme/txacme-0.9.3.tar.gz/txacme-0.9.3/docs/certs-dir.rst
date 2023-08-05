Certificates directory
======================

The layout of the certificates directory used by ``DirectoryStore`` (and thus
the ``le:`` and ``lets:`` endpoints) is coordinated with `txsni`_ to allow
sharing a certificates directory with other applications. The txsni and txacme
maintainers have committed to coordination of any future changes to the
contents of this directory to ensure continued compatibility.

.. _txsni: https://github.com/glyph/txsni

At present, the following entries may exist in this directory:

* ``<server name>.pem``

  A file containing a certificate and matching private key valid for ``<server
  name>``, serialized in PEM format.

* ``client.key``

  A file containing an ACME client key, serialized in PEM format.

All other filenames are currently reserved for future use; introducing
non-specified files or directories into a certificates directory may result in
conflicts with items specified by future versions of txacme and/or txsni.
