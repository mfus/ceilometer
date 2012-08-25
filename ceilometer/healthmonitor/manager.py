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

from nova import flags
from nova import manager
from nova.scheduler import rpcapi
from nova.openstack.common import cfg
from nova.openstack.common import importutils
from nova.openstack.common import log as logging
from nova.openstack.common import rpc
from nova.openstack.common import context

from novastats.rpcapi import HealthMonitorAPI
from ceilometer.healthmonitor.rpcapi import HealthMonitorNodeAPI

#LOG = logging.getLogger(__name__)
LOG = logging.getLogger("health-monitor-node")
LOG.info(__name__)

FLAGS = flags.FLAGS

class HealthMonitorNodeManager(manager.Manager):
    BASE_RPC_API_VERSION = '1.0'

#    def __init__(self, topic=None):
#        self.topic = "health_monitor_node"

    def init_host(self):
        #self.topic = "health_monitor_node" - Initialized in bin/health-monitor-node.py
        self.ctx = context.get_admin_context()
        self.ctx.read_deleted = "no"
        self.instances = self.db.instance_get_all_by_host(self.ctx, self.host)
        
        self._init_monitors_connections()

        self.health_rpc_api = HealthMonitorAPI()
        self._test_rpc()
        
        
    def _test_rpc(self):
        LOG.info(self.health_rpc_api.topic)
        try:
            result = self.health_rpc_api.raise_alert(self.ctx, alert={"a" : "x"})
        except Exception as err:
            LOG.error("%s" % err)
        LOG.info("sent")
        pass        

    def _init_monitors_connections(self):

        node_topic = '%s.%s' % (HealthMonitorNodeAPI.HEALTH_MONITOR_NODE_TOPIC, self.host)

        self.conn = rpc.create_connection(new=True)
        LOG.debug(_("Creating Consumer connection for Service %s") % node_topic)

        rpc_dispatcher = self.create_rpc_dispatcher()
        self.conn.create_consumer(node_topic, rpc_dispatcher, fanout=False)

        # Consume from all consumers in a thread
        self.conn.consume_in_thread()
        

    def periodic_tasks(self, context, raise_on_error=False):
        pass


    def collect_recent_stats(self, ctxt=None, message=None):
        try:
            print message

            return "Collect stats"
        except Exception as err:
            print err
            return None