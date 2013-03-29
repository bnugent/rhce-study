# RHCE Study Guide
Based on [RHCE Objectives](https://www.redhat.com/training/courses/ex300/examobjective) retrieved 2013-01-15

*Disclaimer: This is a simple study-guide based on the published RHCE objectives. It is __not__ a "brain dump" nor in any way meant to cheat the EX300 exam.*

## System configuration and management

### Route IP traffic and create static routes.
* Set a default route:

```bash
ip route add default dev eth0
# OR using next hop IP
ip route add default via 192.168.0.1
```
* Create a static route:

```bash
ip route add 172.16.0.0/12 dev eth1
# OR via next hop IP
ip route add 172.16.0.0/12 via 192.168.0.1
```
### Use iptables to implement packet filtering and configure network address translation (NAT).
#### Packet Filtering
* List current iptables rules:

```bash
iptables -nvL
```
* List current iptables rules in /etc/sysconfig/iptables format:

```bash
iptables -vS
```
* Set default policy for filter table:

```bash
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
```
* Allow SSH:

```bash
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```
* Allow HTTP/S:

```
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```
* Block a suspicious network:

```bash
iptables -A INPUT -i eth0 -s 192.168.8.0/24 -j DROP
```
#### Network Address Translation (NAT)
##### Configure iptables for IP masquerading

```bash
# eth0 is public; eth1 is private on a 192.168.9.9/24 network:
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o eth1 -j MASQUERADE
```
* Enable IP Forwarding
  * edit /etc/sysctl.conf and change the following:

```
net.ipv4.ip_forward = 1
```
  * reload sysctl settings:

```bash
sysctl -p
```
  * OPTIONAL: enable IP forwarding for current running system:

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```
* Configure iptables to allow forwarding between interfaces:

```bash
iptables -A FORWARD -o eth1 -j ACCEPT
iptables -A FORWARD -o eth0 -j ACCEPT
```
##### DNAT
* Forward incoming traffic on port 8800 to port 80 on internal host 192.168.0.5:

```bash
iptables -t nat -I PREROUTING -p tcp --dport 8800 -j DNAT --to-destination 192.168.0.5:80
```
### Use /proc/sys and sysctl to modify and set kernel runtime parameters.
* Change dynamically: /proc/sys/*
* Change persistently: /etc/sysctl.conf && `sysctl -p`
* Examples:

```
# Ensure that packets entering an external interface are in fact external:
net.ipv4.conf.default.rp_filter = 1
# Disable source routing:
net.ipv4.conf.default.accept_source_route = 0
# Disable magic sysrq key combo (REISUB):
kernel.sysrq = 0
# Include PID number in core dumps:
kernel.core_uses_pid = 1
# Protect against "ping of death" attacks:
net.ipv4.tcp_syncookies = 1
# Disable use of iptables, ip6tables, and arptables on bridges:
net.bridge.bridge-nf-call-ip6tables = 0
net.bridge.bridge-nf-call-iptables = 0
net.bridge.bridge-nf-call-arptables = 0
```
### Configure a system to authenticate using Kerberos.
### Build a simple RPM that packages a single file.
```bash
yum install rpmdevtools
# as non-root user:
rpmdev-setuptree
mkdir example-1.0
echo "Here is some text." > example-1.0/example-file.txt
tar czf example-1.0.tar.gz example-1.0
cp example-1.0.tar.gz rpmbuild/SOURCES
rpmdev-newspec rpmbuild/SPECS/example.spec
# edit rpmbuild/SPECS/example.spec accordingly
rpm -ba rpmbuild/SPECS/example.spec
```
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

