#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController

class MastersSwitchTopo(Topo):
    def build(self):
        s0 = self.addSwitch('s0', dpid='0', mac="11:00:00:00:00:10", protocols='OpenFlow13')
        s1 = self.addSwitch('s1', dpid='1', mac="11:00:00:00:00:11", protocols='OpenFlow13')
        s2 = self.addSwitch('s2', dpid='2', mac="11:00:00:00:00:12", protocols='OpenFlow13')
        s3 = self.addSwitch('s3', dpid='3', mac="11:00:00:00:00:13", protocols='OpenFlow13')
        s4 = self.addSwitch('s4', dpid='4', mac="11:00:00:00:00:14", protocols='OpenFlow13')
        s5 = self.addSwitch('s5', dpid='5', mac="11:00:00:00:00:15", protocols='OpenFlow13')

        h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip="10.0.0.1/12")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="10.0.0.2/12")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03", ip="10.0.0.3/12")
        h4 = self.addHost('h4', mac="00:00:00:00:00:04", ip="10.0.0.4/12")

        self.addLink(h1, s0)
        self.addLink(h2, s5)
        self.addLink(h3, s1)
        self.addLink(h4, s3)

        self.addLink(s0, s1)
        self.addLink(s0, s4)
        self.addLink(s1, s2)
        self.addLink(s1, s4)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
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
