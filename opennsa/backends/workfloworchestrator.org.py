"""
OpenNSA Pica8 OVS backend.

Authors:  SURFnet

"""

import random

from twisted.python import log
from twisted.internet import defer

from opennsa import constants as cnt, config
from opennsa.backends.common import genericbackend

LOG_SYSTEM = 'opennsa.workfloworchestrator'


class WorkflowOrchestratorCommandSender:


    def __init__(self):

        pass


    @defer.inlineCallbacks
    def _callPopulatorLightPathCreate(self, source_target, dest_target, bandwidth):

        import subprocess

        log.msg('_callPopulatorLightPathCreate(port %s vlan %s --> port %s vlan %s)' % (source_target.port, source_target.vlan, dest_target.port, dest_target.vlan), system=LOG_SYSTEM)
        yield subprocess.run(["true"])


    @defer.inlineCallbacks
    def _callPopulatorLightPathTerminate(self, source_target, dest_target, bandwidth):

        import subprocess

        log.msg('_callPopulatorLightPathTerminate(port %s vlan %s --> port %s vlan %s)' % (source_target.port, source_target.vlan, dest_target.port, dest_target.vlan), system=LOG_SYSTEM)
        yield subprocess.run(["true"])


    def setupLink(self, source_target, dest_target, bandwidth):

        return self._callPopulatorLightPathCreate(source_target, dest_target, bandwidth)


    def teardownLink(self, source_target, dest_target, bandwidth):

        return self._callPopulatorLightPathTerminate(source_target, dest_target, bandwidth)



class WorkflowOrchestratorTarget(object):

    def __init__(self, port, vlan=None):
        self.port = port
        self.vlan = vlan

    def __str__(self):
        if self.vlan:
            return '<WorkflowOrchestratorTarget %s#%i>' % (self.port, self.vlan)
        else:
            return '<WorkflowOrchestratorTarget %s>' % self.port



class WorkflowOrchestratorConnectionManager:

    def __init__(self, port_map):

        self.port_map = port_map
        self.command_sender = WorkflowOrchestratorCommandSender()


    def getResource(self, port, label):
        assert label is not None or label.type_ == cnt.ETHERNET_VLAN, 'Label type must be VLAN'
        # resource is port + vlan (router / virtual switching)
        label_value = '' if label is None else label.labelValue()
        return port + ':' + label_value


    def getTarget(self, port, label):
        assert label is not None and label.type_ == cnt.ETHERNET_VLAN, 'Label type must be VLAN'
        vlan = int(label.labelValue())
        assert 1 <= vlan <= 4095, 'Invalid label value for vlan: %s' % label.labelValue()

        return WorkflowOrchestratorTarget(self.port_map[port], vlan)


    def createConnectionId(self, source_target, dest_target):
        return 'orchestrator-' + str(random.randint(100000,999999))


    def canSwapLabel(self, label_type):
        return True


    def setupLink(self, connection_id, source_target, dest_target, bandwidth):

        def linkUp(_):
            log.msg('Link %s -> %s up' % (source_target, dest_target), system=LOG_SYSTEM)

        d = self.command_sender.setupLink(source_target, dest_target, bandwidth)
        d.addCallback(linkUp)
        return d


    def teardownLink(self, connection_id, source_target, dest_target, bandwidth):

        def linkDown(_):
            log.msg('Link %s -> %s down' % (source_target, dest_target), system=LOG_SYSTEM)

        d = self.command_sender.teardownLink(source_target, dest_target, bandwidth)
        d.addCallback(linkDown)
        return d



def Backend(network_name, nrm_ports, parent_requester, cfg):

    name = 'WorkflowOrchestrator %s' % network_name
    nrm_map  = dict( [ (p.name, p) for p in nrm_ports ] ) # for the generic backend
    port_map = dict( [ (p.name, p.interface) for p in nrm_ports ] ) # for the nrm backend

    # extract config items
    #host             = cfg[config.PICA8OVS_HOST]
    #port             = cfg.get(config.PICA8OVS_PORT, 22)
    #host_fingerprint = cfg[config.PICA8OVS_HOST_FINGERPRINT]
    #user             = cfg[config.PICA8OVS_USER]
    #ssh_public_key   = cfg[config.PICA8OVS_SSH_PUBLIC_KEY]
    #ssh_private_key  = cfg[config.PICA8OVS_SSH_PRIVATE_KEY]
    #db_ip            = cfg[config.PICA8OVS_DB_IP]

    cm = WorkflowOrchestratorConnectionManager(port_map)
    return genericbackend.GenericBackend(network_name, nrm_map, cm, parent_requester, name)
