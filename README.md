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
```bash
# GUI
system-config-authentication
# Console
authconfig-tui
```

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
```bash
yum install iscsi-initiator-utils
iscsiadm -m discoverydb -t st -p 192.168.0.5 -D
/etc/init.d/iscsi start
/etc/init.d/iscsi status
chkconfig iscsi on
```
### Produce and deliver reports on system utilization (processor, memory, disk, and network).
* Any permutation of `ps`, `top`, `sar` will do.

### Use shell scripting to automate system maintenance tasks.
*N/A*
### Configure a system to log to a remote system.
* Send via UDP to 192.168.8.3:514

```bash
# /etc/rsyslog.conf
*.* @192.168.8.3:514
```
* Send via TCP to 192.168.8.3:514

```bash
# /etc/rsyslog.conf:
*.* @@192.168.8.3:514
```
### Configure a system to accept logging from a remote system.
* Accept via UDP on port 514

```bash
# /etc/rsyslog.conf:
$ModLoad imudp
$UDPServerRun 514
```
* Accept via TCP on port 514

```bash
# /etc/rsyslog.conf:
$ModLoad imtcp
$InputTCPServerRun 514
```
## Network services

Network services are an important subset of the exam objectives. RHCE candidates should be capable of meeting the following objectives for each of the network services listed below:

* Install the packages needed to provide the service.
* Configure SELinux to support the service.
* Configure the service to start when the system is booted.
* Configure the service for basic operation.
* Configure host-based and user-based security for the service.

## HTTP/HTTPS
* Install the packages needed to provide the service.

```bash
yum install httpd
# Alternately, install the default packages in the "Web Server" group
yum groupinstall "Web Server"
```
* Configure SELinux to support the service.

```bash
# show SELinux booleans for http
getsebool -a | grep http

# Create a web directory (for vhosts)
mkdir -p /www
chcon -R -u system_u /www/
chcon -R -t httpd_sys_content_t /www/
semanage fcontext -a -s system_u -t httpd_sys_content_t /www/
```
* Configure the service to start when the system is booted.

```bash
chkconfig httpd on
```
* Configure the service for basic operation.
  1. Install httpd
  2. Set httpd to start on boot
  3. Configure SELinux booleans
  4. Open port 80 in iptables
* Configure host-based and user-based security for the service.
  * Host

```bash
iptables -A INPUT -m state --state NEW -m tcp -p tcp -s 192.168.8.0/24 --dport 80 -j ACCEPT
```
```apache
# Alternately via .htaccess
Order deny,allow
Deny from all
Allow from 192.168.8.8
```
  * User

```bash
htpasswd -c /var/www/.htpasswd user
```
```apache
AuthType Basic
AuthName "Private Area"
AuthUserFile /var/www/.htpasswd
Require valid-user
Order deny,allow
Deny from all
```
### Configure a virtual host.
* Create /etc/httpd/conf.d/virtualhost.conf

```apache
NameVirtualHost *:80
<VirtualHost *:80>
  ServerName vhost.example.com
  DocumentRoot /path/to/docroot
</VirtualHost>
```
### Configure private directories.
* Use *AuthType* above 

### Deploy a basic CGI application.
* Edit /etc/httpd/conf/httpd.conf

```apache
<Directory /var/www/html>
...
  Options +ExecCGI
  AddHandler cgi-script .pl
...
</Directory>
```
```bash
httpd -t && service httpd restart
```
* Create a script

```bash
cat > /var/www/html/hello.pl <EOF
#!/usr/bin/perl
print "Content-type: text/html\n\n";
print "Hello!";
EOF

chmod 755 /var/www/html/hello.pl
```
* Make SELinux work

```bash
chcon --reference=/var/www/cgi-bin hello.pl
# persist (non-optimal, but works)
semanage fcontext -a -s system_u -t httpd_sys_script_exec_t /var/www/html/hello.pl
```
### Configure group-managed content.
```bash
groupadd webdesigners
gpasswd -a user1 webdesigners
gpasswd -a user2 webdesigners
mkdir -p /www/site1
chown -R apache:webdesigners /www/site1
chmod 2775 /www/site1
```

## DNS
* Install the packages needed to provide the service.

```bash
yum install bind
```
* Configure SELinux to support the service.

```bash
getsebool -a | grep named
# or
man named_selinux
```
* Configure the service to start when the system is booted.

```bash
chkconfig named on
```
* Configure the service for basic operation.
  1. Install service
  2. “Configure a caching-only name server”
  3. Configure the service to start when the system is booted
  4. Configure SELinux support
  5. Update /etc/sysconfig/iptables:

```bash
iptables -A INPUT -p tcp -m tcp --dport 53 -j ACCEPT
iptables -A INPUT -p udp -m udp --dport 53 -j ACCEPT
```
* Configure host-based and user-based security for the service.
  * Can be done via `iptables` and/or the `allow-query` directive in /etc/named.conf

