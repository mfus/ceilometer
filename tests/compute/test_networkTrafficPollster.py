from nova import context
from nova import flags
from nova import test
from nova import db

from ceilometer.compute import traffic
from ceilometer.agent import manager

class TestNetworkTrafficPollster(test.TestCase):

    def setUp(self):
        self.context = context.RequestContext('admin', 'admin', is_admin=True) #not used
        self.manager = manager.AgentManager()
        self.pollster = traffic.NetworkTrafficPollster()
        super(TestNetworkTrafficPollster, self).setUp()

    def test_get_counters(self):
        # FIXME: Mock libvirt and instances.
        # FIXME: Right now to run and pass this test, there has to be 'instance-00000001' in local kvm..

        flags.FLAGS.connection_type = 'libvirt'

        instance = db.instance_create(self.context, {})
        self.mox.StubOutWithMock(self.manager.db, 'instance_get_all_by_host')
        self.manager.db.instance_get_all_by_host(self.context,self.manager.host,)\
                        .AndReturn([instance])

        self.mox.ReplayAll()

        counters = list(self.pollster.get_counters(self.manager, self.context))

        assert len(counters) > 0