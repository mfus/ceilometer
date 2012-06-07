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
"""Compute the signature of a metering message.
"""

import hashlib
import hmac
import uuid

from ceilometer import cfg

METER_OPTS = [
    cfg.StrOpt('metering_secret',
               default='change this or be hacked',
               help='Secret value for signing metering messages',
               ),
    cfg.StrOpt('metering_topic',
               default='metering',
               help='the topic ceilometer uses for metering messages',
               ),
    ]

cfg.CONF.register_opts(METER_OPTS)


def compute_signature(message):
    """Return the signature for a message dictionary.
    """
    digest_maker = hmac.new(cfg.CONF.metering_secret, '', hashlib.sha256)
    for name, value in sorted(message.iteritems()):
        if name == 'message_signature':
            # Skip any existing signature value, which would not have
            # been part of the original message.
            continue
        digest_maker.update(name)
        digest_maker.update(unicode(value).encode('utf-8'))
    return digest_maker.hexdigest()


def meter_message_from_counter(counter):
    """Make a metering message ready to be published or stored.

    Returns a dictionary containing a metering message
    for a notification message and a Counter instance.
    """
    msg = {'source': counter.source,
           'counter_name': counter.name,
           'counter_type': counter.type,
           'counter_volume': counter.volume,
           'user_id': counter.user_id,
           'project_id': counter.project_id,
           'resource_id': counter.resource_id,
           'timestamp': counter.timestamp,
           'counter_duration': counter.duration,
           'resource_metadata': counter.resource_metadata,
           'message_id': str(uuid.uuid1()),
           # This field is used by the notification system.
           'event_type': '%s.%s' % (cfg.CONF.metering_topic, counter.type),
           }
    msg['message_signature'] = compute_signature(msg)
    return msg