### Configure a caching-only name server.
* This is default when you install named, but limited to the localhost. Just open up to the network.

```named
# /etc/named.conf:
...
acl good_ips { 192.168.8.0/24; 127.0.0.0/8 };
...
options {
  listen-on port 53 {
    127.0.0.1;
    192.168.8.5;
  };
  ...
  allow-query { good_ips; };
  allow-query-cache { good_ips };
  recursion yes;
  ...
};
```
### Configure a caching-only name server to forward DNS queries.
* Same caching config as above, but also add the following under options:

```named
...
  forwarders {
    192.168.8.1;
  };
  forward first;
...
```
### Note: Candidates are not expected to configure master or slave name servers.

## FTP
* Install the packages needed to provide the service.
* Configure SELinux to support the service.
* Configure the service to start when the system is booted.
* Configure the service for basic operation.
* Configure host-based and user-based security for the service.

### Configure anonymous-only download.

## NFS
* Install the packages needed to provide the service.
* Configure SELinux to support the service.
* Configure the service to start when the system is booted.
* Configure the service for basic operation.
* Configure host-based and user-based security for the service.

### Provide network shares to specific clients.
### Provide network shares suitable for group collaboration.

## SMB
* Install the packages needed to provide the service.
* Configure SELinux to support the service.
* Configure the service to start when the system is booted.
* Configure the service for basic operation.
* Configure host-based and user-based security for the service.

### Provide network shares to specific clients.
### Provide network shares suitable for group collaboration.

## SMTP
* Install the packages needed to provide the service.

```bash
yum groupinstall "E-mail server"
```
* Configure SELinux to support the service.

```bash
getsebool -a | grep postfix
```
* Configure the service to start when the system is booted.

```bash
chkconfig postfix on
```
* Configure the service for basic operation.
  1. Install postfix
  2. Configure postfix to run on boot
  3. Configure SELinux
  4. Open port 25 in `iptables`
* Configure host-based and user-based security for the service.
  * User:

```postfix
# /etc/postfix/main.cf:
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
broken_sasl_auth_clients = yes
smtpd_recipient_restrictions = permit_sasl_authenticated, permit_mynetworks, reject_unauth_destination
```
```bash
service saslauthd start
service saslauthd start
chkconfig saslauthd on
```
* Host:
  * Use `iptables`

### Configure a mail transfer agent (MTA) to accept inbound email from other systems.
```postfix
# /etc/postfix/main.cf
...
myhostname = mail.example.com
...
mydomain = example.com
...
inet_interfaces = all
...
mydestination = $mydomain, $myhostname, localhost.$mydomain, localhost
...
mynetworks = 192.168.8.0/24, 127.0.0.0/8
```
### Configure an MTA to forward (relay) email through a smart host.
```postfix
# /etc/postfix/main.cf
...
relayhost = 192.168.100.5
```

## SSH
* Install the packages needed to provide the service.

```bash
# should be installed already, but:
yum install openssh
```
* Configure SELinux to support the service.
*N/A*

* Configure the service to start when the system is booted.

```bash
chkconfig sshd on
```
* Configure the service for basic operation.
  1. Install ssh
  2. Configure sshd to run on boot
  3. Configure SELinux
  4. Open port 22 in `iptables`
* Configure host-based and user-based security for the service.
  * Host: Use TCPWrappers via /etc/hosts.allow and/or `iptables`
  * User: `AllowUsers user@host` in /etc/ssh/sshd_config

### Configure key-based authentication.
* Enable:

```bash
# /etc/ssh/sshd_config:
...
PubKeyAuthentication yes
...
```
* Setup keys

```bash
ssh-keygen -t rsa
```
### Configure additional options described in documentation.

## NTP
* Install the packages needed to provide the service.

```bash
yum install ntp
```
* Configure SELinux to support the service.
*N/A*

* Configure the service to start when the system is booted.

```bash
chkconfig ntpd on
```
* Configure the service for basic operation.
  1. Install NTP
  2. Chkconfig NTP on
  3. Edit /etc/ntp.conf to work as a server
  4. Start ntpd
  5. Open port 123
* Configure host-based and user-based security for the service.
  * Use `iptables`

### Synchronize time using other NTP peers.
  * Edit /etc/ntp.conf

```bash
# Remove, at minimum, the nopeer restriction option
restrict default kod nomodify notrap noquery
...
# Allow hosts on local network to query
restrict 192.168.8.0 mask 255.255.255.0 nomodify notrap
...
# Use an upstream server
server 0.rhel.pool.ntp.org
server 1.rhel.pool.ntp.org
server 2.rhel.pool.ntp.org
```
