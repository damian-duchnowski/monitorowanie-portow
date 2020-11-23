import smtplib

from parse_input import *
from scan import *
from settings import *

from datetime import datetime
from email.mime.text import MIMEText
from socket import gaierror


def get_messages_to_send():
    '''Return messages to send based on comparison of ports that should be open and ports that are actually open.'''
    messages_to_send = []

    for ip_addr in find_uniq_ip_addr():
        actual_open_tcp_ports = get_open_ports(ip_addr, 'tcp')
        if len(actual_open_tcp_ports) is not 0:
            if actual_open_tcp_ports[0] is not 'DOWN':
                for entry in match_ports_with_ip():
                    if entry['ip'] == ip_addr:
                        if entry['tcp_ports'] != actual_open_tcp_ports:
                            combined = entry['tcp_ports'] + \
                                actual_open_tcp_ports
                            combined = set(combined)
                            combined = sorted(combined)

                            should_be_closed = []
                            should_be_open = []
                            for port in combined:
                                if port in entry['tcp_ports'] and port not in actual_open_tcp_ports:
                                    should_be_open.append(port)
                                if port not in entry['tcp_ports'] and port in actual_open_tcp_ports:
                                    should_be_closed.append(port)

                            if len(should_be_closed) is not 0:
                                messages_to_send.append('Port(s) {} on host {} should be closed but seem open.'.format(
                                    should_be_closed, ip_addr))
                            if len(should_be_open) is not 0:
                                messages_to_send.append('Port(s) {} on host {} should be open but seem closed.'.format(
                                    should_be_open, ip_addr))
            else:
                messages_to_send.append('Host {} is down.'.format(ip_addr))
        else:
            messages_to_send.append(
                'Host {} has all ports closed.'.format(ip_addr))

    return messages_to_send


def send_emails(email_addr_list=get_recipients()):
    '''Send emails to recipients from get_recipients with messages from get_messages_to_send.'''
    for email_addr in email_addr_list:
        port = SMTP_PORT
        smtp_server = SMTP_SERVER
        login = SMTP_LOGIN
        password = SMTP_PASSWORD

        sender = SMTP_SENDER
        receiver = email_addr

        msg = MIMEText('\n'.join(get_messages_to_send()))

        msg['Subject'] = 'Port monitoring warning at {}'.format(
            datetime.now().isoformat(timespec='minutes'))
        msg['From'] = sender
        msg['To'] = receiver

        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.login(login, password)
                server.sendmail(sender, receiver, msg.as_string())
            print('Warning sent to {} at {}'.format(
                receiver, datetime.now().isoformat(timespec='seconds')))
        except (gaierror, ConnectionRefusedError):
            sys.exit('Failed to connect to the server. Bad connection settings?')
        except smtplib.SMTPServerDisconnected:
            sys.exit('Failed to connect to the server. Wrong user/password?')
        except smtplib.SMTPException as e:
            sys.exit('SMTP error occurred: ' + str(e))
