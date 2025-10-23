import socket
import threading
import re

def augustinerBraeuMuenchen(conn, addr):
    print(f"Handling connection from {addr}")
    try:
        while True:

            data = conn.recv(1024) 

            if not data:
                print(f"Connection from {addr} closed by client.")
                break

            if data:
                httpParse(data, conn)
                
    except ConnectionResetError:
        print(f"Connection from {addr} reset.")
    except Exception as e:
        print(f"Error on connection {addr}: {e}")
    finally:
        print(f"Closed connection for {addr}")
        conn.close()

def httpParse(httpRequest, socketHandle):
    httpRequestLines = [line.split(" ") for line in httpRequest.decode('ascii').split("\r\n")]

    wordIndex = 0


    if(httpRequestLines[0][0] != "GET"):
        return
        
    if not (re.match(r"^/[A-Za-z0-9]+.[A-Za-z0-9]+", httpRequestLines[0][1])):
        return
    else:
        requestedPath = re.findall(r"^/[A-Za-z0-9]+.[A-Za-z0-9]+", httpRequestLines[0][1])[0]

        finalRequestedPath = "/home/n0ne/Documents/DontDeleteImportantAllDataObsidian/studium/sem3/WEB/writingOwnWebServer/python/serve" + requestedPath
        with open(finalRequestedPath, "r") as file:
            fileContent = file.read()
            conn.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n".encode())
            conn.sendall(fileContent.encode())
 
    if(httpRequestLines[0][2] != "HTTP/1.1"):
        return
 
    if(httpRequestLines[1][0] != "Host:"):
        return
    
        #    if(httpRequestLines[1][1] != ""):
        #return

 
# https://docs.python.org/3/library/socket.html is a pretty good ressource, especially the start and "funtions" sections and the Examples

meineSocke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket with the default settings(AF_INET specifies how the IP/Port or Host/Port should be input specified later)

meineSocke.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

meineSocke.bind(("", 6789))        # ("", 6789) is a tupel for interface and port and giving "" to interface means use all interfaces
meineSocke.listen(1)               # Now we have a socket listening on all interfaces on port 6789 for incoming connection


while True:

    conn, addr = meineSocke.accept()          # When a connection is coming in, accept it and then we have the object conn via which we can send and receive data for that connection

    print("Connection by", addr)   # This works! Test by running the script and the doing a `nc` or watching netstat -tulpn and you will see the socket show up

    worldWarIII = threading.Thread(target=augustinerBraeuMuenchen, args=(conn, addr))
    worldWarIII.start() 

