import socket
import time

def get_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            service = get_service(port)
            print(f"Port {port} ({service}) - OPEN")
            return True
        return False
    except socket.error as e:
        print(f"Error on port {port}: {e}")
        return False

def scan_range(host, start_port, end_port):
    print(f"\nScanning {host} ports {start_port}-{end_port}")
    print("-" * 40)
    
    start_time = time.time()
    open_ports = 0
    
    for port in range(start_port, end_port + 1):
        if scan_port(host, port):
            open_ports += 1
    
    elapsed = round(time.time() - start_time, 2)
    print("-" * 40)
    print(f"Open ports found: {open_ports}")
    print(f"Scan completed in {elapsed} seconds\n")

# Test
scan_range("127.0.0.1", 1, 1024)