import socket
from threading import Thread

class Client:
    # Constructor to initialize the client socket using  a server ip and port
    def __init__(self, server_ip, server_port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_port))

    # Function to send 3 different type of messages to the server
    def send_message(self):
        while True:
            message_to_send = input()
            self.client_socket.sendall(message_to_send.encode())

   # Function to listen for messages from the server
    def listen_for_message(self):
        while True:
            data = self.client_socket.recv(1024) #receiving message size set to 1024 bytes.
            if not data:
                break
            print(data.decode())

    # staring function to start the server both for sending and receiving messages
    def start(self):
        Thread(target=self.listen_for_message).start()
        self.send_message()

    # Function to close the client
    def close(self):
        self.client_socket.close()

if __name__ == "__main__":
    server_ip = "localhost"
    server_port = 8080
    client = Client(server_ip, server_port)
    print("Valid operations:\n 1.String (to lowercase the string)\n 2.Integer Operation(to check prime or palindrome.Operation can be either 'prime' or 'palindrome')\n")
    client.start()
    client.close()