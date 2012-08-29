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
"""Tests for ceilometer/agent/manager.py
"""

import datetime

from ceilometer.compute import manager
from ceilometer import counter
from ceilometer import publish
from ceilometer.tests import base


def test_load_plugins():
    mgr = manager.AgentManager()
    mgr.init_host()
    assert mgr.pollsters, 'Failed to load any plugins'
    return


class TestRunTasks(base.TestCase):

    class Pollster:
        counters = []
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
            resource_metadata={'name': 'Pollster',
                               },
            )

        def get_counters(self, manager, instance):
            self.counters.append((manager, instance))
            return [self.test_data]

    def faux_notify(self, context, msg):
        self.notifications.append(msg)

    def setUp(self):
        super(TestRunTasks, self).setUp()
        self.notifications = []
        self.stubs.Set(publish, 'publish_counter', self.faux_notify)
        self.mgr = manager.AgentManager()
        self.mgr.pollsters = [('test', self.Pollster())]
        # Set up a fake instance value to be returned by
        # instance_get_all_by_host() so when the manager gets the list
        # of instances to poll we can control the results.
        self.instance = 'faux instance'
        self.mox.StubOutWithMock(self.mgr.db, 'instance_get_all_by_host')
        self.mgr.db.instance_get_all_by_host(
            None,
            self.mgr.host,
            ).AndReturn([self.instance])

        self.mox.ReplayAll()
        # Invoke the periodic tasks to call the pollsters.
        self.mgr.periodic_tasks(None)

    def test_message(self):
        assert self.Pollster.counters[0][1] is self.instance

    def test_notifications(self):
        assert self.notifications[0] is self.Pollster.test_data
        assert len(self.notifications) == 1
