import abc

class MeteringDataProcessorBase(object):
    """Base class for metering data processors.

        Connects pollsters, publisher and mechanism how and when pull and publish metering data.

        Example use case:
            - fetch metering data from pollsters
            - send proper message through default publisher (queue ex. RabbitMQ)
    """
    __metaclass__ = abc.ABCMeta

    pollsters = []
    publishers = []


class SimpleBillingProcessor(MeteringDataProcessorBase):
    """Simple billing processor. Pulls metering data from pollsters and sends them through publisher (ex. RabbitMq)
    """

    def __init__(self):
        pass

    def _periodical_task(self):
        pass


class HealthMonitorProcessor(MeteringDataProcessorBase):
    """Object processing metering data and validating them against defined rules

        Object connects publisher (ex. Queue - RabbitMq), pollsters (CPU, Disk, Network).
    """
    def __init__(self):
        # TODO: Initialize periodical_refresh
        pass

    def _periodical_refresh(self):
        """Periodical task.

            Query known pollsters and analyse data.
        """
        # TODO: Should I define different intervals for each pollster?
        for name, pollster in self.pollsters:
            self._process_metering_data(name, pollster.get_counter())

    def _process_metering_data(self, name, counter):

        alert = self._check_constrains(name, counter)
        if alert:
            self._send_alert(alert)

        # Pass data to local database? Count Average, Min/Max etc...


    def _check_constrains(self, name, counter):
        """Check constrains and generate(return) proper alert"""
        pass

    def _init_alerts(self):
        """Setup constrains"""
        pass

    def _send_alert(self, alert):
        """Notify all publishers about alert"""
        for name, publisher in self.publishers:
            publisher.publish_data(alert.counting, alert.message)
