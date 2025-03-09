import socket

def scan_ports(host, start_port=1, end_port=1024):
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if not s.connect_ex((host, port)):
                print(f"Port {port} is open")

if __name__ == "__main__":
    target_host = "127.0.0.1"
    scan_ports(target_host)