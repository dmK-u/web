import socket
import threading
import os
import mimetypes

root = "/home/dmk/github/web/serve"
abs_root = os.path.abspath(root)

def sendHttpResponse(conn, statusCode, statusText, body=b"", contentType="text/html"):
    try:
        body_bytes = body if isinstance(body, bytes) else body.encode('latin-1')
        
        header = f"HTTP/1.1 {statusCode} {statusText}\r\n"
        header += f"Content-Type: {contentType}\r\n"
        header += f"Content-Length: {len(body_bytes)}\r\n"
        header += "Connection: close\r\n\r\n"
        
        conn.sendall(header.encode('latin-1'))
        conn.sendall(body_bytes)
    except Exception as e:
        print(f"Error sending response: {e}")

def httpParse(httpRequest, conn):
    try:
        request_str = httpRequest.decode('latin-1')
        lines = request_str.split("\r\n")

        if not lines:
            raise ValueError("Empty request")

        first_line_parts = lines[0].split(" ")
        if len(first_line_parts) != 3:
            raise ValueError("Malformed request line")
            
        method, path, version = first_line_parts
        
    except (UnicodeDecodeError, IndexError, ValueError) as e:
        sendHttpResponse(conn, 400, "Bad Request", b"<h1>400 Bad Request</h1>")
        print(f"Sent 400 Bad Request due to: {e}")
        return

    if method != "GET":
        sendHttpResponse(conn, 400, "Bad Request", b"<h1>400 Bad Request: Only GET supported</h1>")
        return

    if path == "/":
        path = "/index.html"

    relative_path = path.lstrip('/')
    
    real_root = os.path.realpath(abs_root)
    real_target = os.path.realpath(os.path.join(abs_root, relative_path))

    print(f"DEBUG: Checking path: {real_target}")
    print(f"DEBUG: Against root:  {abs_root}")
    
    # curl --path-as-is localhost/../server.py
    
    if not real_target.startswith(real_root + os.sep):
        sendHttpResponse(conn, 403, "Forbidden", b"<h1>403 Forbidden</h1>")
        print(f"Forbidden path traversal attempt: {path}")
        return
    
    if not real_target.startswith(abs_root):
        sendHttpResponse(conn, 403, "Forbidden", b"<h1>403 Forbidden</h1>")
        print(f"Forbidden path traversal attempt: {path}")
        return
    
    if os.path.isdir(real_target):
        sendHttpResponse(conn, 403, "Forbidden", b"<h1>403 Forbidden: Is a directory</h1>")
        print(f"Forbidden directory access attempt: {path}")
        return

    if not os.path.isfile(real_target):
        sendHttpResponse(conn, 404, "Not Found", b"<h1>404 Not Found</h1>")
        print(f"File not found: {real_target}")
        return

    if not os.access(real_target, os.R_OK):
        sendHttpResponse(conn, 403, "Forbidden", b"<h1>403 Forbidden: Permission Denied</h1>")
        print(f"Permission denied: {real_target}")
        return

    try:
        with open(real_target, "rb") as file:
            fileContent = file.read()
            
        mime_type, _ = mimetypes.guess_type(real_target)
        if mime_type is None:
            mime_type = "application/octet-stream"
            
        sendHttpResponse(conn, 200, "OK", fileContent, mime_type)

    except IOError as e:
        sendHttpResponse(conn, 500, "Internal Server Error", b"<h1>500 Internal Server Error</h1>")
        print(f"Internal error reading file: {e}")

def augustinerBraeuMuenchen(conn, addr):
    print(f"Handling connection from {addr}")
    try:
        data = conn.recv(1024) 

        if not data:
            print(f"Connection from {addr} closed by client.")
        else:
            httpParse(data, conn)
            
    except ConnectionResetError:
        print(f"Connection from {addr} reset.")
    except Exception as e:
        print(f"Error on connection {addr}: {e}")
    finally:
        print(f"Closed connection for {addr}")
        conn.close()


###

meineSocke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
meineSocke.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
meineSocke.bind(("", 80))
meineSocke.listen(1)

while True:
    conn, addr = meineSocke.accept()
    print("Connection by", addr)
    worldWarIII = threading.Thread(target=augustinerBraeuMuenchen, args=(conn, addr))
    worldWarIII.start()