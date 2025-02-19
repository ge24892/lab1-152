# client.py
import socket
import json
import sys

def send_request(message, proxy_host='127.0.0.1', proxy_port=6000):
    # Prepare the request data
    data = {
        "server_ip": "127.0.0.1",
        "server_port": 7000,
        "message": message
    }
    
    # Convert to JSON
    json_data = json.dumps(data)
    print(f"\nSending data: {json_data}")
    
    # Create socket and send request
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((proxy_host, proxy_port))
        client.send(json_data.encode())
        
        # Receive and print response
        response = client.recv(1024).decode()
        print(f"Received response: {response}")
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <4-char-message>")
        sys.exit(1)
        
    message = sys.argv[1]
    if len(message) != 4:
        print("Error: Message must be exactly 4 characters")
        sys.exit(1)
        
    send_request(message)