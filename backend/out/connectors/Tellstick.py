from backend.out.connectors.Connector import Connector

class Tellstick(Connector):
    TYPE = 'Tellstick'

    def send(self, string):
        string = '{'+string+',"tellstick":"'+self.connector.code+'"}'
        print string