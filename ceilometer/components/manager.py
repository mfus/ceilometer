__author__ = 'michal'

import pkg_resources
from nova import manager

from ceilometer import log



LOG = log.getLogger(__name__)
MONITOR_PLUGIN_NAMESPACE = 'ceilometer.monitor'

class AbstractManager(manager.Manager):

    monitors = []

    def _load_monitors(self, namespace):
        """Loads data processors - objects which are processing metering data locally.

            These objects control messages flow and for example send them through queue.
        """

        self.monitors = []
        for ep in pkg_resources.iter_entry_points(namespace):
            LOG.info('attempting to load metering monitor %s:%s', namespace, ep.name)
            try:
                processor_plugin_class = ep.load()
                processor_plugin = processor_plugin_class()

                self.monitors.append((ep.name, processor_plugin))
            except Exception as err:
                LOG.warning('Failed to load monitor %s:%s',ep.name, err)

        if not self.monitors:
            LOG.warning('Failed to load any monitor for %s', namespace)

        return

    def publish_counter(self, counter):

        for monitor in self.monitors:
            try:
                LOG.info('monitor %s', monitor)
                monitor.process(counter)
            except Exception as err:
                LOG.warning('Continuing after error from %s: %s', monitor, err)
                LOG.exception(err)





