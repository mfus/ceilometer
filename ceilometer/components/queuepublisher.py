from publishers import PublisherBase

from nova import flags
from nova import log as logging
from nova import rpc

FLAGS = flags.FLAGS

LOG = logging.getLogger('nova.' + __name__)

QUEUE_TOPIC_ARG = 'queue_topic'

class QueuePublisher(PublisherBase):

    def __init__(self, context):
        self.context = context

    def publish_data(self, counting, message):
        pass

    def init_publisher(self, **kwargs):
        if kwargs.has_key(QUEUE_TOPIC_ARG):
            topic = kwargs[QUEUE_TOPIC_ARG]
        else:
            topic = None

        def publish_data_to_topic(counting, msg):
            try:
                rpc.cast(self.context, topic, msg)
                rpc.cast(self.context, topic + '.' + counting.type, msg)
            except Exception as err:
#                LOG.warning('Continuing after error from %s: %s', name, err)
                LOG.exception(err)

        self.publish_data = publish_data_to_topic
