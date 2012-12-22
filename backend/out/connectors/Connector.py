from backend.models.Connector import Connector as ConnectorModel

class Connector(object):
    TYPE = ''

    def initialize(self, connector):
        assert isinstance(connector, ConnectorModel)
        self.connector = connector

    def send(self, string):
        raise NotImplementedError