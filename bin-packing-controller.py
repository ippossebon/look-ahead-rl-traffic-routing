from ryu.base import app_manager
from ryu.controller import mac_to_port
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import arp
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import ipv6
from ryu.lib.packet import ether_types
from ryu.lib import mac, ip, hub
from ryu.topology.api import get_switch, get_link
from ryu.app.wsgi import ControllerBase
from ryu.topology import event

from collections import defaultdict
from operator import itemgetter

from utils import ControllerUtilities

from routing.graphModel.graph2 import Graph
from routing.graphModel.link import Link
from routing.graphModel.node import Node
from routing.graphModel.flow import Flow

import os
import random
import time

# Cisco Reference bandwidth = 1 Gbps
REFERENCE_BW = 10000000

DEFAULT_BW = 10000000


class HybridController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(HybridController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.topology_api_app = self
        self.datapath_list = {}         # dicionário cuja chave é o ID do switch e o valor é datapath correspondente
        self.arp_table = {}             # arp table do tipo arp_table[IP] = MAC
        self.switches = []              # lista com IDs de todos os switches da rede
        self.hosts = {}                 # hosts{MAC} = (switch_id, porta que conecta ao swith)
        self.multipath_group_ids = {}
        self.group_ids = []
        self.adjacency = defaultdict(dict)
        self.bandwidths = defaultdict(lambda: defaultdict(lambda: DEFAULT_BW))

        self.controller_utilities_initialized = False

        ## Bin packing variables
        self.networkGraph = Graph()
        self.switches_count = 0
        self.nodes = []
        self.links = []

        self.datapaths = {}
    #     self.monitorThread = hub.spawn(self._monitor)
    #
    #
    # def _monitor(self):
    #     while True:
    #         for dp in self.datapaths.values():
    #             self._request_stats(dp)
    #         hub.sleep(10)


    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, ev):
        switch = ev.switch.dp
        ofp_parser = switch.ofproto_parser
        self.switches_count = self.switches_count + 1

        if not self.networkGraph.containsNodeId(switch.id):
            self.networkGraph.addNode(switch.id)
            self.networkGraph.printGraph()
            # self.networkGraph.printCostMatrix()

        if switch.id not in self.switches:
            self.switches.append(switch.id)
            self.datapath_list[switch.id] = switch

            # Pede informações de porta/link para o switch
            req = ofp_parser.OFPPortDescStatsRequest(switch)
            switch.send_msg(req)

        print('Switches do graphModel: {0}'.format(self.networkGraph.nodes))


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        # Recebe informações do switch
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)


    @set_ev_cls(event.EventSwitchLeave, MAIN_DISPATCHER)
    def switch_leave_handler(self, ev):
        # Remove switch
        switch = ev.switch.dp.id
        if switch in self.switches:
            self.switches.remove(switch)
            del self.datapath_list[switch]
            del self.adjacency[switch]

        if self.networkGraph.containsNodeId(switch):
            self.networkGraph.removeNode(switch)
            self.switches_count = self.switches_count - 1


    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def port_desc_stats_reply_handler(self, ev):
        # Recebe informações da porta
        switch = ev.msg.datapath
        for p in ev.msg.body:
            self.bandwidths[switch.id][p.port_no] = p.curr_speed


    @set_ev_cls(event.EventLinkAdd, MAIN_DISPATCHER)
    def link_add_handler(self, ev):
        s1 = ev.link.src
        s2 = ev.link.dst
        self.adjacency[s1.dpid][s2.dpid] = s1.port_no
        self.adjacency[s2.dpid][s1.dpid] = s2.port_no

        if not self.networkGraph.containsLink(s1.dpid,s2.dpid):
            # link_weight = self.bandwidths[s1.dpid][s2.dpid]
            self.networkGraph.addLink(
                node_id_1=s1.dpid,
                node_id_2=s2.dpid,
                weight=500) # # TODO: colocar largura de banda correta


    @set_ev_cls(event.EventLinkDelete, MAIN_DISPATCHER)
    def link_delete_handler(self, ev):
        s1 = ev.link.src
        s2 = ev.link.dst
        # Exception handling if switch already deleted
        try:
            del self.adjacency[s1.dpid][s2.dpid]
            del self.adjacency[s2.dpid][s1.dpid]

            if self.networkGraph.containsLink(s1.dpid,s2.dpid):
                self.networkGraph.removeLink(s1.dpid,s2.dpid)
        except KeyError:
            pass


    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        print("Adiciona flow: {0} com actions = {1}".format(match, actions))

        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):

        if not self.controller_utilities_initialized:
            self.controller_utilities = ControllerUtilities(self.adjacency, self.datapath_list, self.bandwidths)
            self.controller_utilities_initialized = True

        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        arp_pkt = pkt.get_protocol(arp.arp)

        # avoid broadcast from LLDP
        if eth.ethertype == 35020:
            return

        if pkt.get_protocol(ipv6.ipv6):  # Drop the IPV6 Packets.
            match = parser.OFPMatch(eth_type=eth.ethertype)
            actions = []
            self.add_flow(datapath, 1, match, actions)
            return None

        dst = eth.dst
        src = eth.src
        dpid = datapath.id

        if src not in self.hosts:
            # Mapeia o host de origem para switch ao qual está ligado e porta associada
            self.hosts[src] = (dpid, in_port)

        out_port = ofproto.OFPP_FLOOD

        if arp_pkt:
            src_ip = arp_pkt.src_ip
            dst_ip = arp_pkt.dst_ip

            if arp_pkt.opcode == arp.ARP_REPLY:
                self.arp_table[src_ip] = src

                # Hosts é um dicionário do tipo hosts[MAC_ADDRESS] = (switch_id, porta que conecta ao switch)
                h1 = self.hosts[src]
                h2 = self.hosts[dst]

                source_switch_id = h1[0]
                source_switch_port = h1[1]
                dest_switch_id = h2[0]
                dest_switch_port = h2[1]

                # Retorna a porta para qual deve ser enviado o flow
                out_port = self.installPaths(
                    source_switch_id,
                    source_switch_port,
                    dest_switch_id,
                    dest_switch_port,
                    src_ip,
                    dst_ip
                )

                # Instala caminho reverso
                self.installPaths(
                    dest_switch_id,
                    dest_switch_port,
                    source_switch_id,
                    source_switch_port,
                    dst_ip,
                    src_ip
                )

            elif arp_pkt.opcode == arp.ARP_REQUEST:
                if dst_ip in self.arp_table:
                    self.arp_table[src_ip] = src
                    dst_mac = self.arp_table[dst_ip]

                    h1 = self.hosts[src]
                    h2 = self.hosts[dst_mac]

                    source_switch_id = h1[0]
                    source_switch_port = h1[1]
                    dest_switch_id = h2[0]
                    dest_switch_port = h2[1]

                    # Retorna a porta para qual deve ser enviado o flow
                    out_port = self.installPaths(
                        source_switch_id,
                        source_switch_port,
                        dest_switch_id,
                        dest_switch_port,
                        src_ip,
                        dst_ip
                    )

                    # Instala caminho reverso
                    self.installPaths(
                        dest_switch_id,
                        dest_switch_port,
                        source_switch_id,
                        source_switch_port,
                        dst_ip,
                        src_ip
                    )

        # Trata pacotes que nao sao  ARP
        actions = [parser.OFPActionOutput(out_port)]

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,
            actions=actions, data=data)

        #print('datapath={0}, buffer_id={1}, in_port={2}, actions={3}, data={4}'.format(datapath, msg.buffer_id, in_port, actions, data))

        datapath.send_msg(out)


    # Instala todos os caminhos possíveis, de uma só vez.
    def installPaths(self, src, first_port, dst, last_port, ip_src, ip_dst):
        '''
        src = switch de origem
        first_port = porta que conecta o switch de origem ao host de origem
        dst = switch de destino
        last_port = porta que conecta o switch de destino ao host de destino
        ip_src = IP do host de origem
        ip_dst = IP do host de destino
        '''
        computation_start = time.time()
        neededBandwidth = 1000 # TODO: futuramente, aqui terá a predição da largura de banda necessária
        flow = Flow(src, dst, 200)
        path = self.networkGraph.getMinimumCostPath(flow)

        print('[installPaths] chosen path = {0}'.format(path))

        # --- Gambiarra ---
        list_path = []
        list_path.append(path)
        # -------

        path_with_ports = self.controller_utilities.addPortsToPath(list_path, first_port, last_port)
        print('path_with_ports = {0}'.format(path_with_ports))
        # path_with_ports = {1: (1, 3), 3: (1, 3), 4: (1, 3), 5: (2, 3), 6: (1, 2), 7: (1, 4), 10: (2, 1)}

        # Lista de todos os switches que fazem parte do caminho ótimo
        switches_in_path = set().union(*list_path)

        print('[installPaths] switches_in_path = {0}'.format(switches_in_path))

        for node in switches_in_path:
            # Para cada switch que faz parte do caminho:
            dp = self.datapath_list[node]
            ofp = dp.ofproto
            ofp_parser = dp.ofproto_parser

            match_ip = ofp_parser.OFPMatch(
                eth_type=0x0800,
                ipv4_src=ip_src,
                ipv4_dst=ip_dst
            )
            match_arp = ofp_parser.OFPMatch(
                eth_type=0x0806,
                arp_spa=ip_src,
                arp_tpa=ip_dst
            )

            # path_with_ports = {1: (1, 3), 3: (1, 3), 4: (1, 3), 5: (2, 3), 6: (1, 2), 7: (1, 4), 10: (2, 1)}
            print('[installPaths] path_with_ports = {0}'.format(path_with_ports))
            print('[installPaths] path_with_ports[node] = {0}'.format(path_with_ports[node]))

            in_port = path_with_ports[node][0]
            out_port = path_with_ports[node][1]
            actions = [ofp_parser.OFPActionOutput(out_port)]


            print('[installPaths] dp = {0}'.format(dp))
            self.add_flow(datapath, in_port, dst, actions)
            self.addFlow(dp, 32768, match_ip, actions)
            self.addFlow(dp, 1, match_arp, actions)


    def addFlow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        print('[addFlow]: datapath = {0} ; priority = {1} ; match = {2} ; actions = {3} ; buffer_id = {4}'.format(
            datapath, priority, match, actions, buffer_id))

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst,
                                    hard_timeout=10)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, hard_timeout=10)
        datapath.send_msg(mod)
