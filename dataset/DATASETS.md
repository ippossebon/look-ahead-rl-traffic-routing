**Unicauca**

87 features and 3.577.296 instances

Source: https://www.kaggle.com/jsrojas/ip-network-traffic-flows-labeled-with-87-apps

Features:
Flow.ID = a flow identifier following the next format: SourceIP-DestinationIP-SourcePort-DestinationPort-TransportProtocol
Source.IP = The source IP address of the flow.
Source.Port = The source port number
Destination.IP = The destination IP address.
Destination.Port = The destination port number.
Protocol = The transport layer protocol number identification (i.e.,TCP = 6, UDP = 17).
Timestamp = The instant the packet was captured stored in the next date format: Dd/mm/yyyy HH:MM:SS
Flow.Duration = The total duration of the flow
Total.Fwd.Packets = The total number of packets in the forward direction.
Total.Backward.Packets = The total number of packets in the backward direction.
Total.Length.of.Fwd.Packets = The total quantity of bytes in the forward direction obtained from all the flow (all the packets transmitted). This is obtained from the Total Length field stored on the packets header.
Total.Length.of.Bwd.Packets = The total quantity of bytes in the backward direction obtained from all the flow (all the packets transmitted). This is obtained from the Total Length field stored on the packets header.
Fwd.Packet.Length.Max = The maximum value in bytes of the packets length in the forward direction.
Fwd.Packet.Length.Min = The minimum value in bytes of the packets length in the forward direction.
Fwd.Packet.Length.Mean = The mean value in bytes of the packets length in the forward direction.
Fwd.Packet.Length.Std = The standard deviation in bytes of the packets length in the forward direction.
Bwd.Packet.Length.Max = The maximum value in bytes of the packets length in the backward direction.
Bwd.Packet.Length.Min = The minimum value in bytes of the packets length in the backward direction.
Bwd.Packet.Length.Mean = The mean value in bytes of the packets length in the backward direction.
Bwd.Packet.Length.Std = The standard deviation in bytes of the packets length in the backward direction.
Flow.Bytes.s = The number of bytes per second in the flow.
Flow.Packets.s = The number of packets per second in the flow.
Flow.IAT.Mean = The mean value of the inter-arrival time of the flow (in both directions).
Flow.IAT.Std = The standard deviation of the inter-arrival time of the flow (in both directions).
Flow.IAT.Max = The maximum value of the inter-arrival time of the flow (in both directions).
Flow.IAT.Min = The minimum value of the inter-arrival time of the flow (in both directions).
Fwd.IAT.Total = The total Inter-arrival time in the forward direction.
Fwd.IAT.Mean = The mean inter-arrival time in the forward direction.
Fwd.IAT.Std = The standard inter-arrival time in the forward direction
Fwd.IAT.Max = The maximum value of the inter-arrival time in the forward direction
Fwd.IAT.Min = The minimum value of the inter-arrival time in the forward direction
Bwd.IAT.Total = The total Inter-arrival time in the backward direction.
Bwd.IAT.Mean = The mean inter-arrival time in the backward direction.
Bwd.IAT.Std = The standard inter-arrival time in the backward direction.
Bwd.IAT.Max = The maximum value of the inter-arrival time in the backward direction.
Bwd.IAT.Min = The minimum value of the inter-arrival time in the backward direction
Fwd.PSH.Flags = The number of times the packets sent in the flow had the pushing flag bit set as 1 in the forward direction. The Pushing flag allows to send information immediately without filling all the buffer size from a packet, notifying the receptor to pass the packet to the application at once, it is very useful for real time applications.
Bwd.PSH.Flags = The number of times the packets sent in the flow had the PSH (pushing) flag bit set as 1 in the backward direction.
Fwd.URG.Flags = The number of times the packets sent in the flow had the URG (Urgent) flag bit set as 1 in the forward direction. The URG flag is used to inform a receiving station that certain data within a segment is urgent and should be prioritized. If the URG flag is set, the receiving station evaluates the urgent pointer, a 16-bit field in the TCP header. This pointer indicates how much of the data in the segment, counting from the first byte, is urgent.
Bwd.URG.Flags = The number of times the packets sent in the flow had the URG (Urgent) flag bit set as 1 in the backward direction.
Fwd.Header.Length = The header length of the packets flow in the forward direction.
Bwd.Header.Length = The header length of the packets flow in the backward direction.
Fwd.Packets.s = The number of packets per second in the forward direction.
Bwd.Packets.s = The number of packets per second in the backward direction.
Min.Packet.Length = The minimum length of the packets registered in the flow (both forward and backward directions).
Max.Packet.Length = The maximum length of the packets registered in the flow (both forward and backward directions).
Packet.Length.Mean = The mean value of the length of the packets registered in the flow (both forward and backward directions).
Packet.Length.Std = The standard deviation of the length of the packets registered in the flow (both forward and backward directions).
Packet.Length.Variance = The variance of the length of the packets registered in the flow (both forward and backward directions).
FIN.Flag.CountThe number of times the packets sent in the flow had the FIN flag bit set as 1. In the normal case, each side terminates its end of the connection by sending a special message with the FIN (finish) bit set. This message, sometimes called a FIN, serves as a connection termination request to the other device, while also possibly carrying data like a regular segment. The device receiving the FIN responds with an acknowledgment to the FIN to indicate that it was received. The connection as a whole is not considered terminated until both sides have finished the shutdown procedure by sending a FIN and receiving an ACK.
SYN.Flag.Count = The number of times the packets sent in the flow (in both directions) had the SYN (Synchronize) flag bit set as 1. The SYN (Synchronize) flag is the TCP packet flag that is used to initiate a TCP connection. A packet containing solely a SYN flag is the first part of the "three-way handshake" of TCP connection initiation. It is responded to with a SYN-ACK packet. Packets setting the SYN flag can also be used to perform a SYN flood and a SYN scan.
RST.Flag.Count) = The number of times the packets sent in the flow (in both directions) had the RST (Reset) flag bit set as 1 - (An RST says reset the connection. It must be sent whenever a segment arrives which apparently is not intended for the current connection - FIN says, "I finished talking to you, but I'll still listen to everything you have to say until you're done" (Wait for an ACK) RST says, "There is no conversation. I am resetting the connection!").
PSH.Flag.Count = The number of times the packets sent in the flow (in both directions) had the PSH (Pushing) flag bit set as 1.
ACK.Flag.Count = The number of times the packets sent in the flow (in both directions) had the ACK (Acknowledged) flag bit set as 1. To establish a connection, TCP uses a three-way handshake. Before a client attempts to connect with a server, the server must first bind to and listen at a port to open it up for connections: this is called a passive open. Once the passive open is established, a client may initiate an active open.
URG.Flag.Count = The number of times the packets sent in the flow (in both directions) had the URG (Urgent) flag bit set as 1.
CWE.Flag.Count = The number of times the packets sent in the flow (in both directions) had the CWR (Congestion Window Reduced) TCP flag set as 1. During the synchronization phase of a connection between client and server, the TCP CWR and ECE (Explicit Congestion Notification - Echo) flags work in conjunction to establish whether the connection is capable of leveraging congestion notification. In order to work, both client and server need to support ECN (Explicit Congestion Notification). To accomplish this, the sender sends a SYN packet with the ECE and CWR flags set, and the receiver sends back the SYN-ACK with only the ECE flag set. Any other configuration indicates a non-ECN setup.
ECE.Flag.Count = The number of times the packets sent in the flow (in both directions) had the ECE (Explicit Congestion Notification Echo) TCP flag set as 1.
Down.Up.Ratio = Download and upload ratio.
Average.Packet.Size = The average size of each packet. It is important to notice that Packet Length specify the size of the whole packet including the header, trailer and the data that send on that packet. But Packet Size specify only the size of the header on the packet.
Avg.Fwd.Segment.Size = The average segment size observed in the forward direction. A TCP segment is the Protocol Data Unit (PDU) which consists of a TCP header and an application data piece which comes from the upper Application Layer. Transport layer data is generally named as segment and network layer data unit is named as datagram but when UDP is used as transport layer protocol the data unit is called UDP datagram since the UDP data unit is not segmented (segmentation is made in transport layer when TCP is used).
Avg.Bwd.Segment.Size = Average Segment size observed in the backward direction.
Fwd.Header.Length.1The header length of the packets flow in the forward direction. This attribute has the exact same values than the attribute Fwd Header Length, hence it can be a bug on the CICFlowmeter software.
Fwd.Avg.Bytes.Bulk = The average number of bytes bulk rate in the forward direction. Bulk data transfer is a software-based mechanism designed to move large data file using compression, blocking and buffering methods to optimize transfer times.
Fwd.Avg.Packets.Bulk = Average number of packets bulk rate in the forward direction.
Fwd.Avg.Bulk.Rate = Average number of bulk rate in the forward direction.
Bwd.Avg.Bytes.Bulk = Average number of bytes bulk rate in the backward direction.
Bwd.Avg.Packets.Bulk = Average number of packets bulk rate in the backward direction.
Bwd.Avg.Bulk.Rate = Average number of bulk rate in the backward direction.
Subflow.Fwd.Packets = The average number of packets in a subflow in the forward direction. The core idea of multipath TCP is to define a way to build a connection between two hosts and not between two interfaces (as standard TCP does). In standard TCP, the connection should be established between two IP addresses. Each TCP connection is identified by a four-tuple (source and destination addresses and ports). Given this restriction, an application can only create one TCP connection through a single link. Multipath TCP allows the connection to use several paths simultaneously. For this, Multipath TCP creates one TCP connection, called subflow, over each path that needs to be used. The detailed protocol specification is provided in RFC 6824
Subflow.Fwd.Bytes = The average number of bytes in a subflow in the forward direction.
Subflow.Bwd.Packets = The average number of packets in a subflow in the backward direction.
Subflow.Bwd.Bytes = The average number of bytes in a subflow in the backward direction.
Init_Win_bytes_forwardThe total number of bytes sent in the initial window in the forward direction. TCP uses a sliding window flow control protocol. In each TCP segment, the receiver specifies in the receive window field the amount of additionally received data (in bytes) that it is willing to buffer for the connection. The sending host can send only up to that amount of data, before it must wait for an acknowledgment and window update from the receiving host.
Init_Win_bytes_backward = The total number of bytes sent in the initial window in the backward direction.
act_data_pkt_fwd = Count of packets with at least one byte of TCP data payload in the forward direction.
min_seg_size_forward = Minimum segment size observed in the forward direction.
Active.Mean = The mean time a flow was active before becoming idle.
Active.Std = Standard deviation time a flow was active before becoming idle.
Active.Max = Maximum time a flow was active before becoming idle.
Active.Min = Minimum time a flow was active before becoming idle.
Idle.Mean = Mean time a flow was idle before idle before becoming active.
Idle.Std = Standard deviation time a flow was idle before becoming active.
Idle.Max = The maximum time a flow was idle before becoming active.
Idle.Min = The minimum time a flow was idle before becoming active.
Label = The state of the flow (benign or malign).
L7Protocol = This attribute represents the code number of the layer 7 protocol as obtained from nDPI in Ntopng application. It is a number that varies from 0 to 226 (e.g., 0 is labeled as Unknown application).
ProtocolName = This attribute is the objective class of the dataset. It holds the application name following the code number stored in the L7Protocol attribute (e.g., YouTube, Yahoo, Facebook, etc.).