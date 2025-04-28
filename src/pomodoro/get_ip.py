import socket

class IPAddressFetcher:
    def __init__(self):
        self.ip = None

    def fetch_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # Attempt to connect to an external IP address
            s.connect(('10.254.254.254', 1))
            self.ip = s.getsockname()[0]
        except Exception:
            # Default to localhost if unable to fetch real IP
            self.ip = '127.0.0.1'
        finally:
            s.close()
        return self.ip

    def is_connected(self):
        return self.ip != '127.0.0.1'

        



# Example Usage:
if __name__ == "__main__":
    ip_fetcher = IPAddressFetcher()
    ip_address = ip_fetcher.fetch_ip()
    print(f"IP Address: {ip_address}")

    if ip_fetcher.is_connected():
        print("Connected to network, display IP on LCD")
     
    else:
        print("Not connected to network")
     
