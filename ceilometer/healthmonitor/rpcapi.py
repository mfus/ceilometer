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

    def __init__(self):
        super(HealthMonitorNodeAPI, self).__init__(
#            topic=FLAGS.health_monitor_node_topic,
            topic="health_monitor_node",
            default_version=self.BASE_RPC_API_VERSION)


    def collect_recent_stats(self, ctxt, message, topic):
        return self.call(context=ctxt, msg=message, topic=topic, version=None)
