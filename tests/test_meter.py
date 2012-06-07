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
"""Tests for ceilometer.meter
"""

from ceilometer import counter
from ceilometer import meter
from ceilometer import cfg


def test_compute_signature_change_key():
    sig1 = meter.compute_signature({'a': 'A', 'b': 'B'})
    sig2 = meter.compute_signature({'A': 'A', 'b': 'B'})
    assert sig1 != sig2


def test_compute_signature_change_value():
    sig1 = meter.compute_signature({'a': 'A', 'b': 'B'})
    sig2 = meter.compute_signature({'a': 'a', 'b': 'B'})
    assert sig1 != sig2


def test_compute_signature_same():
    sig1 = meter.compute_signature({'a': 'A', 'b': 'B'})
    sig2 = meter.compute_signature({'a': 'A', 'b': 'B'})
    assert sig1 == sig2


def test_compute_signature_signed():
    data = {'a': 'A', 'b': 'B'}
    sig1 = meter.compute_signature(data)
    data['message_signature'] = sig1
    sig2 = meter.compute_signature(data)
    assert sig1 == sig2


def test_compute_signature_use_configured_secret():
    data = {'a': 'A', 'b': 'B'}
    sig1 = meter.compute_signature(data)
    old_secret = cfg.CONF.metering_secret
    try:
        cfg.CONF.metering_secret = 'not the default value'
        sig2 = meter.compute_signature(data)
    finally:
        cfg.CONF.metering_secret = old_secret
    assert sig1 != sig2


TEST_COUNTER = counter.Counter(source='src',
                               name='name',
                               type='typ',
                               volume=1,
                               user_id='user',
                               project_id='project',
                               resource_id=2,
                               timestamp='today',
                               duration=3,
                               resource_metadata={'key': 'value'},
                               )

TEST_NOTICE = {
    u'_context_auth_token': u'3d8b13de1b7d499587dfc69b77dc09c2',
    u'_context_is_admin': True,
    u'_context_project_id': u'7c150a59fe714e6f9263774af9688f0e',
    u'_context_quota_class': None,
    u'_context_read_deleted': u'no',
    u'_context_remote_address': u'10.0.2.15',
    u'_context_request_id': u'req-d68b36e0-9233-467f-9afb-d81435d64d66',
    u'_context_roles': [u'admin'],
    u'_context_timestamp': u'2012-05-08T20:23:41.425105',
    u'_context_user_id': u'1e3ce043029547f1a61c1996d1a531a2',
    u'event_type': u'compute.instance.create.end',
    u'message_id': u'dae6f69c-00e0-41c0-b371-41ec3b7f4451',
    u'payload': {u'created_at': u'2012-05-08 20:23:41',
                 u'deleted_at': u'',
                 u'disk_gb': 0,
                 u'display_name': u'testme',
                 u'fixed_ips': [{u'address': u'10.0.0.2',
                                 u'floating_ips': [],
                                 u'meta': {},
                                 u'type': u'fixed',
                                 u'version': 4}],
                 u'image_ref_url': u'http://10.0.2.15:9292/images/UUID',
                 u'instance_id': u'9f9d01b9-4a58-4271-9e27-398b21ab20d1',
                 u'instance_type': u'm1.tiny',
                 u'instance_type_id': 2,
                 u'launched_at': u'2012-05-08 20:23:47.985999',
                 u'memory_mb': 512,
                 u'state': u'active',
                 u'state_description': u'',
                 u'tenant_id': u'7c150a59fe714e6f9263774af9688f0e',
                 u'user_id': u'1e3ce043029547f1a61c1996d1a531a2'},
    u'priority': u'INFO',
    u'publisher_id': u'compute.vagrant-precise',
    u'timestamp': u'2012-05-08 20:23:48.028195',
    }


def test_meter_message_from_counter_signed():
    msg = meter.meter_message_from_counter(TEST_COUNTER)
    assert 'message_signature' in msg


def test_meter_message_from_counter_event_type():
    msg = meter.meter_message_from_counter(TEST_COUNTER)
    assert msg['event_type'] == 'metering.' + TEST_COUNTER.type


def test_meter_message_from_counter_field():
    def compare(f, c, msg_f, msg):
        assert msg == c
    msg = meter.meter_message_from_counter(TEST_COUNTER)
    name_map = {'name': 'counter_name',
                'type': 'counter_type',
                'volume': 'counter_volume',
                'duration': 'counter_duration',
                }
    for f in TEST_COUNTER._fields:
        msg_f = name_map.get(f, f)
        yield compare, f, getattr(TEST_COUNTER, f), msg_f, msg[msg_f]
