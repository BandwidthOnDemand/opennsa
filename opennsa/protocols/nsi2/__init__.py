"""
Various protocol initialization.

Author: Henrik Thostrup Jensen <htj@nordu.net>
Copyright: NORDUnet (2011-2012)
"""

from twisted.web import resource, server

from opennsa.protocols.shared import resource as soapresource

from opennsa.protocols.nsi2 import providerservice, providerclient, provider, \
                                   requesterservice, requesterclient, requester



def setupProvider(child_provider, top_resource, tls=False, ctx_factory=None):

    soap_resource = soapresource.setupSOAPResource(top_resource, 'CS2')

    provider_client = providerclient.ProviderClient(ctx_factory)

    nsi2_provider = provider.Provider(child_provider, provider_client)

    providerservice.ProviderService(soap_resource, nsi2_provider)

    return nsi2_provider


def setupRequester(top_resource, host, port, providers, tls=False, ctx_factory=None, callback_timeout=None):

    resource_name = 'RequesterService2'

    # copied from nsi1.__init__
    def _createServiceURL(host, port, tls=False):
        proto_scheme = 'https://' if tls else 'http://'
        service_url = proto_scheme + '%s:%i/NSI/services/%s' % (host,port, resource_name)
        return service_url

    service_url = _createServiceURL(host, port, tls)

    soap_resource = soapresource.setupSOAPResource(top_resource, resource_name)

    requester_client = requesterclient.RequesterClient(providers, service_url)

    nsi_requester = requester.Requester(requester_client, callback_timeout=callback_timeout)

    requester_service = requesterservice.RequesterService(soap_resource, nsi_requester)

    return nsi_requester


# copied from nsi1.__init__
def createRequesterClient(host, port, providers, tls=False, ctx_factory=None, callback_timeout=None):

    top_resource = resource.Resource()
    nsi_requester = setupRequester(top_resource, host, port, providers, tls, ctx_factory, callback_timeout)
    site = server.Site(top_resource, logPath='/dev/null')
    return nsi_requester, site


