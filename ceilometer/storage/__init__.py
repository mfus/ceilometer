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
"""Storage backend management
"""

import pkg_resources

from ceilometer.openstack.common import log
from ceilometer.openstack.common import cfg

LOG = log.getLogger(__name__)

STORAGE_ENGINE_NAMESPACE = 'ceilometer.storage'

STORAGE_OPTS = [
    cfg.StrOpt('metering_storage_engine',
               default='mongodb',
               help='The name of the storage engine to use',
               ),
    ]


cfg.CONF.register_opts(STORAGE_OPTS)


def register_opts(conf):
    """Register any options for the storage system.
    """
    p = get_engine(conf)
    p.register_opts(conf)


def get_engine(conf):
    """Load the configured engine and return an instance.
    """
    engine_name = conf.metering_storage_engine
    LOG.debug('looking for %r driver in %r',
              engine_name, STORAGE_ENGINE_NAMESPACE)
    for ep in pkg_resources.iter_entry_points(STORAGE_ENGINE_NAMESPACE,
                                              engine_name):
        try:
            engine_class = ep.load()
            engine = engine_class()
        except Exception as err:
            LOG.error('Failed to load storage engine %s: %s',
                      engine_name, err)
            LOG.exception(err)
            raise
        LOG.info('Loaded %s storage engine %r', engine_name, ep)
        return engine
    else:
        raise RuntimeError('No %r storage engine found' % engine_name)


def get_connection(conf):
    """Return an open connection to the database.
    """
    engine = get_engine(conf)
    engine.register_opts(conf)
    db = engine.get_connection(conf)
    return db


class EventFilter(object):
    """Holds the properties for building a query to filter events.

    :param user: The event owner.
    :param project: The event owner.
    :param start: Earliest timestamp to include.
    :param end: Only include events with timestamp less than this.
    :param resource: Optional filter for resource id.
    :param meter: Optional filter for meter type using the meter name.
    :param source: Optional source filter.
    """
    def __init__(self, user=None, project=None, start=None, end=None,
                 resource=None, meter=None, source=None):
        self.user = user
        self.project = project
        self.start = start
        self.end = end
        self.resource = resource
        self.meter = meter
        self.source = source
        if not (self.user or self.project):
            raise RuntimeError('Must provide one of "user" or "project".')
