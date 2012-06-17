from ceilometer import log

from ceilometer.components.monitors import MeteringDataMonitorBase
from ceilometer.components.queuepublisher import QueuePublisher

LOG = log.getLogger(__name__)

class HealthMonitor(MeteringDataMonitorBase):
    """Object processing metering data and validating them against defined rules

        Object connects publisher (ex. Queue - RabbitMq), pollsters (CPU, Disk, Network).
    """
    HEALTH_MONITOR_TOPIC = "health.topic"

    def __init__(self, context):
        """Initialize HealthMonitor

            :param context: pollsters and queuePublisher context
        """
        super(HealthMonitor, self).__init__(context)
        self.publisher = QueuePublisher(self.context, {QueuePublisher.QUEUE_TOPIC_ARG: self.HEALTH_MONITOR_TOPIC})

        def alert_message_from_data(data):
            #TODO: Implement
            pass

        self.publisher.message_from_data = alert_message_from_data
        pass

    def _periodic_refresh(self):
        """Foreach pollsters and fetch counters"""
        # TODO: Should I define different intervals for each pollster?
        for name, pollster in self.pollsters:
            self._process_metering_data(name, pollster.get_counter())

    def _process_metering_data(self, name, counter):
        """Check counters and rules. Send alert if it's needed.

            :param name: pollster's name
            :param counter: object with data collected by pollster
        """

        alert = self._check_constrains(name, counter)
        if alert:
            self._send_alert(alert)

            # Pass data to local database? Count Average, Min/Max etc...

    def _check_constrains(self, name, counter):
        """Check constrains and generate proper alert"""
        #TODO: Implement
        pass

    def _init_alerts(self):
        """Setup constrains"""
        #TODO: Implement
        pass

    def _send_alert(self, alert):
        """Send/Publish alert message"""
        self.publisher.publish_data(alert)