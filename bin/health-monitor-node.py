import eventlet
eventlet.monkey_patch()
import sys

from ceilometer.service import prepare_service
from ceilometer.openstack.common import cfg
from nova import service
from nova.compute import manager as compute_manager
from nova import flags
from nova.openstack.common import log as logging
from nova import utils

if __name__ == '__main__':

    # Register the compute options from nova with our config object so
    # our pollsters can figure out which compute driver the hypervisor
    # is using.
#    cfg.CONF.register_opts(compute_manager.compute_opts)

    try:
        logging.setup("health-monitor-node")
        LOG = logging.getLogger("health-monitor-node")
        LOG.logger.setLevel(10)
    except Exception as err:
        print err
    flags.parse_args(sys.argv)
    logging.setup("health-monitor-node")

#    prepare_service(sys.argv)
    flags.parse_args(sys.argv)
    utils.monkey_patch()
    try:
        server = service.Service.create(binary='health-monitor-node',
            topic='health_monitor_node',
            manager='ceilometer.healthmonitor.manager.HealthMonitorNodeManager',
            periodic_interval=None)
        service.serve(server)
        service.wait()
    except Exception as err:
        print err

