..
      Copyright 2012 Nicolas Barcet for Canonical

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

.. _install:

================================================
 Installing and Running the Development Version
================================================

Ceilometer has two daemons. The :term:`agent` runs on the Nova compute
node(s) and the :term:`collector` runs on the cloud's management
node(s). In a development environment created by devstack_, these two
are typically the same server. They do not have to be, though, so some
of the instructions below are duplicated. Skip the steps you have
already done.

.. _devstack: http://www.devstack.org/

Installing the Collector
========================

.. index::
   double: installing; collector

1. Install and configure nova.

   The collector daemon imports code from ``nova``, so it needs to be
   run on a server where nova has already been installed.

   .. note::

      Ceilometer makes extensive use of the messaging bus, but has not
      yet been tested with ZeroMQ. We recommend using Rabbit or qpid
      for now.

2. Install MongoDB.

   Follow the instructions to install the MongoDB_ package for your
   operating system, then start the service.

3. Clone the ceilometer git repository to the management server::

   $ cd /opt/stack
   $ git clone https://github.com/stackforge/ceilometer.git

4. As a user with ``root`` permissions or ``sudo`` privileges, run the
   ceilometer installer::

   $ cd ceilometer
   $ sudo python setup.py install

5. Configure ceilometer.

   Ceilometer needs to know about some of the nova configuration
   options, so the simplest way to start is copying
   ``/etc/nova/nova.conf`` to ``/etc/ceilometer-collector.conf``. Some
   of the logging settings used in nova break ceilometer, so they need
   to be removed. For example, as a user with ``root`` permissions::

     $ grep -v format_string /etc/nova/nova.conf > /etc/ceilometer-collector.conf

   Refer to :doc:`configuration` for details about any other options
   you might want to modify before starting the service.

6. Start the collector.

   ::

     $ ./bin/ceilometer-collector

   .. note:: 

      The default development configuration of the collector logs to
      stderr, so you may want to run this step using a screen session
      or other tool for maintaining a long-running program in the
      background.

.. _MongoDB: http://www.mongodb.org/


Installing the Compute Agent
============================

.. index::
   double: installing; compute agent

.. note:: The compute agent must be installed on each nova compute node.

1. Install and configure nova.

   The collector daemon imports code from ``nova``, so it needs to be
   run on a server where nova has already been installed.

   .. note::

      Ceilometer makes extensive use of the messaging bus, but has not
      yet been tested with ZeroMQ. We recommend using Rabbit or qpid
      for now.

2. Clone the ceilometer git repository to the server::

   $ cd /opt/stack
   $ git clone https://github.com/stackforge/ceilometer.git

4. As a user with ``root`` permissions or ``sudo`` privileges, run the
   ceilometer installer::

   $ cd ceilometer
   $ sudo python setup.py install

5. Configure ceilometer.

   Ceilometer needs to know about some of the nova configuration
   options, so the simplest way to start is copying
   ``/etc/nova/nova.conf`` to ``/etc/ceilometer-agent.conf``. Some
   of the logging settings used in nova break ceilometer, so they need
   to be removed. For example, as a user with ``root`` permissions::

     $ grep -v format_string /etc/nova/nova.conf > /etc/ceilometer-agent.conf

   Refer to :doc:`configuration` for details about any other options
   you might want to modify before starting the service.

6. Start the agent.

   ::

     $ ./bin/ceilometer-agent

   .. note:: 

      The default development configuration of the agent logs to
      stderr, so you may want to run this step using a screen session
      or other tool for maintaining a long-running program in the
      background.
