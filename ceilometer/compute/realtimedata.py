from ceilometer.reading import Reading
from ceilometer.plugin import NotificationBase
from .. import counter

class RealTimeData(NotificationBase):

    def __init__(self):
        self._mem_total = {}
        self._cpu_system = {}
        self._pkts_out = {}

    def createCounterFromReading(self, reading):
        if isinstance(reading, Reading):
            return counter.Counter(
                source=reading.ClusterName,
                name=reading.MetricName,
                type=reading.EventType,
                volume=reading.Value,
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
        #return self.createCounterFromReading(message)
        return message


class CpuMeter(RealTimeData):

    def get_event_types(self):
        return ['host.cpu_user',
                'host.cpu_system',
                'host.mem_free',
                'host.mem_total',
                'host.pkts_out',
                'host.pkts_in',
                ]


    def process_notification(self, message):

        if message.EventType == 'host.mem_total':
            self._mem_total[message.HostName] = message.Value
        elif message.EventType == 'host.mem_free':
            if self._mem_total.has_key(message.HostName):
                message.MetricName = 'mem_util'
                message.Value = 1.0 - (message.Value / self._mem_total[message.HostName])
                message.Units = '%'


        elif message.EventType == 'host.cpu_system':
            self._cpu_system[message.HostName] = message.Value
        elif message.EventType == 'host.cpu_user':
            if self._cpu_system.has_key(message.HostName):
                message.MetricName = 'cpu_util'
                message.Value = message.Value + self._cpu_system[message.HostName]


        elif message.EventType == 'host.pkts_out':
            self._pkts_out[message.HostName] = message.Value
        elif message.EventType == 'host.pkts_in':
            if self._pkts_out.has_key(message.HostName):
                message.MetricName = 'pkts'
                message.Value = message.Value + self._pkts_out[message.HostName]

        return message

