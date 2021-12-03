# TLS/SSL Configuration


The configuration of TLS/SSL of OpenNSA is something that has confused several
people. This guide tries to make it more comprehensible. OpenNSA is somewhat
barebones in its configuration style, but uses standard X.509 certificates and
directory layouts. Prodding at TLS/SSL config until it works is usually a bad
strategy. Understand it, and it should be straightforward.

First you need to get a certificate. Please don't make a self-signed. Get one
from a real certificate authority. Many NRENs can get certificates from TERENA
or similar. These typically have guides as well and there is no purpose in
repeating it here.

OpenNSA or its author cannot magically produce a certificate you (sorry).

When you have obtained a certificate you should have a private key and a
certificate file (also contains the public key).


## Configuration Options 

`tls=true`
Enable TLS.

`key=/etc/hostcert/nsi.nordu.net.key`
Path to private key.

`certificate=/etc/hostcert/nsi.nordu.net.pem`
Path to the certificate.

`certdir=/etc/ssl/certs`
Directory for certificates authorities. OpenNSA uses the OpenSSL standard of seperate CA files ending with .0
Only files ending with .0 are loaded.

`verify=true`
If OpenNSA should verify the peer. You want this to true, unless debugging..

`allowedhosts=host1.example.org,host2.example.org`
Comma-seperated list of hosts that are allowed to make request to OpenNSA.


## Common Issues 

If you get:
AttributeError: 'OpenSSL.SSL.Context' object has no attribute 'set_session_cache_mode'

Upgrade pyOpenSSL to at least version 0.14 (as listed in the INSTALL file).


