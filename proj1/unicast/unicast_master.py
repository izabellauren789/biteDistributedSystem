
# POSSIBLE CODE FOR UNICAST PLZ DOUBLECHECK AND DEBUG
import socket
import sys
import threading
import time

# Global list to keep track of connections (for simplicity)
node_connections = []


def handle_node(connection, node_addr):
    print(f'Connection from {node_addr}')
    # Here you might handle initial handshaking or authentication
    node_connections.append((connection, node_addr))


def send_unicast_messages():
    message = "Hello Node, this is a unicast message from Master!"
    for connection, node_addr in node_connections:
        try:
            print(f'Sending message to {node_addr}')
            connection.sendall(message.encode('utf-8'))
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

        # Separate thread to accept connections for a limited time
        def accept_connections():
            while True:
                connection, node_addr = sock.accept()
                threading.Thread(target=handle_node, args=(
                    connection, node_addr)).start()

        accept_thread = threading.Thread(target=accept_connections)
        accept_thread.start()

        # Wait for a certain time to collect connections, then send messages
        print(f'Waiting for nodes to connect for {wait_for_nodes} seconds...')
        time.sleep(wait_for_nodes)

        # Stop accepting connections
        print('Stop accepting new connections. Sending messages to connected nodes.')
        # Attempt to stop the thread (not reliable)
        accept_thread.join(timeout=1)
        sock.close()  # Close the listening socket

        send_unicast_messages()


if __name__ == "__main__":
    master_thread()
