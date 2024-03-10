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
