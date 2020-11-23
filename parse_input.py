import re
import sys

IPV4_REGEX = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
IPV6_REGEX = r'(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$'

EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+'


def find_uniq_ip_addr():
    '''Return list of all unique ip_addr found in input file.'''
    with open('wzorcowe_porty', 'r') as f:  # TODO: Zmienić z powrotem na sys.argv[1]
        ip_addr = []
        for line in f:
            ip = line.split(';')[0]
            if re.match(IPV4_REGEX, ip) or re.match(IPV6_REGEX, ip):
                if ip not in ip_addr:
                    ip_addr.append(ip)
            else:
                if ';' in line:
                    sys.exit('{} is not a valid IP address!'.format(ip))
        ip_addr.sort()
    return ip_addr


def match_ports_with_ip():
    '''Return list of ip_addr and their corresponding ports from input file.'''
    entries = []
    for ip in find_uniq_ip_addr():
        tcp_ports = []
        udp_ports = []
        # TODO: Zmienić z powrotem na sys.argv[1]
        with open('./wzorcowe_porty', 'r') as f:
            for line in f:
                if ip == line.split(';')[0]:
                    protocol = line.split(';')[1].lower()
                    port = int(line.split(';')[2].strip('\n'))
                    if port in range(1, 65536):
                        if protocol == 'tcp' and port not in tcp_ports:
                            tcp_ports.append(port)
                        # UDP is not supported for now.
                        '''
                        if protocol == 'udp' and port not in udp_ports:
                            udp_ports.append(port)
                        '''
                    else:
                        if ';' in line:
                            sys.exit(
                                '{} is not a valid port number!'.format(port))
            # entries.append({'ip': ip, 'tcp_ports': tcp_ports, 'udp_ports': udp_ports})
            entries.append({'ip': ip, 'tcp_ports': tcp_ports})
    return entries


def get_recipients():
    '''Return list of email addresses in input file of users to be notified.'''
    with open('wzorcowe_porty', 'r') as f:
        return re.findall(EMAIL_REGEX, f.read())
