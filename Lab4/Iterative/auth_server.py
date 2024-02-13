import socket

IP = 'localhost'
AUTH_PORT = 8003
BUFFER_SIZE = 1024
FORMAT = "utf-8"

auth_records = {
    'cse.du.ac.bd': '192.0.2.3',
    'google.com': '142.250.193.110'
}

def handle_query(data, addr, server):
    query = data.decode(FORMAT)
    print(f"Authoritative Server received query: {query}")

    if query in auth_records:
        server.sendto(auth_records[query].encode(FORMAT), addr)
    else:
        server.sendto("Not Found".encode(FORMAT),addr)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((IP, AUTH_PORT))
    print(f"Authoritative Server listening on {IP}:{AUTH_PORT}")

    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        handle_query(data, addr, server)

if __name__ == "__main__":
    start_server()