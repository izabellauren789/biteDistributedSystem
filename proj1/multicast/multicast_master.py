# Done by Izabel Smid - 027494569
# inspired code from https://pymotw.com/2/socket/multicast.html
import socket
import struct
import csv
from datetime import datetime

def log_communication(type, time, source_ip, destination_ip, source_port, destination_port, protocol, length, flags):
        log_file = '/app/logs/multicast_communications.csv'

        log_headers = ['Type', ' Time(s)', ' Source_Ip', ' Destination_Ip', ' Source_Port', ' Destination_Port', ' Protocol', ' Length (bytes)', ' Flags (hex)']
    
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


def multicast_receiver(master_addr=('224.0.0.1', 5000)):

    # create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # allow multiple sockets to use the same port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind to server address
    sock.bind(('', master_addr[1]))  # bind all interfaces on the given port

    # tell the operating system to add the socket to the multicast on all interfaces
    group = socket.inet_aton(master_addr[0])
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(
        f'Listening for multicast messages on {master_addr[0]}:{master_addr[1]}')

    # loop for receiving and responding messages
    while True:
        print(f'waiting to receive message')
        data, address = sock.recvfrom(1024)

        # calling log function after receiving a multicast message
        log_communication(
            'Multicast', 
            datetime.now().timestamp(), 
            address[0], 
            master_addr[0], 
            str(address[1]), 
            str(master_addr[1]), 
            'UDP', 
            len(data), 
            '0x011'
        )

        print(f'received {data.decode()} from {address}')

        print(f'sending acknowledgement to', address)
        sock.sendto(b'ack', address)



if __name__ == "__main__":
    multicast_receiver()
