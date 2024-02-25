sudo apt update 
sudo apt install iproute2 net-tools iputils-ping tcpdump -y
sudo ip netns add red
sudo ip netns add green
sudo ip link add dev br type bridge
sudo ip link set dev br up
sudo ip link add dev red-eth type veth peer name br-red
sudo ip link add dev green-eth type veth peer name br-green 
sudo ip link set red-eth netns red
sudo ip link set green-eth netns green
sudo ip link set br-red master br
sudo ip link set br-green master br 
sudo ip addr add 10.0.0.1/24 dev br
sudo ip link set br-red up
sudo ip link set br-green up
sudo ip netns exec red bash ip addr add 10.0.0.2/24 dev red-eth
sudo ip netns exec red bash ip link set red-eth up
sudo ip netns exec green ip link set green-eth up
sudo ip netns exec green ip addr add 10.0.0.3/24 dev green-eth
sudo ip netns exec red ip route add default via 10.0.0.1
sudo ip netns exec green ip route add default via 10.0.0.1
sudo apt install iptables
sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -j MASQUERADE
sudo iptables -A FORWARD --in-interface br -j ACCEPT 
sudo iptables -A FORWARD --out-interface br -j ACCEPT
