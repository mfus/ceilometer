from ceilometer.openstack.common import log
from jsonrpc2_zeromq import RPCNotificationServer


LOG = log.getLogger(__name__)

class JsonServer(RPCNotificationServer):

    _update_configuration = False

    def handle_update_stats_method(self, stats):
        """ New stats from Ganglia
        :param stats: new stats
        :type stats: Dict
        """

        LOG.log('No method has been assigned to handle incoming messages')
        raise Exception('No method has been assigned to handle incoming messages')

    def handle_update_ganglia_configuration_method(self, configuration):
        print str(configuration)
        self._update_configuration = False
        self.cfg = configuration

    def update_ganglia_configuration(self):
        self._update_configuration = True
