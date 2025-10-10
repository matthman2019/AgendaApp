import socket
with socket.create_server(("", 25313)) as s:
    while True:
        connection, address = s.accept()
        print(connection.recv(1024).decode)
        connection.close()