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


LOG = logging.getLogger(__name__)

FLAGS = flags.FLAGS

class HealthMonitorNodeManager(manager.Manager):
    BASE_RPC_API_VERSION = '1.0'

    def __init__(self, topic=None):
        self.topic = "health_monitor_node"

    def init_host(self):

#        context = nova.context.get_admin_context()
#        instances = self.db.instance_get_all_by_host(context, self.host)

        pass


    def _init_monitors_connections(self):

        node_topic = '%s.%s' % (self.topic, self.host)

        self.conn = rpc.create_connection(new=True)
        LOG.debug(_("Creating Consumer connection for Service %s") % node_topic)

        rpc_dispatcher = self.create_rpc_dispatcher()

        self.conn.create_consumer(node_topic, rpc_dispatcher, fanout=False)

        # Consume from all consumers in a thread
        self.conn.consume_in_thread()

    def periodic_tasks(self, context, raise_on_error=False):
        pass


    def collect_recent_stats(self, ctxt, message, topic, version=None):

#        vmName = message.vmName;
#        statsParams = message.statsParams

        return "Collect stats"