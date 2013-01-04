from backend.out import Connector

class Tellstick(Connector):
    TYPE = 'Tellstick'

    def send(self, string):
        string = '{%s,"tellstick":"%s"}' % (string, self.connector.code)
        print string