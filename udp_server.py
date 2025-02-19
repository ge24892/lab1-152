# udp_server.py
import socket
import time
import json
from datetime import datetime

def start_server():
    # Create UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    
    print(f"Server started on {server_address}")
    print(f"Server IP: {socket.gethostbyname(socket.gethostname())}")

    while True:
        try:
            print("\nWaiting to receive data...")
            total_bytes_received = 0
            received_data = b''
            start_time = None

            while True:
                # Receive data in chunks
                data, client_address = server_socket.recvfrom(65507)  # Max UDP packet size
                
                if start_time is None:
                    start_time = time.time()
                    print(f"Started receiving data at: {datetime.now()}")

                if data.endswith(b"END_OF_DATA"):
                    received_data += data[:-11]  # Remove the END_OF_DATA marker
                    total_bytes_received += len(data) - 11
                    break
                
                received_data += data
                total_bytes_received += len(data)

            end_time = time.time()
            receive_timestamp = datetime.now()
            
            # Calculate throughput
            duration = end_time - start_time
            throughput = (total_bytes_received / 1024) / duration  # KB/s

            print(f"Received {total_bytes_received} bytes from {client_address}")
            print(f"Data received at: {receive_timestamp}")
            print(f"Throughput: {throughput:.2f} KB/s")

            # Send throughput back to client
            response = {
                "throughput": throughput,
                "bytes_received": total_bytes_received,
                "receive_timestamp": str(receive_timestamp)
            }
            server_socket.sendto(json.dumps(response).encode(), client_address)

        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    start_server()