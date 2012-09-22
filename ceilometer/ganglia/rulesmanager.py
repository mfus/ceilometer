Valid, Warning, Error, Fatal = range(4)

class RulesManager(object):

    def validateAgainstRules(self, reading):

        if reading.Value > 70 or reading.Value < 40:
            reading.Alert = Error
        else:
            reading.Alert = Valid

        return reading.Alert

