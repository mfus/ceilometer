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
"""Tests for ceilometer/publish.py
"""

import datetime

from nova import context
from ceilometer.openstack.common import rpc
from nova import test

from ceilometer import counter
from ceilometer import publish


class TestPublish(test.TestCase):

    test_data = counter.Counter(
        source='test',
        name='test',
        type='cumulative',
        volume=1,
        user_id='test',
        project_id='test',
        resource_id='test_run_tasks',
        timestamp=datetime.datetime.utcnow().isoformat(),
        duration=0,
        resource_metadata={'name': 'TestPublish',
                           },
        )

    def faux_notify(self, context, topic, msg):
        self.notifications.append((topic, msg))

    def setUp(self):
        super(TestPublish, self).setUp()
        self.notifications = []
        self.stubs.Set(rpc, 'cast', self.faux_notify)
        self.ctx = context.RequestContext("user", "project")
        publish.publish_counter(self.ctx, self.test_data)

    def test_notify(self):
        assert len(self.notifications) == 2

    def test_notify_topics(self):
        topics = [n[0] for n in self.notifications]
        assert topics == ['metering', 'metering.test']
