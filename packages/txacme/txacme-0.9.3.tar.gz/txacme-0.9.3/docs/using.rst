Using txacme
============

There are several possible ways to make use of txacme:

* An issuing service for keeping certificates in a certificate store up to date;

* A server endpoint, which may be used anywhere an endpoint is accepted, that
  combines the issuing service with TLS SNI for certificate mapping;

* A server endpoint string parser, which can be used anywhere a server endpoint
  string es accepted, that produces a server endpoint.

While the server endpoint string parser is a convenient high-level API the
lower-level APIs (the issuing service and server endpoint) may be useful for
better integration with existing systems. For example, if the requirements for
storing certificates were more complex than a directory on a filesystem, one
might implement a certificate store that communicated with a REST webservice or
directly with a database and pass an instance of this to the server endpoint.


Server endpoint string
----------------------

Note: as of 09-Jan-2018, the Let's Encrypt server has indefinitely
`disabled`_ the ``tls-sni-01`` validation method needed by these endpoints
(for new sites), due to a security problem. A future ``txacme`` release might
reimplement these with a different validation method: see `Issue 129`_ for
details.

The simplest way to use txacme is the stream server endpoint string. Two endpoint
parsers are provided, under the ``le:`` (Let's Encrypt) and ``lets:`` (Let's
Encrypt Test in Staging) prefixes. The endpoint takes as parameters a directory
to store certificates in, and the underlying endpoint to listen on. One might
use the following command to start a Twisted web server on TCP port 443 and
store certificates in the ``/srv/www/certs`` directory:

.. code-block:: shell

   $ twistd -n web --port lets:/srv/www/certs:tcp:443 --path /srv/www/root

.. note:: The certificate directory must already exist, and be writable by the
   user the application is running as.

.. note:: The Let's Encrypt staging environment generates certificates signed
   by *Fake LE Intermediate X1*, but does not have the `stringent limits`_ that
   the production environment has, so using it for testing before switching to
   the production environment is highly recommended.

   .. _stringent limits: https://community.letsencrypt.org/t/rate-limits-for-lets-encrypt/6769
   .. _disabled: https://community.letsencrypt.org/t/important-what-you-need-to-know-about-tls-sni-validation-issues/50811
   .. _Issue 129: https://github.com/twisted/txacme/issues/129

The ACME client key will be stored in ``client.key`` in the certificate
directory, if this file does not exist a new key will automatically be
generated.

Certificates (and chain certificates and keys) in PEM format will be stored in
the certificate directory using filenames based on the servername that the
client sends by SNI, e.g. ``some.domain.name.pem``. The contents of the
directory are documented in more detail :doc:`here <certs-dir>`. If there is no
existing certificate available for a domain, an empty file should be created to
have one issued on startup; the behaviour is as if the certificate had expired.
Importantly, clients that do not perform SNI will not be able to connect to the
endpoint.

At startup, and every 24 hours, a check will be performed for expiring
certificates; if a certificate will expire in less than 30 days' time, it will
be reissued. If the reissue fails, it will be retried at the next check. If a
certificate will expire in less than 15 days' time, and reissue fails, a message
will be logged at *CRITICAL* level.

.. note:: This endpoint uses the ``tls-sni-01`` challenge type to perform
   authorization; this requires that the endpoint is reachable on port 443 for
   those domains (possibly via port forwarding).

Sharing certificates
~~~~~~~~~~~~~~~~~~~~

A certificate directory can be shared amongst multiple applications by using
``le:`` for the application running on port 443 to keep the certificates up to
date, and ``txsni:`` for other applications to make use of certificates in the
same directory.


Server endpoint
---------------

The endpoint can be instantiated directly as well; this allows extra
customizations beyond what the string syntax provides for. Most of the
parameters that can be passed correspond to the parameters of the `issuing
service`_.

.. autoclass:: txacme.endpoint.AutoTLSEndpoint
   :noindex:
   :members:


Issuing service
---------------

The `server endpoint`_ is a simple wrapper that combines the functionality of the
`txsni`_ endpoint for handling SNI, and the issuing service which takes care of
(re)issuing certificates using an ACME service.

.. autoclass:: txacme.service.AcmeIssuingService
   :noindex:
   :members:

The `~txacme.interfaces.ICertificateStore` and `~txacme.interfaces.IResponder`
interfaces are the main extension points for using the issuing service
directly. For example, a custom implementation of
`~txacme.interfaces.ICertificateStore` might manage the certificate
configuration of a cloud load balancer, implementing the ``dns-01`` challenge
type by modifying DNS entries in the cloud DNS configuration.

.. _txsni: https://github.com/glyph/txsni
