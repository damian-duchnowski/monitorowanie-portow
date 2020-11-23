import re
import subprocess
import sys


def get_open_ports(ip_addr, protocol='tcp'):
    '''Return list of all open ports for given ip_addr and protocol upon checking if host is up.'''
    if protocol.lower() == 'tcp':
        cmd = 'sudo nmap -oG - -sS -p- ' + ip_addr
        result = subprocess.check_output(cmd.split(' ')).decode()
        num_of_hosts_up = int(re.findall(r'(?<=\()\d(?=\s)', result)[0])

        if num_of_hosts_up == 1:
            open_tcp_ports = re.findall(
                r'\d+\/\w+\/\w+', result.split('\t')[2])
            for i, tcp_port in enumerate(open_tcp_ports):
                open_tcp_ports[i] = int(tcp_port.split('/')[0])
        else:
            open_tcp_ports = []
            open_tcp_ports.append('DOWN')

        return open_tcp_ports

    # UDP is not supported for now.
    '''
    if protocol.lower() == 'udp':
        cmd = 'nmap -oG - -sUV -T4 -F --version-intensity 0 ' + ip_addr   # Usunąć -T4?
        result = subprocess.check_output(cmd.split(' ')).decode()

        open_udp_ports = re.findall('\d+\/\w+\/\w+', result.split('\t')[2])
        for i, udp_port in enumerate(open_udp_ports):
            open_udp_ports[i] = int(udp_port.split('/')[0])

        return open_udp_ports
    '''
