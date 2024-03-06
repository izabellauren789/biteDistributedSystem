import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_addr = ('localhost', 10000)
print('starting up on %s port %s' % server_addr, file=sys.stderr)
sock.bind(server_addr)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection', file=sys.stderr)
    connection, client_addr = sock.accept()

    # Message read from connection
    print('connection from', client_addr, file=sys.stderr)

    # Recieve data
    data = connection.recv(1024).decode('utf-8')
    print('message from node: ', data, file=sys.stderr)

    # Close up the connection
    connection.close()
