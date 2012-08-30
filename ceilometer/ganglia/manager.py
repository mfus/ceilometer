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

from nova import flags
from ceilometer.components import manager

from ceilometer import log
from ceilometer.reading import Reading

from ceilometer.ganglia.jsonServer import JsonServer

FLAGS = flags.FLAGS
LOG = log.getLogger(__name__)


COMPUTE_COLLECTOR_NAMESPACE = 'ceilometer.ganglia.compute'


class CollectorManager(manager.AbstractManager):

    handlers = {}

    def init_host(self):
        connection_address = "tcp://127.0.0.1:90000" #TODO move to confguration file

        self.receiver = JsonServer(connection_address)
        self.receiver.handle_update_stats_method = self.received_stats_event


    def _load_plugins(self):
        # Listen for notifications from nova
        for ep in pkg_resources.iter_entry_points(COMPUTE_COLLECTOR_NAMESPACE):
            LOG.info('attempting to load notification handler for %s:%s', COMPUTE_COLLECTOR_NAMESPACE, ep.name)
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
            LOG.warning('Failed to load any notification handlers for %s', COMPUTE_COLLECTOR_NAMESPACE)


    def received_stats_event(self, data):
        """This method is triggered when metering data is
        cast from an agent.
        """

        r = Reading(data)
        event_type = r.EventType

        LOG.info('NOTIFICATION: %s', event_type)
        for handler in self.handlers.get(event_type, []):
            for c in handler.process_notification(data):
                LOG.info('COUNTER: %s', c)
                self.publish_counter(c)
        return

