#do not run this as root
if [ `whoami` == root ]; then
    echo Please run this script as NON root
    exit
fi

#git clone and set to the havana branch
git clone https://github.com/openstack-dev/devstack.git
cp localrc devstack/localrc
cd devstack
git checkout stable/havana

