# udp_client.py
import socket
import time
import json
import sys
from datetime import datetime

def generate_payload(size_mb):
    # Generate random payload of specified size
    size_bytes = size_mb * 1024 * 1024
    return b'X' * size_bytes

def send_data(payload_size_mb):
    # Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    
    try:
        # Generate payload
        payload = generate_payload(payload_size_mb)
        chunk_size = 65507  # Max UDP packet size
        
        print(f"Client IP: {socket.gethostbyname(socket.gethostname())}")
        print(f"Sending {payload_size_mb} MB of data to server")
        send_timestamp = datetime.now()
        print(f"Started sending data at: {send_timestamp}")

        # Send data in chunks
        for i in range(0, len(payload), chunk_size):
            chunk = payload[i:i + chunk_size]
            if i + chunk_size >= len(payload):
                # Add end marker to last chunk
                chunk = chunk + b"END_OF_DATA"
            client_socket.sendto(chunk, server_address)

        # Receive throughput from server
        data, _ = client_socket.recvfrom(4096)
        response = json.loads(data.decode())
        
        print("\nTransfer Summary:")
        print(f"Data sent at: {send_timestamp}")
        print(f"Data received at: {response['receive_timestamp']}")
        print(f"Bytes sent: {len(payload)}")
        print(f"Bytes received: {response['bytes_received']}")
        print(f"Throughput: {response['throughput']:.2f} KB/s")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python udp_client.py <size_in_MB>")
        sys.exit(1)
    
    try:
        size_mb = int(sys.argv[1])
        if not 25 <= size_mb <= 200:
            raise ValueError("Size must be between 25 and 200 MB")
        send_data(size_mb)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)