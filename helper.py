import socket

def get_internal_ip():
    # Create a dummy socket to connect to an external server
    # This doesn't actually connect but helps determine the local IP address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # We use a dummy IP and port
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]  # This returns the local IP address
        except Exception:
            return "Unable to get IP"