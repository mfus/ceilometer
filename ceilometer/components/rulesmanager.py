__author__ = 'michal'

Valid, Warning, Error, Fatal = range(4)

class RulesManager(object):

    def validateAgainstRules(self, counter):

        alert = Error
        counter['alert'] = alert
        return alert
