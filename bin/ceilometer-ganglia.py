import eventlet
#eventlet.monkey_patch()
import sys

from ceilometer.service import prepare_service
from ceilometer.openstack.common import cfg
from nova import service
from nova.compute import manager as compute_manager

from nova import utils


if __name__ == '__main__':

    # Register the compute options from nova with our config object so
    # our pollsters can figure out which compute driver the hypervisor
    # is using.

    print "przed config\n"

    cfg.CONF.register_opts(compute_manager.compute_opts)

    print "po config"

    prepare_service(sys.argv)

    utils.monkey_patch()
	
    server =\
    service.Service.create(
        binary='ceilometer-ganglia',
        topic='ceilometer.ganglia',
        manager='ceilometer.ganglia.manager.GangliaManager',
        periodic_interval=None)
    service.serve(server)
    service.wait()
