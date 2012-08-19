from ceilometer.reading import Reading
from ceilometer.plugin import NotificationBase
from .. import counter

class RealTimeData(NotificationBase):

    def get_event_types(self):
        return ['host.cpu',
                'instance.cpu',
                ]


    def createCounterFromReading(self, reading):
        if isinstance(reading, Reading):
            return counter.Counter(
                source=reading.ClusterName,
                name=reading.MetricName,
                type=reading.EventType,
                volume=1,
                timestamp=reading.Time,
                resource_metadata={
                    'display_name': reading.EventType + ': ' + reading.ClusterName + '[' + reading.InstanceName + ']',
                    'instance_type': reading.InstanceName,
                    'host': reading.ClusterName,
                    'event_type': reading.EventType,
                    'value': reading.Value,
                    'units': reading.Units
                    },
                )
        else:
            raise Exception('Unexpected argument')

    def process_notification(self, message):
        return self.createCounterFromReading(message)
