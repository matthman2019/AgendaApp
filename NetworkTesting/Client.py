import socket

with socket.create_connection(("255.255.255.255", 25313)) as s:
    s.send("We just broadcasted this!")