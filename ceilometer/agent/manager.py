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

from ceilometer.components import manager

from ceilometer import log


LOG = log.getLogger(__name__)

COMPUTE_PLUGIN_NAMESPACE = 'ceilometer.poll.compute'


class AgentManager(manager.AbstractManager):

    pollsters = []
    publishers = []

    def init_host(self):
        self._load_plugins()
        self._load_monitors(manager.MONITOR_PLUGIN_NAMESPACE)
        return

    def _load_plugins(self):
        self.pollsters = []
        for ep in pkg_resources.iter_entry_points(COMPUTE_PLUGIN_NAMESPACE):
            try:
                plugin_class = ep.load()
                plugin = plugin_class()
                # FIXME(dhellmann): Currently assumes all plugins are
                # enabled when they are discovered and
                # importable. Need to add check against global
                # configuration flag and check that asks the plugin if
                # it should be enabled.
                self.pollsters.append((ep.name, plugin))
                LOG.info('loaded pollster %s:%s',
                         COMPUTE_PLUGIN_NAMESPACE, ep.name)
            except Exception as err:
                LOG.warning('Failed to load pollster %s:%s',
                            ep.name, err)
                LOG.exception(err)
        if not self.pollsters:
            LOG.warning('Failed to load any pollsters for %s',
                        COMPUTE_PLUGIN_NAMESPACE)
        return

    def periodic_tasks(self, context, raise_on_error=False):
        """Tasks to be run at a periodic interval."""
        for name, pollster in self.pollsters:
            try:
                LOG.info('polling %s', name)
                for c in pollster.get_counters(self, context):
                    LOG.info('COUNTER: %s', c)
                    self.publish_counter(context, c)
            except Exception as err:
                LOG.warning('Continuing after error from %s: %s', name, err)
                LOG.exception(err)
