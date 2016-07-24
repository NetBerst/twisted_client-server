
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory
from twisted.protocols.basic import LineReceiver


class Sr_Protocol(LineReceiver):

    def dataReceived(self, data):
        self.sendMessageToConnections(self.factory.factoryObject, data)

    def connectionMade(self): #10001
        print "Port <10001> Client connected"
        self.factory.connections.append(self)

    def sendMessageToConnections(self, factoryObject, data):
        for connection in factoryObject.factory.connections:  
            connection.transport.write(data)


class Sr_Factory(ServerFactory):
    protocol = Sr_Protocol
    
    def __init__(self):
        self.connections = []
    


class Cl_Protocol(LineReceiver):
    
    def dataReceived(self, data):
        self.sendMessageToConnections(self.factory.factoryObject, data)
        
    def sendMessageToConnections(self, factoryObject, data):
        for connection in factoryObject.factory.connections:  
            connection.transport.write("<10002> %s " % data)

    def connectionMade(self): #10002
        print "Port <10002> Rightmost connected"
        self.transport.write("Port <10002> Rightmost connected")
        self.factory.connections.append(self)

    def connectionLost(self, reason):
        self.factory.connections.remove(self)


class Cl_Factory(ServerFactory): 
    protocol = Cl_Protocol

    def __init__(self):
        self.connections = []


host = 'localhost'
cl = Cl_Factory()
sr = Sr_Factory()

clFactoryObject = reactor.listenTCP(10002, cl ,interface = host)

sr.factoryObject = clFactoryObject

SrFactoryObject = reactor.listenTCP(10001, sr, interface = host)

cl.factoryObject = SrFactoryObject

reactor.run()















