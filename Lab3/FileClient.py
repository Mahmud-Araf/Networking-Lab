import socket
import os

# Set the server's IP address and port
server_ip = 'localhost'
server_port = 12347

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))

while True:
    # Receive the operation prompt from the server
    operation_prompt = "Please select a operation.\n1.list\n2.upload\n3.download"
    print(operation_prompt)

    # Send the operation to the server
    operation = input()
    client_socket.send(operation.encode())

    if operation == 'list':
        # Receive and print the list of files
        files = client_socket.recv(1024).decode()
        print(files)
    elif operation == 'upload':
        # Send the filename to the server
        filename = input('Enter the filename: ')
        client_socket.send(filename.encode())

        response = client_socket.recv(1024).decode()
        print(response)

        if response == 'OK':
            # Send the file size to the server
          if os.path.exists(os.getcwd()+'/'+filename):
            file_size = os.path.getsize(filename)
            client_socket.send(str(file_size).encode())
            # Send the file to the server
            with open(filename, 'rb') as file:
                while True:
                    bytes_to_send = file.read(1024)
                    if not bytes_to_send:
                        break
                    client_socket.send(bytes_to_send)
            print(client_socket.recv(1024).decode())
          else:
            print('File not found')
            client_socket.send('File not found'.encode())
    elif operation == 'download':
        # Send the filename to the server
        filename = input('Enter the filename: ')
        client_socket.send(filename.encode())

        response = client_socket.recv(1024).decode()
        print(response)

        if response == 'OK':
            # Receive the file from the server
        
            file_size = int(client_socket.recv(1024).decode())  

            with open(filename, 'wb') as file:
                received_size = 0
                while received_size<file_size:
                    bytes_received = client_socket.recv(1024)

                    received_size += len(bytes_received)
                    
                    file.write(bytes_received)
            print('File downloaded successfully')
    else:
        msg= client_socket.recv(1024).decode()
        print(msg)

# Close the socket
client_socket.close()