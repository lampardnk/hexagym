import socket
import subprocess
import sys
import os

def get_ip():
    """Get the local IP address of this machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def main():
    ip = get_ip()
    
    print("\n===== HexaGym Server =====")
    print("\nNetwork Information:")
    print(f"Local IP: {ip}")
    print(f"Access URL: http://{ip}:5000")
    print("\nShare the above URL with others on the same network to access HexaGym")
    print("\nStarting server...")
    print("(Press CTRL+C to stop the server)")
    print("\n===========================\n")
    
    # Start the Flask application
    if sys.platform.startswith('win'):
        os.system("python app.py")
    else:
        os.system("python3 app.py")

if __name__ == "__main__":
    main() 