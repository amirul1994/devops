sudo ip netns add nns1
sudo ip netns add nns2
sudo ip link add 'nns1-eth' type veth peer name 'nns-eth'
sudo ip link add 'nns1-eth' type veth peer name 'nns2-eth'
sudo ip link delete 'nns1-eth' type veth peer name 'nns2-eth'
sudo ip link delete 'nns1-eth' type veth peer name 'nns-eth'
sudo ip link add 'nns1-eth' type veth peer name 'nns2-eth'
sudo ip link set dev 'nns1-eth' netns nns1
sudo ip link set dev 'nns2-eth' netns nns2
sudo ip netns exec nns1 ip link set 'nns1-eth' up
sudo ip netns exec nns2 ip link set 'nns2-eth' up
sudo ip netns exec nns2 ip link set 'lo' up
sudo ip netns exec nns1 ip link set 'lo' up
sudo ip netns nns1 ip addr add 10.0.0.1/24 dev 'nns1-eth'
sudo ip netns exec nns1 ip addr add 10.0.0.1/24 dev 'nns1-eth'
sudo ip netns exec nns1 ip route add default via 10.0.0.2 dev 'nns1-eth'
sudo ip netns exec nns2 ip addr add 10.0.0.2/24 dev 'nns2-eth'
sudo ip netns exec nns2 ip route add default via 10.0.0.2 dev 'nns2-eth'
sudo ip netns exec nns1 ping 10.0.0.2
sudo ip netns exec nns2 ping 10.0.0.1
