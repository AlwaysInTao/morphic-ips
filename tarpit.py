import socket
import time
import sys

def start_tarpit(ip="127.0.0.1", port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((ip, port))
        server.listen(100)
        print(f"[*] Morphic Tarpit listening on {ip}:{port}...")
    except Exception as e:
        print(f"[-] Tarpit bind failed: {e}")
        sys.exit(1)

    while True:
        try:
            client_sock, addr = server.accept()
            print(f"[!] Attacker trapped from connection origin: {addr[0]}:{addr[1]}")
            # Keep client engaged indefinitely 
            client_sock.settimeout(None)
            while True:
                # Slowly feed 1 byte of garbage data every 5 seconds
                client_sock.send(b"\x00")
                time.sleep(5.0)
        except (socket.error, ConnectionResetError):
            print(f"[*] Attacker resource exhausted. Target dropped connection.")
            client_sock.close()
        except KeyboardInterrupt:
            break
