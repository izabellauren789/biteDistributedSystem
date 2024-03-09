import socket
import sys
import struct


def multicast_sender(node_id, message, multicast_group=('224.0.0.1', 5000)):

    # Create Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely
    sock.settimeout(0.2)

    # Set the time-to-live for messages to 1 so they dont go past the local network segment
    ttl = struct.pack('b', 1)
    # Add to multicast group
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
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
                if data.decode() == 'ack':
                    print(f'received acknowledgement from {server}')
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


'''
def node_thread(id, master_addr=('master-server', 5000)):
    # Create TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to the server
    try:
        print(f'node {id} connecting to {master_addr}')
        sock.connect(master_addr)
    except socket.error as e:
        print(f'node {id} failed to connect to {master_addr}: {e}',
              file=sys.stderr)
        return

    # After connection established, data sent
    try:
        # Send data
        message = f"Hello Master from node {id}!"
        print(f'node {id}: sending {message}')
        sock.sendall(message.encode('utf-8'))
    except socket.error as e:
        print(f'node {id} failed to send data: {e}')
    finally:
        print(f'node {id} closing socket')
        sock.close()


def main():
    # declare number of nodes
    numThreads = 4

    # list to store theads
    threads = []

    # create and start node threads
    for i in range(numThreads):
        thread = threading.Thread(target=node_thread, args=(i+1,))
        threads.append(thread)
        thread.start()

    # wait for threads to start
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
    '''
