# -*- encoding: utf-8 -*-
__docformat__ = 'restructuredtext en'

from ceilometer import plugin, reading
from ceilometer.ganglia.jsonServer import JsonServer

class GangliaPlugin(plugin.PollsterBase):
    """ Ganglia connector """

    def __init__(self):
        pass

    def init_queue(self):

        self.receiver = JsonServer(connection_address)
        self.receiver.handle_update_stats_method = self.received_stats_event

        #self.receiver.handle_update_ganglia_configuration_notification = self.update_ganglia_configuration

        try:
            self.receiver.start()
        except Exception as err:
            print err.message

    def get_rrds_directory(self):
        if not self.rrd_directory:
            self.rrd_directory = self.client.get_rrds_directory()

    def update_ganglia_configuration(self, configuration_json):
        """

        :param configuration_json: Json Ganglia's configuration
        :type configuration_json: Dict
        """
        self. rrd_directory = configuration_json.rrds_directory

    def received_stats_event(self, stats):
        """
        :param stats: Xml stats from Ganglia in Json array {"data" : "<xml data>"}
        :type stats: Dict
        """
        try:
            r = reading(stats)
        except :
            pass



        self.last_stats = stats.data
        self.notify_observer()

    def notify_observer(self):
        """
        Event. Notifies observer.
        """
        pass

    def get_counters(self, manager, context):

        if self.last_stats:
            return self.last_stats
        else:
            return None


if __name__ == "__main__":
    print "Starting"
    listener = GangliaPlugin()
    listener.init_queue()
    print "ops"
    listener.receiver.update_ganglia_configuration()

