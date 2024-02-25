First, a brief introduction to Linux namespace-

Linux namespace is a feature of the Linux kernel. It provides isolation for the system resources for a number of processes. That gives those processes to have a separate view of these resources. Docker calls Linux namespace APIs to create a docker container.Each namespace has a separate instance of a particular resource. Linux has seven default namespaces and the Network namespace is one of them. The network namespace decides a process’s ability to see the network devices. It has its own independent set of networking. The network namespace can have its own virtual network devices e.g. ethernet cables, switches, and ip addresses, routing tables, firewall rules, etc. 

Now dive into the lab –

First update the packages-

**sudo apt update**

Now I install the necessary packages, some of them are installed by default.

iproute2 – provides several utilities (like ip, bridge, etc.) for networking in the Linux kernel.

net-tools – provides tools like ifconfig, route, netstat, etc.

iputils-ping - is a utility whose purpose is to send ICMP echo requests.

tcpdump – a tool for packet analysis

**sudo apt install iproute2 net-tools iputils-ping tcpdump -y**

In Linux, it is possible to create a custom namespace. I shall create two network namespaces and name them ‘red’ and ‘green’.

**sudo ip netns add red**

**sudo ip netns add green**

List the newly created network namespaces

**sudo ip netns list**

Output:

green

red

Now, I shall create a bridge. The advantage of the bridge is, it will let multiple network namespaces communicate with each other without joining them via cable directly.

**sudo ip link add dev br type bridge**


‘Up’ the bridge.

**sudo ip link set dev br up**

To connect those network namespaces, first I have to create two virtual ethernet cables. For a cable, one side will be connected to the network namespace and the other side to the ‘bridge’. As I have two network namespaces, I have to create two virtual ethernet cables.

**sudo ip link add dev red-eth type veth peer name br-red**

**sudo ip link add dev green-eth type veth peer name br-green**

After that, connect the virtual ethernet cables on one side to the network namespaces.

**sudo ip link set red-eth netns red**

**sudo ip link set green-eth netns green**


Connect other sides of the cables to the bridge. For connecting to the bridge, the word ‘master’ has to be mentioned.

**sudo ip link set br-red master br**

**sudo ip link set br-green master br**

Now configure ip address to the bridge

**sudo ip addr add 10.0.0.1/24 dev br**

‘Up’ the bridge interfaces.

**sudo ip link set br-red up**

**sudo ip link set br-green up**

Execute the following command to enter into the ‘red’ network namespace.

**sudo ip netns exec red bash**

exec – will let execute a command for the network namespace

Configure ip address for the ‘red’ network namespace interface.

**ip addr add 10.0.0.2/24 dev red-eth**

‘Up’ the red-eth interface.

**ip link set red-eth up**

Similarly, ‘Up’ the green network namespace interface.

**sudo ip netns exec green ip link set green-eth up**

And also configure ip address for the green network namespace interface.

**sudo ip netns exec green ip addr add 10.0.0.3/24 dev green-eth**

At this stage,  I shall test connectivity between the ‘red’ and ‘green’ network namespaces.

Inside the ‘red’ network namespace.

**root@amirul:/home/amirul# ping 10.0.0.3**

PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.

64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.059 ms

64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.136 ms

64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.133 ms

64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.215 ms


Inside the ‘green’ network namespace.


**amirul@amirul:~$ sudo ip netns exec green bash**

root@amirul:/home/amirul# ping 10.0.0.2

PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.

64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=0.065 ms

64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.131 ms

64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.133 ms

64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.132 ms


If I want to the connectivity between the network namespaces and the ‘root’ namespace, I have to add a route for both network namespaces. I shall add a default route, so packets outside of the network namespaces network will exit through that ip address. In this case, it will be the bridge’s ip address.

Use the following command inside both network namespaces.

**ip route add default via 10.0.0.1**


At the present stage, I will ping 8.8.8.8 from both ‘red’ & ‘green’ namespace. The following incident occurs –


‘red’ network namespace

**root@amirul:/home/amirul# ping 8.8.8.8**

PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.

--- 8.8.8.8 ping statistics ---

10 packets transmitted, 0 received, 100% packet loss, time 9194ms


**‘green’ network namespace**

root@amirul:/home/amirul# ping 8.8.8.8

PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.


--- 8.8.8.8 ping statistics ---

10 packets transmitted, 0 received, 100% packet loss, time 9194ms


Listen on the ‘root’ namespace’s network interface.

**sudo tcpdump -i ens33 -p icmp**

