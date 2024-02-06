import socket
import threading
import os
import time

# Set the server's IP address and port
server_ip = 'localhost'
server_port = 12347

server_path = '/files'

cwpath = os.getcwd()

os.makedirs(cwpath+server_path, exist_ok=True)

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server's IP address and port
server_socket.bind((server_ip, server_port))

# Listen for a connection
server_socket.listen(1)
print('Server is listening...')

def handle_client(client_socket,client_address):
    while True:
        # Receive the operation
        operation = client_socket.recv(1024).decode()

        if operation == 'list':
            # Send the list of files
            files = os.listdir(cwpath+server_path)
            if(len(files) == 0):
                client_socket.send('There is no files in the server'.encode())
            else:
                send_data = 'files:\n'
                for file in files:
                    send_data += file + '\n'
                client_socket.send(send_data.encode())
                print(f"File list sent to {client_address}")
        elif operation == 'upload':
            # Receive the filename
            filename = client_socket.recv(1024).decode()

            if(os.path.exists(cwpath+server_path+'/'+filename)):
                client_socket.send('File already exists'.encode())
            else:
                client_socket.send('OK'.encode())
                print(f"uploading from {client_address}")

                res = client_socket.recv(1024).decode()
                if res == 'File not found':
                    print('File not found')
                    continue
                # Receive the file size
                file_size = int(res)

                with open(cwpath+server_path+'/'+filename, 'wb') as file:
                    print(f'Saving file {filename}')
                    received_size = 0
                    while received_size < file_size:
                        file_data = client_socket.recv(1024)
                        received_size += len(file_data)
                        file.write(file_data)
                
                print(f"File {filename} uploaded successfully from {client_address}")
                
                client_socket.send('File uploaded successfully'.encode())

        elif operation == 'download':
            # Receive the filename
            filename = client_socket.recv(1024).decode()

            if(os.path.exists(cwpath+server_path+'/'+filename)):
                client_socket.send('OK'.encode())
                print(f"downloading to {client_address}")
                file_size = os.path.getsize(cwpath+server_path+'/'+filename)
                client_socket.send(str(file_size).encode())
                with open(cwpath+server_path+'/'+filename, 'rb') as file:
                    while True:
                        file_data = file.read(1024)
                        if not file_data:
                            break
                        client_socket.send(file_data)
                print(f"File {filename} downloaded successfully to {client_address}")
            else:
                client_socket.send('File does not exist'.encode())
        else:
            client_socket.send('Invalid operation'.encode())
        
        time.sleep(0.5)

while True:
    # Accept a connection
    try:
        client_socket, client_address = server_socket.accept()
        print(f'Accepted connection from {client_address}')

    # Create a new thread to handle this client
        threading.Thread(target=handle_client, args=(client_socket,client_address,)).start()
    except KeyboardInterrupt:
        server_socket.close()
        break