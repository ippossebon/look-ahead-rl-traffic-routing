#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController

class MastersSwitchTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1', dpid='1', mac="11:00:00:00:00:11", protocols='OpenFlow13')
        s2 = self.addSwitch('s2', dpid='2', mac="11:00:00:00:00:12", protocols='OpenFlow13')
        s3 = self.addSwitch('s3', dpid='3', mac="11:00:00:00:00:13", protocols='OpenFlow13')
        s4 = self.addSwitch('s4', dpid='4', mac="11:00:00:00:00:14", protocols='OpenFlow13')
        s5 = self.addSwitch('s5', dpid='5', mac="11:00:00:00:00:15", protocols='OpenFlow13')
        s6 = self.addSwitch('s6', dpid='6', mac="11:00:00:00:00:16", protocols='OpenFlow13')

        h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip="10.0.0.1/12")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="10.0.0.2/12")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03", ip="10.0.0.3/12")
        h4 = self.addHost('h4', mac="00:00:00:00:00:04", ip="10.0.0.4/12")

        # Adiciona hosts aos switches
        self.addLink(
            node1 = h1,
 	        node2 = s1,
 	        port1 = 1,
 	        port2 = 1
        )
        self.addLink(
            node1 = h2,
 	        node2 = s6,
 	        port1 = 1,
 	        port2 = 1
        )
        self.addLink(
            node1 = h3,
 	        node2 = s2,
 	        port1 = 1,
 	        port2 = 1
        )
        self.addLink(
            node1 = h4,
            node2 = s4,
            port1 = 1,
            port2 = 1
        )

        # Adiciona links entre os switches
        self.addLink(
            node1 = s1,
            node2 = s2,
            port1 = 2,
            port2 = 2
        )
        self.addLink(
            node1 = s1,
            node2 = s5,
            port1 = 3,
            port2 = 2
        )
        self.addLink(
            node1 = s2,
            node2 = s3,
            port1 = 3,
            port2 = 2
        )
        self.addLink(
            node1 = s2,
            node2 = s5,
            port1 = 4,
            port2 = 3
        )
        self.addLink(
            node1 = s3,
            node2 = s4,
            port1 = 3,
            port2 = 2
        )
        self.addLink(
            node1 = s4,
            node2 = s5,
            port1 = 3,
            port2 = 4
        )
        self.addLink(
            node1 = s4,
            node2 = s6,
            port1 = 4,
            port2 = 2
        )
        self.addLink(
            node1 = s5,
            node2 = s6,
            port1 = 5,
            port2 = 3
        )


if __name__ == '__main__':
    setLogLevel('info')
    topo = MastersSwitchTopo()
    # c1 = RemoteController('c1', ip='127.0.0.1') #usando RYU
    c1 = RemoteController('c1', ip='0.0.0.0', port='6653') #usando Floodlight

    net = Mininet(topo=topo, controller=c1)
    net.start()
    #net.pingAll()
    CLI(net)
    net.stop()
