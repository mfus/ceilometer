# -*- encoding: utf-8 -*-
#
# Copyright © 2012 eNovance <licensing@enovance.com>
#
# Author: Julien Danjou <julien@danjou.info>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from nova import exception

from ceilometer.openstack.common import log

from .. import counter
from .. import plugin


class FloatingIPPollster(plugin.PollsterBase):

    LOG = log.getLogger(__name__ + '.floatingip')

    def get_counters(self, manager, context):
        try:
            ips = manager.db.floating_ip_get_all_by_host(context, manager.host)
        except exception.FloatingIpNotFoundForHost:
            pass
        else:
            for ip in ips:
                self.LOG.info("FLOATING IP USAGE: %s" % ip.address)
                yield counter.Counter(
                    source='?',
                    name='floating_ip',
                    type='delta',
                    volume=1,
                    user_id=None,
                    project_id=ip.project_id,
                    resource_id=ip.id,
                    timestamp=None,
                    duration=None,
                    resource_metadata={
                        'address': ip.address,
                        'fixed_ip_id': ip.fixed_ip_id,
                        'host': ip.host,
                        'pool': ip.pool,
                        'auto_assigned': ip.auto_assigned
                        })
