# RHCE Study Guide
Based on [RHCE Objectives](https://www.redhat.com/training/courses/ex300/examobjective) retrieved 2013-01-15

*Disclaimer: This is a simple study-guide based on the published RHCE objectives. It is __not__ a "brain dump" nor in any way meant to cheat the EX300 exam.*

## System configuration and management

### Route IP traffic and create static routes.
* Set a default route:
    `ip route add default dev eth0`
    `# OR using next hop IP`
    `ip route add default via 192.168.0.1`
* Create a static route:
    `ip route add 172.16.0.0/12 dev eth1`
    `# OR via next hop IP`
    `ip route add 172.16.0.0/12 via 192.168.0.1`
### Use iptables to implement packet filtering and configure network address translation (NAT).
#### Packet Filtering
* List current iptables rules:
    `iptables -nvL`
* List current iptables rules in /etc/sysconfig/iptables format:
    `iptables -vS`
* Set default policy for filter table:
    `iptables -P INPUT DROP`
    `iptables -P FORWARD DROP`
    `iptables -P OUTPUT ACCEPT`
* Allow SSH:
    `iptables -A INPUT -p tcp --dport 22 -j ACCEPT`
* Allow HTTP/S:
    `iptables -A INPUT -p tcp --dport 80 -j ACCEPT`
    `iptables -A INPUT -p tcp --dport 443 -j ACCEPT`
* Block a suspicious network:
    `iptables -A INPUT -i eth0 -s 192.168.8.0/24 -j DROP`
#### Network Address Translation (NAT)
1. Configure iptables for IP masquerading
    `# eth0 is public; eth1 is private on a 192.168.9.9/24 network:`
    `iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o eth1 -j MASQUERADE`
2. Enable IP Forwarding
* edit /etc/sysctl.conf and change the following:
    `net.ipv4.ip_forward = 1`
* reload sysctl settings:
    `sysctl -p`
* OPTIONAL: enable IP forwarding for current running system:
    `echo 1 > /proc/sys/net/ipv4/ip_forward`
3. Configure iptables to allow forwarding between interfaces:
    `iptables -A FORWARD -o eth1 -j ACCEPT`
    `iptables -A FORWARD -o eth0 -j ACCEPT`
### Use /proc/sys and sysctl to modify and set kernel runtime parameters.
### Configure a system to authenticate using Kerberos.
### Build a simple RPM that packages a single file.
### Configure a system as an iSCSI initiator that persistently mounts an iSCSI target.
### Produce and deliver reports on system utilization (processor, memory, disk, and network).
### Use shell scripting to automate system maintenance tasks.
### Configure a system to log to a remote system.
### Configure a system to accept logging from a remote system.

## Network services

Network services are an important subset of the exam objectives. RHCE candidates should be capable of meeting the following objectives for each of the network services listed below:

* Install the packages needed to provide the service.
* Configure SELinux to support the service.
* Configure the service to start when the system is booted.
* Configure the service for basic operation.
* Configure host-based and user-based security for the service.

## HTTP/HTTPS

### Configure a virtual host.
### Configure private directories.
### Deploy a basic CGI application.
### Configure group-managed content.

## DNS

### Configure a caching-only name server.
### Configure a caching-only name server to forward DNS queries.
### Note: Candidates are not expected to configure master or slave name servers.

## FTP

### Configure anonymous-only download.

## NFS

### Provide network shares to specific clients.
### Provide network shares suitable for group collaboration.

## SMB

### Provide network shares to specific clients.
### Provide network shares suitable for group collaboration.

## SMTP

### Configure a mail transfer agent (MTA) to accept inbound email from other systems.
### Configure an MTA to forward (relay) email through a smart host.

## SSH

### Configure key-based authentication.
### Configure additional options described in documentation.

## NTP

### Synchronize time using other NTP peers.

