
import socket
import sys
import threading
import time
import csv
from datetime import datetime

def log_communication(type, time, source_ip, destination_ip, source_port, destination_port, protocol, length, flags):
    log_file = '/app/logs/network_communications.csv'
    log_headers = ['Type', 'Time(s)', 'Source_Ip', 'Destination_Ip', 'Source_Port', 'Destination_Port', 'Protocol', 'Length (bytes)', 'Flags (hex)']

    try:
        with open(log_file, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(log_headers)
    except FileExistsError:
        pass

    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([type, datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'), source_ip, destination_ip, source_port, destination_port, protocol, length, flags])

node_connections = []

def handle_node(connection, node_addr):
    connection.settimeout(10)  # Set timeout for receiving
    print(f'Connection from {node_addr}')
    log_communication('Unicast Connection', datetime.now().timestamp(), '0.0.0.0', node_addr[0], '5000', str(node_addr[1]), 'TCP', 'N/A', 'N/A')
    node_connections.append((connection, node_addr))

def send_unicast_messages():
    message = "Hello Node, this is a unicast message from Master!"
    for connection, node_addr in node_connections:
        try:
            print(f'Sending message to {node_addr}')
            connection.sendall(message.encode('utf-8'))
            log_communication('Unicast Sent', datetime.now().timestamp(), '0.0.0.0', node_addr[0], '5000', str(node_addr[1]), 'TCP', len(message), 'N/A')
        except Exception as e:
            print(f'Error sending message to {node_addr}: {e}')
        finally:
            connection.close()

def master_thread(master_addr=('0.0.0.0', 5000), wait_for_nodes=10):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(master_addr)
        sock.listen()
        print(f'Master starting up on {master_addr}')
        
        def accept_connections():
            while accepting:
                try:
                    connection, node_addr = sock.accept()
                    threading.Thread(target=handle_node, args=(connection, node_addr)).start()
                except socket.timeout:
                    continue

        sock.settimeout(1)  # Set timeout for accept() to prevent hanging
        accepting = True
        accept_thread = threading.Thread(target=accept_connections)
        accept_thread.start()

        print(f'Waiting for nodes to connect for {wait_for_nodes} seconds...')
        time.sleep(wait_for_nodes)

        accepting = False
        accept_thread.join()
        print('Stop accepting new connections. Sending messages to connected nodes.')

        send_unicast_messages()

if __name__ == "__main__":
    master_thread()
