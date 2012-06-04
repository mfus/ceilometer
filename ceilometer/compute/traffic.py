import datetime

from nova import log as logging
from nova import flags
import nova.virt.connection

from .. import counter
from .. import plugin

FLAGS = flags.FLAGS
LOG = logging.getLogger('nova.' + __name__)

def make_counter_from_instance(instance, source, type, volume):
    return counter.Counter(
        source=source,
        type=type,
        volume=volume,
        user_id=instance.user_id,
        project_id=instance.project_id,
        resource_id=instance.uuid,
        timestamp=datetime.datetime.utcnow().isoformat(),
        duration=None,
        resource_metadata={
            'display_name': instance.display_name,
#            'instance_type': instance.instance_type.flavorid,
            'host': instance.host,
            },
    )

class NetworkTrafficPollster(plugin.PollsterBase):
    """Gets network in/out bytes from libvirt"""

    LOG = logging.getLogger('nova.' + __name__ + '.net')

    keys = ['rx_bytes' , 'rx_drop', 'rx_errs', 'rx_packets', 'tx_bytes', 'tx_drop', 'tx_errs', 'tx_packets']

    def get_counters(self, manager, context):

        conn = None
        if FLAGS.connection_type == 'libvirt':
            conn = nova.virt.connection.get_connection(read_only=True)

        for instance in manager.db.instance_get_all_by_host(context, manager.host):
            self.LOG.info('checking instance %s', instance.uuid)
            try:
                interfaces = conn.get_interfaces(instance.name)

                # interface_stats = [rx_bytes,
                #                    rx_drop,
                #                    rx_errs,
                #                    rx_packets,
                #                    tx_bytes,
                #                    tx_drop,
                #                    tx_errs,
                #                    tx_packets]

                for interface_name in interfaces:
                    try:
                        #FIXME: Use pcap to filter packages from virtual interface. Http/Tcp/ping etc.
                        interfaces_stats = dict(zip(NetworkTrafficPollster.keys,
                                    conn.interface_stats(instance.name, interface_name)
                                )
                            )

                        yield make_counter_from_instance(instance,
                            source=interface_name,
                            type='network',
                            volume= {'net_in_bytes' : interfaces_stats['rx_bytes'], 'net_out_bytes' : interfaces_stats['tx_bytes']}
                        )
                    except Exception as err:
                        self.LOG.error('Could not get Network stats for %s %s: %s',
                            instance.uuid, interface_name, err)
                        self.LOG.exception(err)

            except Exception as err:
                self.LOG.error('Could not get Network Stats for %s: %s',
                    instance.uuid, err)
                self.LOG.exception(err)
