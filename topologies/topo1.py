#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController

class SingleSwitchTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1', mac="11:00:00:00:00:01", protocols='OpenFlow13')
        s2 = self.addSwitch('s2', mac="11:00:00:00:00:02", protocols='OpenFlow13')
        s3 = self.addSwitch('s3', mac="11:00:00:00:00:03", protocols='OpenFlow13')
        s4 = self.addSwitch('s4', mac="11:00:00:00:00:04", protocols='OpenFlow13')
        s5 = self.addSwitch('s5', mac="11:00:00:00:00:05", protocols='OpenFlow13')
        s6 = self.addSwitch('s6', mac="11:00:00:00:00:06", protocols='OpenFlow13')
        s7 = self.addSwitch('s7', mac="11:00:00:00:00:07", protocols='OpenFlow13')
        s8 = self.addSwitch('s8', mac="11:00:00:00:00:08", protocols='OpenFlow13')
        s9 = self.addSwitch('s9', mac="11:00:00:00:00:09", protocols='OpenFlow13')
        s10 = self.addSwitch('s10', mac="11:00:00:00:00:10", protocols='OpenFlow13')

        h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip="10.0.0.1/12")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="10.0.0.2/12")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03", ip="10.0.0.3/12")


        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s10)

        self.addLink(s1, s2)
        self.addLink(s1, s3)
        self.addLink(s2, s3)

        self.addLink(s3, s4)

        self.addLink(s4, s5)
        self.addLink(s4, s6)
        self.addLink(s5, s6)

        self.addLink(s5, s7)
        self.addLink(s6, s8)
        self.addLink(s7, s8)

        self.addLink(s7, s9)
        self.addLink(s7, s10)

        self.addLink(s8, s9)
        self.addLink(s8, s10)

        self.addLink(s9, s10)



if __name__ == '__main__':
    setLogLevel('info')
    topo = SingleSwitchTopo()
    c1 = RemoteController('c1', ip='127.0.0.1')
    net = Mininet(topo=topo, controller=c1)
    net.start()
    #net.pingAll()
    CLI(net)
    net.stop()
