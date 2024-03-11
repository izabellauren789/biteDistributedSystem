import socket
import sys
import csv
from datetime import datetime

def log_communication(type, time, source_ip, destination_ip, source_port, destination_port, protocol, length, flags):
        log_file = '/app/logs/network_communications.csv'

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


def main(id, master_addr=('master-server', 5000)):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            print(f'Node {id} connecting to {master_addr}')
            sock.connect(master_addr)
            local_ip = socket.gethostbyname(socket.gethostname())  # Local IP address
            local_port = sock.getsockname()[1]  # Local port used for the connection
            # Log the connection attempt
            log_communication('Unicast Connection Attempt', datetime.now().timestamp(), local_ip, master_addr[0], str(local_port), str(master_addr[1]), 'TCP', 'N/A', 'N/A')
            # Wait to receive a message from the master
            data = sock.recv(1024)
            print(f'Node {id} received: {data.decode("utf-8")}')
            # Log the message reception
            log_communication('Unicast Message Received', datetime.now().timestamp(), master_addr[0], local_ip, str(master_addr[1]), str(local_port), 'TCP', len(data), 'N/A')
        except Exception as e:
            print(f'Node {id} failed to connect or receive from {master_addr}: {e}', file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python node_script.py <node_id>")
        sys.exit(1)
    node_id = sys.argv[1]
    main(node_id)
