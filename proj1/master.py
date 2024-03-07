import socket
import sys
import threading


def handle_node(connection, node_addr):
    try:
        print(f'connection from {node_addr}', file=sys.stderr)

        # recieve data
        data = connection.recv(1024).decode('utf-8')
        if data:
            print(f'Message from {node_addr}: {data}', file=sys.stderr)
    except Exception as e:
        print(
            f'Error handling connection from {node_addr}: {e}', file=sys.stderr)
    finally:
        # close connection
        connection.close()


def master_thread(master_addr=('0.0.0.0', 5000)):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow reusing address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    print('starting up on %s port %s' % master_addr, file=sys.stderr)
    sock.bind(master_addr)
    sock.listen(5)

    while True:
        # Wait for a connection
        print('waiting for a connection', file=sys.stderr)
        connection, node_addr = sock.accept()

        # create new thread for each incoming connection
        node_thread = threading.Thread(
            target=handle_node, args=(connection, node_addr))
        node_thread.start()


if __name__ == "__main__":
    master_thread()
