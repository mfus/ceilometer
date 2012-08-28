import abc

from ceilometer import log
from ceilometer import cfg
from ceilometer.components.queuepublisher import QueuePublisher
from ceilometer import publish
from nova import context

from ceilometer.components import rulesmanager

LOG = log.getLogger(__name__)

class MeteringDataMonitorBase(object):
    """Base class for metering data processors.

        Connects pollsters, publisher and mechanism how and when pull and publish metering data.

        Example use case:
            - fetch metering data from pollsters
            - send proper message through default publisher (queue ex. RabbitMQ)
    """
    __metaclass__ = abc.ABCMeta

    pollsters = []

    publisher = None

    def __init__(self, context):
        self.context = context

    @abc.abstractmethod
    def filter_pollsters(self, pollster):
        """Filter pollsters"""

    def set_pollsters(self, pollsters):
        """Set pollsters

            :param pollsters: List with pollsters (name, pollster)
        """

        self.pollsters = filter(self.filter_pollsters, pollsters)


class BillingMonitor(MeteringDataMonitorBase):
    """Simple billing processor. Pulls metering data from pollsters and sends them through publisher (ex. RabbitMq)
    """

    def __init__(self, context):
        super(BillingMonitor, self).__init__(context)
        self.publisher = QueuePublisher(self.context, {QueuePublisher.QUEUE_TOPIC_ARG: cfg.CONF.metering_topic})

    def periodic_tasks(self, context, raise_on_error=False):
        """Tasks to be run at a periodic interval."""
        for name, pollster in self.pollsters:
            try:
                LOG.info('polling %s', name)
                for counter in pollster.get_counters(self, context):
                    LOG.info('COUNTER: %s', counter)
                    self.publisher.publish_data(counter)
            except Exception as err:
                LOG.warning('Continuing after error from %s: %s', name, err)
                LOG.exception(err)


class CeilometerMonitor(object):

    def __init__(self):
        self.topic = cfg.CONF.metering_topic

    def publish_counter(self, counter):
        """Create a metering message for the counter and publish it."""

        ctx = context.get_admin_context()
        publish.publish_counter(ctx, counter, self.topic)

    def process(self, counter):
        self.publish_counter(counter)


class ValidationMonitor(object):

    def __init__(self):
        self.topic = 'Ceilometer'

    def __init__(self):
        self.rules = rulesmanager.RulesManager()

    def publish_counter(self, counter):
        """Create a metering message for the counter and publish it."""

        ctx = context.get_admin_context()
        publish.publish_counter(ctx, counter, self.topic)

    def process(self, counter):
        result = self.rules.validateAgainstRules(counter)

        if result != rulesmanager.Valid:
            self.publish_counter(counter)





