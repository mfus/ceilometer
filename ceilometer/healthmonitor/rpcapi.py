# -*- encoding: utf-8 -*-
__docformat__ = 'restructuredtext en'

import errno
import inspect
import os
import random
import signal
import sys
import time

import eventlet
import greenlet

from nova import context
from nova import flags
from nova import manager
from nova.scheduler import rpcapi
from nova.openstack.common import cfg
from nova.openstack.common import importutils
from nova.openstack.common import log as logging
from nova.openstack.common import rpc
from nova.openstack.common import context

import nova.openstack.common.rpc.proxy

LOG = logging.getLogger(__name__)

FLAGS = flags.FLAGS

class HealthMonitorNodeAPI(nova.openstack.common.rpc.proxy.RpcProxy):
    pass

    BASE_RPC_API_VERSION = '1.0'
    HEALTH_MONITOR_NODE_TOPIC = "health_monitor_node"

    @staticmethod
    def make_msg(method, **kwargs):
        return {'method': method, 'args': kwargs}

    def __init__(self, hostname): 
        
        node_topic = '%s.%s' % (HealthMonitorNodeAPI.HEALTH_MONITOR_NODE_TOPIC, hostname)
        
        super(HealthMonitorNodeAPI, self).__init__(
            topic=node_topic,
            default_version=self.BASE_RPC_API_VERSION)

    def collect_recent_stats(self, ctxt=None, message=None):
        return self.call(context=ctxt, 
                         msg=self.make_msg('collect_recent_stats', message=message), 
                         topic=self.topic, 
                         version=None)
