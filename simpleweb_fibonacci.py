# -*- coding: utf-8 -*-
import socket

# server host IP, PORT
HOST, PORT = '192.168.9.181', 8888

# socket, bind, listen 
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT

# main loop
while True:
    # accept
    client_connection, client_address = listen_socket.accept()

    # receive request
    request = client_connection.recv(1024)
    print request

    # here parse request
    # parse ...

    # make response, simple fibonacci numbers
    http_response = """\
    HTTP/1.1 200 OK

    0 1 1 2 3 5 8 13 ...
    """

    # send response
    client_connection.sendall(http_response)

    # close connection
    client_connection.close()

