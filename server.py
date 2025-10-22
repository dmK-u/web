import socket

# https://docs.python.org/3/library/socket.html is a pretty good ressource, especially the start and "funtions" sections and the Examples

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket with the default settings(AF_INET specifies how the IP/Port or Host/Port should be input specified later)

mySocket.bind(("", 6789))        # ("", 6789) is a tupel for interface and port and giving "" to interface means use all interfaces
mySocket.listen(1)               # Now we have a socket listening on all interfaces on port 6789 for incoming connection

conn, addr = mySocket.accept()          # When a connection is coming in, accept it and then we have the object conn via which we can send and receive data for that connection

with conn:
    print("Connection by", addr)   # This works! Test by running the script and the doing a `nc` or watching netstat -tulpn and you will see the socket show up
                                   # sudo fuser -k 6789/tcp for debugging
    while True:
        data = conn.recv(1024)         # Read data from socket. Max block size in which data is read: 1024bytes. If you `nc` in and then write something and press enter it will show up here
        if data:                       # Check if data is actually something new and interesting we sent to the socket or just null(which is falsy) because it is in a while loop constantly polling
            print(data)
            # Send Response to the client: .encode will encode the f-string into a byte-type object(b'any') because that is what sendall() expects
            conn.sendall(f"<echo> Following data arrived at server and echoed back: {data}\n".encode())


mySocket.close()
