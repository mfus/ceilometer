from ceilometer.openstack.common import log

Valid, UpperBound, LowerBound = range(3)
LOG = log.getLogger(__name__)


class RulesManager(object):

    def validateAgainstRules(self, message):

        print "RulesManager %s" % message.resource_metadata
        value = message.resource_metadata['value']
        print value


        if value > 70:
            message.resource_metadata['alert'] = UpperBound
        elif value < 40:
            message.resource_metadata['alert'] = LowerBound
        else:
            message.resource_metadata['alert'] = Valid

        return message.resource_metadata['alert']

