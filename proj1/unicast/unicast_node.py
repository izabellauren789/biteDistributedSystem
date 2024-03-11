# POSSIBLE CODE FOR UNICAST PLZ DOUBLECHECK AND DEBUG
import socket
import sys


def main(id, master_addr=('master-server', 5000)):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            print(f'Node {id} connecting to {master_addr}')
            sock.connect(master_addr)
            # Wait to receive a message from the master
            data = sock.recv(1024)
            print(f'Node {id} received: {data.decode("utf-8")}')
        except Exception as e:
            print(f'Node {id} failed to connect or receive from {master_addr}: {e}', file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python node_script.py <node_id>")
        sys.exit(1)
    node_id = sys.argv[1]
    main(node_id)
