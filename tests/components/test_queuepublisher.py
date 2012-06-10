from nova import context
from nova import rpc
from nova import test

from ceilometer.components.queuepublisher import QueuePublisher
from ceilometer import counter

class TestRunTasks(test.TestCase):

    def setUp(self):
        super(TestRunTasks, self).setUp()
        self.notifications = []
        self.stubs.Set(rpc, 'cast', self.faux_notify)
        self.ctx = context.RequestContext("user", "project")

    def faux_notify(self, context, topic, msg):
        self.notifications.append((topic, msg))

    def test_construct(self):
        publisher = QueuePublisher(self.ctx)
        assert publisher != None , "Error during QueuePublisher creation"

    def test_publish_data(self):
        publisher = QueuePublisher(self.ctx)
        publisher.init_publisher(queue_topic='myTopic')

        TEST_COUNTER = counter.Counter(source='src',
            type='typ',
            volume=1,
            user_id='user',
            project_id='project',
            resource_id=2,
            timestamp='today',
            duration=3,
            resource_metadata={'key': 'value'},
        )

        publisher.publish_data(TEST_COUNTER, "message")

        assert len(self.notifications) == 2
        self.notifications = []
