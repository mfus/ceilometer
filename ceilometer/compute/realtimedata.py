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
                user_id=None,
                project_id=None,
                resource_id=None,
                duration=None,
                resource_metadata={
                    'display_name': reading.EventType + ': ' + reading.ClusterName + '[' + reading.InstanceName + ']',
                    'instance_type': reading.InstanceName,
                    'host': reading.HostName,
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

        send = False

        if message.EventType == 'host.mem_total':
            #print "%s %s"  % (message.HostName, message.Value)
            self._mem_total[message.HostName] = float(message.Value)
        elif message.EventType == 'host.mem_free':
            #if self._mem_total.has_key(message.HostName):

            #print "free %s %s"  % (message.HostName, float(message.Value) / 8110416 )

            message.MetricName = 'mem_util'
            message.Value = (1.0 - (float(message.Value) / 8110416)) * 100.0
            message.Units = '%'
            send = True
            print "total %s %s"  % (message.HostName, message.Value)


        elif message.EventType == 'host.cpu_system':
            self._cpu_system[message.HostName] = float(message.Value)
        elif message.EventType == 'host.cpu_user':
            if self._cpu_system.has_key(message.HostName):
                message.MetricName = 'cpu_util'
                message.Value = float(message.Value) + self._cpu_system[message.HostName]
                send = True
                print "cpu total %s %s"  % (message.HostName, message.Value)


        elif message.EventType == 'host.pkts_out':
            self._pkts_out[message.HostName] = float(message.Value)
        elif message.EventType == 'host.pkts_in':
            if self._pkts_out.has_key(message.HostName):
                message.MetricName = 'pkts'
                message.Value = float(message.Value) + self._pkts_out[message.HostName]
                send = True

        if send:
            try:
                counter = [self.createCounterFromReading(message),]
                return counter
            except Exception as err:
                print "%s" % err
        else:
            pass



