## Running the vagrant setup.

To gain access to the IOS-XR vagrant box, take a look at the following tutorial on [xrdocs](https://xrdocs.github.io):

[IOS-XR vagrant quickstart](https://xrdocs.github.io/application-hosting/tutorials/iosxr-vagrant-quickstart)


Assuming you've downloaded the IOS-XR vagrant box and named it `"IOS-XRv"`, you can proceed with the steps below. If you name it something different, make sure you edit the Vagrantfile in this folder.

Copy the `python/` folder into the `vagrant/` folder of the cloned repo:

```
server:~/ciscoiosxr-slapi-examples$ cp -r python/ vagrant/
server:~/ciscoiosxr-slapi-examples$ ls -l vagrant/
total 16
drwxrwxr-x 2 cisco cisco 4096 Jul  9 22:40 configs
drwxrwxr-x 4 cisco cisco 4096 Jul  9 22:47 python
drwxrwxr-x 2 cisco cisco 4096 Jul  9 22:40 scripts
-rw-rw-r-- 1 cisco cisco 1567 Jul  9 22:40 Vagrantfile
server:~/ciscoiosxr-slapi-examples$ 

```


Switch into the `vagrant/` directory of this cloned repository and issue a `vagrant up`

```

server:~/ciscoiosxr-slapi-examples/vagrant$ vagrant up
Bringing machine 'rtr' up with 'virtualbox' provider...
Bringing machine 'devbox' up with 'virtualbox' provider...
==> rtr: Importing base box 'IOS-XRv'...


```

Once the boxes are up, ssh into the devbox and cd into the `/vagrant/python/` directory. Now follow the instructions detailed in the python folder README.md to run your examples.  

**The genpy folder will need to be created by the user and must contain the generated python grpc client bindings for IOS-XR SL-API **  

```
server:~/slapi/vagrant-examples/iosxr-grpc-setup$ vagrant ssh devbox
Welcome to Ubuntu 14.04.4 LTS (GNU/Linux 3.13.0-87-generic x86_64)

 * Documentation:  https://help.ubuntu.com/

  System information as of Mon Jul 10 05:10:25 UTC 2017

  System load:  0.0               Users logged in:     0
  Usage of /:   9.6% of 39.34GB   IP address for eth0: 10.0.2.15
  Memory usage: 6%                IP address for eth1: 11.1.1.20
  Swap usage:   0%                IP address for eth2: 12.1.1.20
  Processes:    75                IP address for eth3: 13.1.1.20

  Graph this data and manage this system at:
    https://landscape.canonical.com/

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

31 packages can be updated.
12 updates are security updates.

New release '16.04.2 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


Last login: Mon Jul 10 05:10:25 2017 from 10.0.2.2

vagrant@vagrant-ubuntu-trusty-64:~$ cd /vagrant/python
vagrant@vagrant-ubuntu-trusty-64:/vagrant/python$ ls
client_init.py  genpy  interface.py  mpls_ilm.py  README.md  route.py  util  vrf.py
vagrant@vagrant-ubuntu-trusty-64:/vagrant/python$ 
vagrant@vagrant-ubuntu-trusty-64:/vagrant/python$ export SERVER_IP=10.0.2.2
vagrant@vagrant-ubuntu-trusty-64:/vagrant/python$ export SERVER_PORT=57344
vagrant@vagrant-ubuntu-trusty-64:/vagrant/python$ python mpls_ilm.py 
Using GRPC Server IP(10.0.2.2) Port(57344)
Global thread spawned
Server Returned 0x502, Version 0.0.0
Successfully Initialized, connection established!
Max VRF Name Len     : 33
Max Iface Name Len   : 64
Max Paths per Entry  : 128
Max Prim per Entry   : 64
Max Bckup per Entry  : 64
Max Labels per Entry : 3
Min Prim Path-id     : 1
Max Prim Path-id     : 64
Min Bckup Path-id    : 65
Max Bckup Path-id    : 128
Max Remote Bckup Addr: 2
MPLS SL_OBJOP_ADD Success!
MPLS SL_OBJOP_UPDATE Success!
vagrant@vagrant-ubuntu-trusty-64:/vagrant/python$ 

```







