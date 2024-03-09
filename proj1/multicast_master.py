import socket
import struct


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

        print(f'received {data.decode()} from {address}')

        print(f'sending acknowledgement to', address)
        sock.sendto(b'ack', address)


if __name__ == "__main__":
    multicast_receiver()

'''
def handle_node(connection, node_addr):
    try:
        print(f'connection from {node_addr}')

        # recieve data
        data = connection.recv(1024).decode('utf-8')
        if data:
            print(f'Message from {node_addr}: {data}')
    except Exception as e:
        print(
            f'Error handling connection from {node_addr}: {e}')
    finally:
        # close connection
        connection.close()


def master_thread(master_addr=('0.0.0.0', 5000)):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow reusing address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    print('starting up on %s port %s' % master_addr)
    sock.bind(master_addr)
    sock.listen(5)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, node_addr = sock.accept()

        # create new thread for each incoming connection
        node_thread = threading.Thread(
            target=handle_node, args=(connection, node_addr))
        node_thread.start()


if __name__ == "__main__":
    master_thread()
    '''
