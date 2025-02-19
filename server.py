# server.py
import socket

def start_server(host='127.0.0.1', port=7000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    
    while True:
        client_sock, addr = server.accept()
        try:
            # Receive message
            message = client_sock.recv(1024).decode()
            print(f"\nReceived message: {message}")
            
            # Process message and send response
            response = process_message(message)
            print(f"Sending response: {response}")
            client_sock.send(response.encode())
            
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_sock.close()

def process_message(message):
    # For any 4-character message, return the reverse
    return message[::-1]

if __name__ == "__main__":
    start_server()