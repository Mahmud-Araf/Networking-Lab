import socket
from threading import Thread

class Server:
    # Constructor to initialize the server socket using a port
    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        self.server.bind(('localhost', port))
        self.server.listen(5) #limiting client connections to 5
        print(f"Server started on port {port}")

    # Function to convert capital to small
    def small(self, sentence):
        return sentence.lower()

    # Function to check if a number is prime or not
    def is_prime(self, a):
        try:
            a = int(a)
        except:
            return "Not a number"
        if a < 2:
            return "No"
        for i in range(2, int(a**0.5) + 1):
            if a % i == 0:
                return "No"
        return "Yes"

    # Function to check if a string is palindrome or not
    def is_palindrome(self, a):
        return "Yes" if a == a[::-1] else "No"

    # Function to start the server
    def start(self):
        try:
            while True:
                client_socket, addr = self.server.accept()
                print(f"New client connected: {addr}")
                Thread(target=self.handle_client, args=(client_socket,)).start() #starting a new thread for each client 
        except KeyboardInterrupt:
            print("Server stopped by user")
        finally:
            self.close()

    # Function to close the server
    def close(self):
        self.server.close()

    # Function to handle each client
    def handle_client(self, client_socket):
        with client_socket:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    client_socket.send("Invalid input".encode())
                    continue
                str = data.decode()

                # Checking for the type of operation
                parts = str.split(" ")
                if len(parts) != 2:
                    print("capital to small converting", str)
                    rstr = self.small(str)
                elif parts[1]=="prime": # condition for checking if a number is prime or not
                    print("checking prime", parts[0])
                    rstr = self.is_prime(parts[0])
                elif parts[1]=="palindrome": # condition for checking if a string is palindrome or not
                    print("checking palindrome", parts[0])
                    rstr = self.is_palindrome(parts[0])
                else:                  # condition for lowercasing a string
                    print("capital to small converting", str)
                    rstr = self.small(str)
                
                client_socket.sendall(rstr.encode())

if __name__ == "__main__":
    port = 8080  
    server = Server(port)
    server.start()
