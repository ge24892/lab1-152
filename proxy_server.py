# proxy_server.py
import socket
import json
import threading

class ProxyServer:
    def __init__(self, host='127.0.0.1', port=6000):
        self.host = host
        self.port = port
        self.blocklist = [
            '192.168.1.100',
            '10.0.0.50',
            '172.16.0.1'
            # Add more blocked IPs as needed
        ]
        
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Proxy server listening on {self.host}:{self.port}")
        
        while True:
            client_sock, addr = server.accept()
            client_handler = threading.Thread(
                target=self.handle_client,
                args=(client_sock,)
            )
            client_handler.start()
            
    def handle_client(self, client_socket):
        try:
            # Receive data from client
            data = client_socket.recv(1024).decode()
            print(f"\nReceived from client: {data}")
            
            # Parse JSON data
            request = json.loads(data)
            server_ip = request['server_ip']
            server_port = request['server_port']
            message = request['message']
            
            # Check if server IP is blocklisted
            if server_ip in self.blocklist:
                response = "Error: Server IP is blocklisted"
                print(f"Blocked request to {server_ip}")
                client_socket.send(response.encode())
            else:
                # Forward request to server
                response = self.forward_request(server_ip, server_port, message)
                print(f"Forwarding response to client: {response}")
                client_socket.send(response.encode())
                
        except Exception as e:
            print(f"Error handling client request: {e}")
        finally:
            client_socket.close()
            
    def forward_request(self, server_ip, server_port, message):
        # Create connection to target server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.connect((server_ip, server_port))
            server.send(message.encode())
            response = server.recv(1024).decode()
            return response
        except Exception as e:
            return f"Error forwarding request: {e}"
        finally:
            server.close()

if __name__ == "__main__":
    proxy = ProxyServer()
    proxy.start()