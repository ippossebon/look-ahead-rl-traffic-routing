#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController

class MultipathExampleTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1', mac="11:00:00:00:00:11", protocols='OpenFlow13')
        s2 = self.addSwitch('s2', mac="11:00:00:00:00:12", protocols='OpenFlow13')
        s3 = self.addSwitch('s3', mac="11:00:00:00:00:13", protocols='OpenFlow13')
        s4 = self.addSwitch('s4', mac="11:00:00:00:00:14", protocols='OpenFlow13')
        s5 = self.addSwitch('s5', mac="11:00:00:00:00:15", protocols='OpenFlow13')

        h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip="10.0.0.1/12")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="10.0.0.2/12")

        self.addLink(h1, s1)
        self.addLink(h2, s4)

        self.addLink(s1, s2)
        self.addLink(s1, s3)
        self.addLink(s2, s4)
        self.addLink(s3, s5)
        self.addLink(s4, s5)


if __name__ == '__main__':
    setLogLevel('info')
    topo = MastersSwitchTopo()
    c1 = RemoteController('c1', ip='127.0.0.1')
    net = Mininet(topo=topo, controller=c1)
    net.start()
    #net.pingAll()
    CLI(net)
    net.stop()
