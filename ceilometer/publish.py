# -*- encoding: utf-8 -*-
#
# Copyright © 2012 New Dream Network, LLC (DreamHost)
#
# Author: Doug Hellmann <doug.hellmann@dreamhost.com>
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
"""Publish a counter using the preferred RPC mechanism.
"""

from nova import log as logging
from nova import rpc

from ceilometer import cfg
from ceilometer import meter

# FIXME(dhellmann): We need to have the main program set up logging
# correctly so messages from modules outside of the nova package
# appear in the output.
LOG = logging.getLogger('nova.' + __name__)


def publish_counter(context, counter):
    """Send a metering message for the data represented by the counter.

    :param context: Execution context from the service or RPC call
    :param counter: ceilometer.counter.Counter instance
    """
    msg = {
        'method': 'record_metering_data',
        'version': '1.0',
        'args': {'data': meter.meter_message_from_counter(counter),
                 },
        }
    LOG.debug('PUBLISH: %s', str(msg))
    rpc.cast(context, cfg.CONF.metering_topic, msg)
    rpc.cast(context,
             cfg.CONF.metering_topic + '.' + counter.name,
             msg)