-i: interface

ens33: name of the ‘root’ namespace’s network interface

-p: protocol


**amirul@amirul:~$ sudo tcpdump -i ens33 -p icmp**

[sudo] password for amirul:

tcpdump: verbose output suppressed, use -v[v]... for full protocol decode

listening on ens33, link-type EN10MB (Ethernet), snapshot length 262144 bytes

11:51:52.826387 IP 192.168.0.104 > dns.google: ICMP echo request, id 21464, seq 58, length 64

11:51:58.901259 IP 192.168.0.104 > amirul: ICMP redirect dns.google to net_gateway

11:51:58.901259 IP dns.google > amirul: ICMP echo request, id 16179, seq 63, length 64

11:51:59.284402 IP amirul > dns.google:: ICMP amirul udp port 43971 unreachable,length75

11:51:59..848381 IP amirul > dns.google:: ICMP amirul udp port45840 unreachable,length64

ICMP echo requests are got but no echo reply.

The reason behind this, I am trying to reach a public ip address from a private ip address without Network Address Translation (NAT). Therefore, I have to add a source NAT (SNAT) rule to the NAT table of the iptables. ‘iptables’ is a tool that allows filter, NAT, etc. for the ip-related information. 

Install the ‘iptables’ tool.

**sudo apt install iptables**
 
After that, add the following iptables rule

**sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -j MASQUERADE**

-t: table

nat: NAT

-A: append

POSTROUTING: for changing outgoing packets

-s: source

-j: Jump, which action I want to execute

MASQUERADE: it will alter the packets' ip address to the network interface’s ip address through which they will leave. In this scenario, they will leave through ens33. 


Now again ping from the ‘red’, and ‘green’ network namespaces and listen on the ens33 interface.


**amirul@amirul:~$ sudo ip netns exec red ping 8.8.8.8**

PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.

64 bytes from 8.8.8.8: icmp_seq=1 ttl=112 time=33.2 ms

64 bytes from 8.8.8.8: icmp_seq=2 ttl=112 time=35.2 ms

64 bytes from 8.8.8.8: icmp_seq=3 ttl=112 time=33.2 ms

64 bytes from 8.8.8.8: icmp_seq=4 ttl=112 time=32.2 ms

64 bytes from 8.8.8.8: icmp_seq=5 ttl=112 time=36.2 ms

64 bytes from 8.8.8.8: icmp_seq=6 ttl=112 time=37.2 ms

64 bytes from 8.8.8.8: icmp_seq=7 ttl=112 time=40.2 ms

64 bytes from 8.8.8.8: icmp_seq=8 ttl=112 time=35.2 ms


**amirul@amirul:~$ sudo ip netns exec green ping 8.8.8.8**

PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.

64 bytes from 8.8.8.8: icmp_seq=1 ttl=112 time=31.6 ms

64 bytes from 8.8.8.8: icmp_seq=2 ttl=112 time=36.2 ms

64 bytes from 8.8.8.8: icmp_seq=3 ttl=112 time=41.2 ms

64 bytes from 8.8.8.8: icmp_seq=4 ttl=112 time=32.2 ms



12:45:02.761506 IP 192.168.0.104 > amirul: ICMP redirect dns.google to net_gateway length 92

12:45:02.793417 IP dns.google > amirul: ICMP echo reply, id 9028, seq 1, length 64

12:45:03.763474 IP amirul > dns.google : ICMP echo request , id 9028 , seq 2 , length 64

12:45:03.763855 IP 192.168.0.104 > amirul : ICMP redirect dns.google to net_gateway length 92

12:45:03.805356 IP dns.google > amirul : ICMP echo reply , id 9028 , seq 2 , length 64

12:45:04.767656 IP amirul > dns.google : ICMP echo request , id 9028 , seq 3 , length 64


Now, it is getting ICMP echo replies.

Find out the ‘iptables’ NAT table.

**sudo iptables -t nat -L -n**

Chain POSTROUTING (policy ACCEPT)

target     prot opt source               destination         

MASQUERADE  all  --  172.17.0.0/16       0.0.0.0/0           

**MASQUERADE  all  --  10.0.0./24          0.0.0.0/0**


//Optional

Sometimes, in the iptables, if there is any blocking rule for forwarding via the bridge, it might block network namespaces packets. The rules below will allow forwarding through the bridge both for incoming and outgoing packets.

**sudo iptables -A FORWARD --in-interface br -j ACCEPT**

**sudo iptables -A FORWARD --out-interface br -j ACCEPT**
