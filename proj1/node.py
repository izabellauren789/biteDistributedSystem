import socket
import sys
import threading


def node_thread(id, master_addr=('localhost', 5000)):
    # Create TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to the server
    try:
        print(f'node {id} connecting to {master_addr}', file=sys.stderr)
        sock.connect(master_addr)
    except socket.error as e:
        print(f'node {id} failed to connect to {master_addr}: {e}',
              file=sys.stderr)
        return

    # After connection established, data sent
    try:
        # Send data
        message = f"Hello Master from node {id}!"
        print(f'node {id}: sending {message}', file=sys.stderr)
        sock.sendall(message.encode('utf-8'))
    except socket.error as e:
        print(f'node {id} failed to send data: {e}', file=sys.stderr)
    finally:
        print(f'node {id} closing socket', file=sys.stderr)
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
