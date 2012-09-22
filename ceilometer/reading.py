__author__ = 'Michal Fus'

from ceilometer.ganglia import rulesmanager

class Reading(object):
    "container for ganglia reading"

    def __init__(self, data):
        self.__clusterName = data.get('clusterName', 'undefined')
        self.__hostName = data.get('host', 'undefined')
        self.__value = data.get('value', 'undefined')
        self.__time = data.get('time', 'undefined')
        self.__units = data.get('units', 'undefined')
        self.__metricName = data.get('metricName', 'undefined')

        self.__is_instance = data.has_key('instance_name')

        if self.__is_instance:
            self.__instanceName = data['instance_name']
        else:
            self.__instanceName = 'undefined'

        self.__type = data.get('type', 'undefined')

        self.__alert = rulesmanager.Valid

    def getAlert(self):
        return self.__alert

    def setAlert(self, value):
        self.__alert = value

    def getClusterName(self):
        return self.__clusterName

    def getHostName(self):
        return self.__hostName

    def getValue(self):
        return self.__value

    def getTime(self):
        return self.__time

    def getUnits(self):
        return self.__units

    def getMetricName(self):
        return self.__metricName

    def getClusterName(self):
        return self.__clusterName

    def getHostName(self):
        return self.__hostName

    def getValue(self):
        return self.__value

    def getTime(self):
        return self.__time

    def getUnits(self):
        return self.__units

    def getMetricName(self):
        return self.__metricName

    def getInstanceName(self):
        return self.__instanceName

    def getType(self):
        return self.__type

    def getEventType(self):
        if self.__is_instance:
            return 'instance.' + self.MetricName
        else:
            return 'host.' + self.MetricName


    def setUnits(self, value):
        self.__units = value

    def setValue(self, value):
        self.__value = value

    def setMetricName(self, value):
        self.__metricName = value

    Alert = property(getAlert, setAlert, doc='Alert')

    ClusterName = property(getClusterName, doc='ClusterName')

    HostName = property(getHostName, doc='HostName')

    Value = property(getValue, setValue, doc='Value')

    Time = property(getTime, doc='Time')

    Units = property(getUnits, setUnits, doc='Units')

    MetricName = property(getMetricName, setMetricName, doc='MetricName')

    InstanceName = property(getInstanceName, doc='InstanceName')

    Type = property(getType, doc='Type')

    EventType = property(getEventType, doc='EventType')