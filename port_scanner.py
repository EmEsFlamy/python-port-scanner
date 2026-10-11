import socket
import time
import threading

print_lock = threading.Lock()


def get_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"


def scan_port(host, port, open_ports_list):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            service = get_service(port)
            with print_lock:
                print(f"Port {port} ({service}) - OPEN")
            open_ports_list.append(port)
    except socket.error as e:
        print(f"Error on port {port}: {e}")
    return False


def scan_range(host, start_port, end_port):
    print(f"\nScanning {host} ports {start_port}-{end_port}")
    print("-" * 40)

    start_time = time.time()

    threads = []
    open_ports_list = []

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(host, port, open_ports_list))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    elapsed = round(time.time() - start_time, 2)
    print("-" * 40)
    print(f"Open ports found: {len(open_ports_list)}")
    print(f"Scan completed in {elapsed} seconds\n")


# Test
scan_range("127.0.0.1", 1, 1024)
