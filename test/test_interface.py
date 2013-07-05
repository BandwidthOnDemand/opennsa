from twisted.trial import unittest

from zope.interface.verify import verifyObject

from opennsa.interface import INSIProvider, INSIRequester

from opennsa import aggregator
from opennsa.backends.common import genericbackend
from opennsa.protocols.nsi2 import provider, requester


class FakeTopology:
    def __init__(self, name):
        self.name = name


class InterfaceTest(unittest.TestCase):

    def testGenericBackend(self):
        simple_backend = genericbackend.GenericBackend('network', FakeTopology('network'), None, None, None)
        verifyObject(INSIProvider, simple_backend)


    def testAggregator(self):
        aggr = aggregator.Aggregator('network', None, None, None, None)
        verifyObject(INSIProvider, aggr)
        verifyObject(INSIRequester, aggr)

    testAggregator.skip = 'aggregator not complete yet'

    def testSoapProvider(self):
        prov = provider.Provider(None, None)
        verifyObject(INSIRequester, prov)

    testSoapProvider.skip = 'provider not complete yet'


