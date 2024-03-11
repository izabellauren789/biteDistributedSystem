import socket
import sys
import struct
import csv
from datetime import datetime

def log_communication(type, time, source_ip, destination_ip, source_port, destination_port, protocol, length, flags):
    log_file = 'network_communications.csv'
    log_headers = ['Type', 'Time(s)', 'Source_Ip', 'Destination_Ip', 'Source_Port', 'Destination_Port', 'Protocol', 'Length (bytes)', 'Flags (hex)']
    
    # Check if log file exists and if headers are needed
    try:
        with open(log_file, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(log_headers)
    except FileExistsError:
        pass

    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([type, datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'), source_ip, destination_ip, source_port, destination_port, protocol, length, flags])


def multicast_sender(node_id, message, multicast_group=('224.0.0.1', 5000)):

    # Create Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely
    sock.settimeout(0.2)

    # Set the time-to-live for messages to 1 so they dont go past the local network segment
    ttl = struct.pack('b', 1)
    # Add to multicast group
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    local_ip = socket.gethostbyname(socket.gethostname())  # Get the local IP address

    try:
        log_communication('Multicast Sent', datetime.now().timestamp(), local_ip, multicast_group[0], str(sock.getsockname()[1]), str(multicast_group[1]), 'UDP', len(message), '0x010')
        # send data to the multicast group
        print(f'sending {message}')
        sent = sock.sendto(message.encode(), multicast_group)

        # look for responses from all recipients
        while True:
            print(f'waiting to receive')
            try:
                # receives messages
                data, server = sock.recvfrom(1024)
            except socket.timeout:
                print(f'timed out... no responses')
                break
            else:
                received_message = data.decode()
                if received_message == 'ack':
                    print(f'received acknowledgement from {server}')
                    log_communication('Multicast Ack Received', datetime.now().timestamp(), server[0], local_ip, str(server[1]), str(sock.getsockname()[1]), 'UDP', len(received_message), '0x011')
                    break
                else:
                    print(
                        f'received unexpected data from {server} : {data.decode()}')
    finally:
        print(f'closing socket')
        # close socket
        sock.close()


if __name__ == "__main__":
    node_id = sys.argv[1]
    message = ' '.join(sys.argv[2:]) or "Hello, multicast!"
    multicast_sender(node_id, message)
