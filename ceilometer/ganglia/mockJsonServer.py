
from jsonrpc2_zeromq import RPCNotificationServer

class MockJsonServer(RPCNotificationServer):

    def initialize(self):

        f = open('home/michal/Pulpit/file.txt')
        list = f.readlines()

        for line in list:
            self.received_stats_event(line)

    def received_stats_event(self, data):
        """do nothing"""

    def handle_update_stats_method(self, stats):
        """ do nothing """

    def handle_update_ganglia_configuration_method(self, configuration):
        """do nothng"""

    def update_ganglia_configuration(self):
        """do nothng"""