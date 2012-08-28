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
        pass

    def _periodical_refresh(self):
        pass

    def _init_alerts(self):
        pass

    def _send_alert(self):
        pass
