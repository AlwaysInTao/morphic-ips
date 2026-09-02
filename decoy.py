import socket

def serve_decoy(ip="127.0.0.1", port=8080):
    decoy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    decoy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    decoy.bind((ip, port))
    decoy.listen(5)
    
    # Fake header pool to confuse vulnerability scanners
    fake_header = (
        "HTTP/1.1 200 OK\r\n"
        "Server: Apache/2.2.3 (CentOS) Dav/2 PHP/5.1.6 Blueframe/v1.0.4\r\n"
        "X-Powered-By: VulnerableWebFramework/2.3.1\r\n"
        "Content-Type: text/html\r\n\r\n"
        "<html><body><h1>Admin Portal</h1><!-- TODO: Fix CVE-2021-41773 vulnerability --></body></html>"
    )

    while True:
        client, addr = decoy.accept()
        request = client.recv(1024).decode(errors='ignore')
        if "GET" in request or "POST" in request:
            # Send dynamic honeypot trail headers
            client.sendall(fake_header.encode())
        client.close()
