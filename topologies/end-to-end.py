#!/usr/bin/python


"""Custom topology example

!!! Contains loops !!!

MAC,IP, Controller, CLI stuff configured
# run RYU SDN STP Application for this topology
ryu-manager ryu.app.simple_switch_stp
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController

class SingleSwitchTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')
        s9 = self.addSwitch('s9')


        h1 = self.addHost('h1', mac="00:00:00:00:11:11", ip="192.168.1.1/24")
        h2 = self.addHost('h2', mac="00:00:00:00:11:12", ip="192.168.1.2/24")

        self.addLink(h1, s1)

        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s4, s9)

        self.addLink(s1, s5)
        self.addLink(s5, s6)
        self.addLink(s6, s9)

        self.addLink(s1, s7)
        self.addLink(s7, s8)
        self.addLink(s8, s9)

        self.addLink(h2, s9)


if __name__ == '__main__':
    setLogLevel('info')
    topo = SingleSwitchTopo()
    c1 = RemoteController('c1', ip='127.0.0.1')
    net = Mininet(topo=topo, controller=c1)
    net.start()
    #net.pingAll()
    CLI(net)
    net.stop()
