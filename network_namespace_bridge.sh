sudo ip link add 'br' type bridge
sudo ip link add br type bridge
sudo ip link add dev br type bridge
sudo ip link set dev br up
sudo ip netns add nns1
sudo ip netns add nns2
sudo ip netns add nns3
sudo ip link add dev 'nns1-eth' peer name 'br-eth1'
sudo ip link add dev 'nns1-eth' type veth peer name 'br-eth1'
sudo ip link add dev 'nns2-eth' type veth peer name 'br-eth2'
sudo ip netns delete nns3
sudo ip netns list
sudo ip link set 'nns1-eth' netns nns1
sudo ip link set 'nns2-eth' netns nns2
sudo ip link set 'br-eth1' master br
sudo ip link set 'br-eth2' master br
sudo ip link set dev br up
sudo ip link set dev 'br-eth1' up
sudo ip link set dev 'br-eth2' up
sudo ip netns exec nns1 ip link set dev nns1-eth up
sudo ip netns exec nns2 ip link set dev nns2-eth up
sudo ip netns exec nns1 ip link set dev 'lo' up
sudo ip netns exec nns2 ip link set dev 'lo' up
sudo ip addr add 10.0.0.1/24 dev br
sudo ip netns nns1 exec ip addr add 10.0.0.2/24 dev nns1-eth
sudo ip netns nns1 exec ip addr add 10.0.0.2/24 dev 'nns1-eth'
sudo ip netns exec nns1 ip addr add 10.0.0.2/24 dev 'nns1-eth'
sudo ip netns exec nns2 ip addr add 10.0.0.3/24 dev 'nns2-eth'
sudo ip netns exec nns1 ip route add default via 10.0.0.1 dev nns1-eth
sudo ip netns exec nns2 ip route add default via 10.0.0.1 dev nns2-eth
sudo iptables --append FORWARD --in-interface br --jump ACCEPT
sudo iptables --append FORWARD --out-interface br --jump ACCEPT
sudo ip netns exec nns1 ping 10.0.0.3
sudo ip netns exec nns2 ping 10.0.0.2

