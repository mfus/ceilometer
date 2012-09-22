# -*- encoding: utf-8 -*-
#
# Copyright © 2012 eNovance <licensing@enovance.com>
#
# Author: Julien Danjou <julien@danjou.info>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pkg_resources

from nova import manager
from ceilometer.openstack.common import log
from nova.openstack.common import context
from nova.openstack.common import rpc

from ceilometer.reading import Reading
from ceilometer.ganglia.jsonServer import JsonServer
from ceilometer.ganglia.rpcapi import HealthMonitorNodeAPI
from novastats.rpcapi import HealthMonitorAPI
from ceilometer.ganglia import rulesmanager

LOG = log.getLogger(__name__)


GANGLIA_COLLECTOR_NAMESPACE = 'ceilometer.ganglia'


class GangliaManager(manager.Manager):

    handlers = {}

    def init_host(self):

	LOG.info("Attepmt to create JsonServer")

        connection_string = "tcp://127.0.0.1:90000" #TODO move to confguration file
        self.receiver = JsonServer(connection_string)
	self.receiver.start()
        self.receiver.handle_update_stats_method = self.received_stats_event
	
	LOG.info("Created jsonServer")

        self._create_connection()

	LOG.info("Established connection")	

        self.__rulesManager = rulesmanager.RulesManager()
	
	LOG.info("Attept to load plugins")

	self._load_plugins()

	LOG.info("Plugins loaded")

    def _load_plugins(self):
        # Listen for notifications from nova
        for ep in pkg_resources.iter_entry_points(GANGLIA_COLLECTOR_NAMESPACE):
            LOG.info('attempting to load notification handler for %s:%s', GANGLIA_COLLECTOR_NAMESPACE, ep.name)
            try:
                plugin_class = ep.load()
                plugin = plugin_class()
                # FIXME(dhellmann): Currently assumes all plugins are
                # enabled when they are discovered and
                # importable. Need to add check against global
                # configuration flag and check that asks the plugin if
                # it should be enabled.
                for event_type in plugin.get_event_types():
                    LOG.info('subscribing %s handler to %s events', ep.name, event_type)
                    self.handlers.setdefault(event_type, []).append(plugin)
            except Exception as err:
                LOG.warning('Failed to load notification handler %s: %s', ep.name, err)
                LOG.exception(err)
        if not self.handlers:
            LOG.warning('Failed to load any notification handlers for %s', GANGLIA_COLLECTOR_NAMESPACE)

    def _create_connection(self):
        self.ctx = context.get_admin_context()
        self.ctx.read_deleted = "no"
        self.instances = self.db.instance_get_all_by_host(self.ctx, self.host)

        node_topic = '%s.%s' % (HealthMonitorNodeAPI.HEALTH_MONITOR_NODE_TOPIC, self.host)
        self.conn = rpc.create_connection(new=True)

        LOG.debug(("Creating Consumer connection for Service %s") % node_topic)

        rpc_dispatcher = self.create_rpc_dispatcher()
        self.conn.create_consumer(node_topic, rpc_dispatcher, fanout=False)

        self.conn.consume_in_thread()

        self.health_rpc_api = HealthMonitorAPI()


    def _publish_reading(self, reading):
        LOG.info(self.health_rpc_api.topic)
        try:
            result = self.health_rpc_api.raise_alert(self.ctx, alert={ "Severity" :  reading.Alert, "Value" : reading })
        except Exception as err:
            LOG.error("%s" % err)
        LOG.info("sent")
        pass


    def received_stats_event(self, data):
        """This method is triggered when metering data is
        cast from an agent.
        """

        r = Reading(data)
        event_type = r.EventType

        LOG.info('NOTIFICATION: %s', event_type)
        for handler in self.handlers.get(event_type, []):
            for c in handler.process_notification(r):
                if self.__rulesManager.validateAgainstRules(c) != rulesmanager.Valid:
                    LOG.info('READING: %s', c)
                    self._publish_reading(c)
        return

