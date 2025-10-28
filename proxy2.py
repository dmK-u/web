import socket
import threading

# proxy request curl --proxy http://localhost:80 http://example.com

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
        print(f"Error sending error response: {e}")

def proxy_handler(client_conn, full_request_bytes):
    
    try:
        header_part, body_bytes = full_request_bytes.split(b"\r\n\r\n", 1)
        header_str = header_part.decode('latin-1')
        lines = header_str.split("\r\n")
        
        request_line = lines[0]
        method, full_path, version = request_line.split(" ", 2)
        
        headers = {}
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key.lower()] = value

    except Exception as e:
        print(f"Failed to parse request: {e}")
        sendHttpResponse(client_conn, 400, "Bad Request", b"<h1>400 Bad Request</h1>")
        return

    print("\n--- NEW REQUEST ---")
    print(f"Method: {method}")
    print(f"Full Path: {full_path}")
    print("Headers:")
    for key, value in headers.items():
        print(f"  {key}: {value}")

    target_host = ""
    target_port = 80
    target_path = ""

    if full_path.startswith("http://"):
        path_remainder = full_path[7:]
        if "/" not in path_remainder:
            host_port = path_remainder
            target_path = "/"
        else:
            host_port, target_path = path_remainder.split("/", 1)
            target_path = "/" + target_path
            
        if ":" in host_port:
            target_host, port_str = host_port.split(":", 1)
            try:
                target_port = int(port_str)
            except ValueError:
                sendHttpResponse(client_conn, 400, "Bad Request", b"<h1>400 Bad Request: Invalid Port</h1>")
                return
        else:
            target_host = host_port
            target_port = 80
            
    else:
        if "host" not in headers:
            sendHttpResponse(client_conn, 400, "Bad Request", b"<h1>400 Bad Request: No Host Header</h1>")
            return
            
        host_header = headers["host"]
        target_path = full_path
        
        if ":" in host_header:
            target_host, port_str = host_header.split(":", 1)
            try:
                target_port = int(port_str)
            except ValueError:
                sendHttpResponse(client_conn, 400, "Bad Request", b"<h1>400 Bad Request: Invalid Port</h1>")
                return
        else:
            target_host = host_header
            target_port = 80

    if method == "GET":
        if "?" in target_path:
            query_string = target_path.split("?", 1)[-1]
            print(f"GET Parameters: {query_string}")
            
    elif method == "POST":
        print("POST Body:\n", body_bytes.decode('latin-1', errors='ignore'))

    target_sock = None
    try:
        target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_ip = socket.gethostbyname(target_host)
        target_sock.connect((target_ip, target_port))
        
        forward_request_line = f"{method} {target_path} {version}\r\n"
        
        forward_header_str = forward_request_line
        for key, value in headers.items():
            if key not in ["proxy-connection", "connection", "host"]:
                forward_header_str += f"{key.capitalize()}: {value}\r\n"
        
        forward_header_str += f"Host: {target_host}\r\n"
        forward_header_str += "Connection: close\r\n"
        forward_header_str += "\r\n"
        
        target_sock.sendall(forward_header_str.encode('latin-1'))
        
        if body_bytes:
            target_sock.sendall(body_bytes)
            
    except Exception as e:
        print(f"Error connecting/sending to target: {e}")
        sendHttpResponse(client_conn, 502, "Bad Gateway", b"<h1>502 Bad Gateway</h1>")
        if target_sock:
            target_sock.close()
        return

    try:
        while True:
            response_chunk = target_sock.recv(4096)
            if not response_chunk:
                break
            client_conn.sendall(response_chunk)
            
    except Exception as e:
        print(f"Error relaying response: {e}")
    finally:
        if target_sock:
            target_sock.close()

def handle_connection(conn, addr):
    print(f"Handling connection from {addr}")
    try:
        headers_raw = b""
        while b"\r\n\r\n" not in headers_raw:
            chunk = conn.recv(1024)
            if not chunk:
                break
            headers_raw += chunk
        
        if not headers_raw:
            print(f"Connection from {addr} closed by client.")
            return

        header_part, body_fragment = headers_raw.split(b"\r\n\r\n", 1)
        
        content_length = 0
        try:
            header_str = header_part.decode('latin-1')
            lines = header_str.split("\r\n")
            for line in lines[1:]:
                if line.lower().startswith("content-length:"):
                    content_length = int(line.split(":", 1)[1].strip())
                    break
        except Exception:
            pass

        body_bytes = body_fragment
        while len(body_bytes) < content_length:
            chunk = conn.recv(4096)
            if not chunk:
                break
            body_bytes += chunk
        
        full_request_bytes = header_part + b"\r\n\r\n" + body_bytes
        
        proxy_handler(conn, full_request_bytes)
        
    except ConnectionResetError:
        print(f"Connection from {addr} reset.")
    except Exception as e:
        print(f"Error on connection {addr}: {e}")
    finally:
        print(f"Closed connection for {addr}")
        conn.close()

port = 80
meineSocke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
meineSocke.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
meineSocke.bind(("", port))
meineSocke.listen(5)

print(f"\nProxy Server is running on port: {port}")

while True:
    conn, addr = meineSocke.accept()
    print("Connection by", addr)
    proxy_thread = threading.Thread(target=handle_connection, args=(conn, addr))
    proxy_thread.start()