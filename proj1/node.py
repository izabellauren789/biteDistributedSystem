import socket
import sys

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to socket to the port where the server is listening
server_addr = ('localhost', 10000)
print('connecting to %s port %s' % server_addr, file=sys.stderr)
sock.connect(server_addr)

# After connection established, data sent
try:
    # Send data
    message = "Hello Master!"
    print('sending %s' % message, file=sys.stderr)
    sock.sendall(message.encode('utf-8'))

finally:
    print('closing socket', file=sys.stderr)
    sock.close()
