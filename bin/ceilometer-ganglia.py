import eventlet
eventlet.monkey_patch()
import sys

from ceilometer.service import prepare_service
from ceilometer.openstack.common import cfg
from nova import service
from nova.compute import manager as compute_manager


if __name__ == '__main__':

    # Register the compute options from nova with our config object so
    # our pollsters can figure out which compute driver the hypervisor
    # is using.
    cfg.CONF.register_opts(compute_manager.compute_opts)

    prepare_service(sys.argv)
    server =\
    service.Service.create(
        binary='ceilometer-ganglia',
        topic='ceilometer.ganglia',
        manager='ceilometer.ganglia.GangliaManager',
        periodic_interval=None)
    service.serve(server)
    service.wait()
