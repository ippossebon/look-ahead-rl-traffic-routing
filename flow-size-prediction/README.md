**Creating features file from `nfcapd`:**

Example:
`nfdump -r nfcapd.201706271035 -o csv > nfcapd.201706271035.csv`



**Dataset description**

| **Indices used in nfdump 1.6**                               | **Description**                            |
|--------------------------------------------------------------|--------------------------------------------|
| ts,te,td                                                     | time records: t-start, t-end, duration     |
| sa,da                                                        | src dst address                            |
| sp,dp                                                        | src, dst port                              |
| pr                                                           | protocol (TCP = 1, UDP = 2)                |
| flg                                                          | flags                                      |
| fwd                                                          | forwarding status                          |
| stos                                                         | src tos                                    |
| ipkt,ibyt                                                    | input packets/bytes                        |
| opkt,obyt                                                    | output packets, bytes                      |
| in,out                                                       | input/output interface SNMP number         |
| sas,das                                                      | src, dst AS                                |
| smk,dmk                                                      | src, dst mask                              |
| dtos                                                         | dst tos                                    |
| dir                                                          | direction                                  |
| nh,nhb                                                       | nethop IP address, bgp next hop IP         |
| svln,dvln                                                    | src, dst vlan id                           |
| ismc,odmc                                                    | input src, output dst MAC                  |
| idmc,osmc                                                    | input dst, output src MAC                  |
| mpls1,mpls2,mpls3,mpls4,mpls5,mpls6,mpls7,mpls8,mpls9,mpls10 | MPLS label 1-10                            |
| cl,sl,al                                                     | client server application latency (nprobe) |
| ra                                                           | router IP                                  |
| eng                                                          | router engine type/id                      |
| exid                                                         | exporter SysID                             |
