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
            end_marker_received = False

            while not end_marker_received:
                # Receive data in chunks
                data, client_address = server_socket.recvfrom(65507)  # Max UDP packet size
                
                if start_time is None:
                    start_time = time.time()
                    print(f"Started receiving data at: {datetime.now()}")

                if data == b"END_OF_DATA":
                    print("Received END_OF_DATA marker")
                    end_marker_received = True
                    break
                
                received_data += data
                total_bytes_received += len(data)
                
                # Periodically print progress for large transfers
                if total_bytes_received % (10 * 1024 * 1024) < 65507:  # roughly every 10MB
                    mb_received = total_bytes_received / (1024 * 1024)
                    print(f"Progress: {mb_received:.2f} MB received")

            if not end_marker_received:
                print("Warning: END_OF_DATA marker not received, data may be incomplete")
                continue

            end_time = time.time()
            receive_timestamp = datetime.now()
            
            # Calculate throughput
            duration = end_time - start_time
            throughput = (total_bytes_received / 1024) / duration  # KB/s
            mb_received = total_bytes_received / (1024 * 1024)

            print(f"Received {total_bytes_received} bytes ({mb_received:.2f} MB) from {client_address}")
            print(f"Data received at: {receive_timestamp}")
            print(f"Transfer duration: {duration:.2f} seconds")
            print(f"Throughput: {throughput:.2f} KB/s")

            # Send throughput back to client
            response = {
                "throughput": throughput,
                "bytes_received": total_bytes_received,
                "receive_timestamp": str(receive_timestamp)
            }
            server_socket.sendto(json.dumps(response).encode(), client_address)
            print("Sent response to client")

        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    start_server()