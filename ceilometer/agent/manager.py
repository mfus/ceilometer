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

from nova import log as logging
from nova import manager
from nova import rpc

from ceilometer import meter
from ceilometer import cfg


# FIXME(dhellmann): We need to have the main program set up logging
# correctly so messages from modules outside of the nova package
# appear in the output.
LOG = logging.getLogger('nova.' + __name__)

COMPUTE_PLUGIN_NAMESPACE = 'ceilometer.poll.compute'
PROCESSOR_PLUGIN_NAMESPACE = 'ceilometer.metering.processors'
PUBLISHER_PLUGIN_NAMESPACE = 'ceilometer.publishers'

class AgentManager(manager.Manager):

    pollsters = []
    publishers = []
    processors = []

    def init_host(self):
        self._load_plugins()
        self._load_data_processors()
        self._hook_data_processors_with_plugins_and_publishers()
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

    def _load_data_processors(self):
        """Loads data processors - objects which are processing metering data locally.

            These objects control messages flow and for example send them through queue.
        """

        self.processors = []
        for ep in pkg_resources.iter_entry_points(PROCESSOR_PLUGIN_NAMESPACE):
            LOG.info('attempting to load metering data processor %s:%s', PROCESSOR_PLUGIN_NAMESPACE, ep.name)
            try:
                processor_plugin_class = ep.load()
                processor_plugin = processor_plugin_class()

                self.processors.append((ep.name, processor_plugin))
            except Exception as err:
                LOG.warning('Failed to load processor %s:%s',
                    ep.name, err)

        if not self.processors:
            LOG.warning('Failed to load any processors for %s',
                PROCESSOR_PLUGIN_NAMESPACE)
        return


    def _hook_data_processors_with_plugins_and_publishers(self):
        """Hooks objects which are processing metering data
            with plugins (local metering data collectors)
            and publishers (objects which are publishing data to external sources)."""

        for name, processor in self.processors:
            processor.pollsters = self.pollsters
            processor.publishers = self.publishers


    def periodic_tasks(self, context, raise_on_error=False):
        """Tasks to be run at a periodic interval."""
        for name, pollster in self.pollsters:
            try:
                LOG.info('polling %s', name)
                for c in pollster.get_counters(self, context):
                    LOG.info('COUNTER: %s', c)
                    msg = {
                        'method': 'record_metering_data',
                        'version': '1.0',
                        'args': {'data': meter.meter_message_from_counter(c),
                                 },
                        }
                    rpc.cast(context, cfg.CONF.metering_topic, msg)
                    rpc.cast(context,
                             cfg.CONF.metering_topic + '.' + c.type,
                             msg)
            except Exception as err:
                LOG.warning('Continuing after error from %s: %s', name, err)
                LOG.exception(err)
