import socket
# pip install dnspython
import dns.resolver as dr
import re

"""
Port scanning.
Resolve host to IP first, if host is FQDN. After that scan ports
"""

ports = {
    20: 'ftp-data',
    21: 'ftp',
    22: 'ssh',
    23: 'telnet',
    25: 'smtp',
    53: 'domain',
    67: 'bootps',
    68: 'bootpc',
    69: 'tftp',
    80: 'http',
    110: 'pop3',
    137: 'netbios-ns',
    138: 'netbios-dgm',
    139: 'netbios-ssn',
    143: 'imap',
    161: 'snmp',
    179: 'bgp',
    389: 'ldap',
    443: 'https',
    500: 'isakmp',
    587: 'smtps',
    993: 'imaps',
    995: 'pop3s',
    3306: 'mysql',
    4569: 'iax',
    5060: 'sip'
}


def scan_ports(ports, host):
    print('Scanning ports...')
    for port in ports:
        s = socket.socket()
        s.settimeout(1)
        try:
            s.connect((host, port))
        except socket.error:
            pass
        else:
            s.close()
            print('{}:{} [{}]  port active'.format(host, str(port), ports[port]))


if __name__ == '__main__':
    try:
        host = input('Enter host: ').strip()
        if not re.search('\d+\.\d+\.\d+\.\d+', host):
            ip = dr.query(host, 'A')
            for rdata in ip:
                host = rdata
        scan_ports(ports, str(host))
    except KeyboardInterrupt:
        exit()
