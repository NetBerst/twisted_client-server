
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory
from twisted.protocols.basic import LineReceiver


class Sr_Protocol(LineReceiver):

    def dataReceived(self, data):
        self.sendMessageToConnections(self.factory.factoryObject, data)

    def connectionMade(self): 
        self.factory.connections.append(self)
        print "Port <10000> LeftMost connected"
        self.transport.write('Port <10000> LeftMost connected')

    def sendMessageToConnections(self, factoryObject, data):
        for connection in factoryObject.factory.connections:  
            connection.transport.write("<10000> %s" % data)


class Sr_Factory(ServerFactory):
    protocol = Sr_Protocol

    def __init__(self):
        self.connections = []



class Cl_Protocol(Protocol):
    
    def dataReceived(self, data):
        self.sendMessageToConnections(self.factory.factoryObject, data)
        
    def sendMessageToConnections(self, factoryObject, data):
        for connection in factoryObject.factory.connections:  
            connection.transport.write(data)

    def connectionMade(self):
        self.factory.connections.append(self)

    def connectionLost(self, reason):
        self.factory.connections.remove(self)


class Cl_Factory(ClientFactory): 
    protocol = Cl_Protocol

    def __init__(self):
        self.connections = []


host = 'localhost'

Cl = Cl_Factory()
Sr = Sr_Factory()
clFactoryObject = reactor.connectTCP(host, 10001, Cl)
srFactoryObject = reactor.listenTCP(10000, Sr)

Sr.factoryObject = clFactoryObject
Cl.factoryObject = srFactoryObject

reactor.run()
