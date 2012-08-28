from nova import log as logging
from nova import rpc

from ceilometer import meter
from ceilometer import counter

from ceilometer.publish import PublisherBase

LOG = logging.getLogger('nova.' + __name__)

class QueuePublisher(PublisherBase):

    QUEUE_TOPIC_ARG = 'topic'

    def __init__(self, context, **kwargs):
        self.context = context
        if kwargs.has_key(self.QUEUE_TOPIC_ARG):
            self.topic = kwargs[self.QUEUE_TOPIC_ARG]
        else:
            self.topic = None

    def publish_data(self, data):

        if isinstance(data, counter.Counter):
            self._publish_counter(self.context, data)
        else:
            LOG.debug('Bad argument passed. Expected ceilometer.counter:Counter, received ' + str(type(data)))

    def message_from_data(self, raw_data):

        msg = {
            'method': 'record_metering_data',
            'version': '1.0',
            'args': {'data': meter.meter_message_from_counter(raw_data),
                     },
            }

        return msg

    def _publish_counter(self, context, counter):
        """Send a metering message for the data represented by the counter.

        :param context: Execution context from the service or RPC call
        :param counter: ceilometer.counter.Counter instance
        """
        msg = self.message_from_data(counter)

        LOG.debug('PUBLISH: %s', str(msg))
        rpc.cast(context, self.topic, msg)
        rpc.cast(context,
            self.topic + '.' + counter.name,
            msg)
