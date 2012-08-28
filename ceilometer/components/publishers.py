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

import abc

class PublisherBase(object):
    """Base class for plugins that support publishing data to external resource ex. Queue."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def publish_data(self, counting, message):
        """Takes and processes metering data. It could publish it to external stream, write to file,
        pass it to local daemon."""

    @abc.abstractmethod
    def init_publisher(self, **kwargs):
        """Takes arguments needed to initialize publisher class"""

#class HealthMonitorBase(object):
#    """Base class for plugins that support consuming metering data and sending proper alert messages via own mechanisms"""
#
#    __metaclass__ = abc.ABCMeta
#
#    @abc.abstractmethod
#    def process_monitoring_data(self, data):
#        """Consumes monitoring (metering) data and do proper actions."""