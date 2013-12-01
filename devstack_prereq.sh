#run this as root
if [ `whoami` != root ]; then
    echo Please run this script as root or using sudo
    exit
fi
#update apt repo
apt-get update
#install could keyring for grizzly
apt-get install ubuntu-cloud-keyring python-software-properties software-properties-common python-keyring
echo deb http://ubuntu-cloud.archive.canonical.com/ubuntu precise-updates/grizzly main >> /etc/apt/sources.list.d/grizzly.list
#upgrade system
apt-get update
apt-get upgrade
#setup network interfaces
echo "#For Exposing OpenStack API over the internet
auto eth0
iface eth0 inet dhcp

#Not internet connected(used for OpenStack management)
auto eth1
iface eth1 inet manual
up ip link set $IFACE up
down ip link set $IFACE down" >> /etc/network/interfaces
service networking restart
#install devstack stuff
apt-get install openvswitch-switch openvswitch-datapath-dkms
#setup ovs bridge
ovs-vsctl add-br br-eth1
ovs-vsctl add-port br-eth1 eth1
