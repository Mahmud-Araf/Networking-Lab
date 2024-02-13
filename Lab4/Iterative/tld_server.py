import socket

IP = 'localhost'
TLD_PORT = 8002
AUTH_PORT = 8003
BUFFER_SIZE = 1024
FORMAT = "utf-8"

tld_records = {
    'cse.du.ac.bd': AUTH_PORT,
    'google.com': AUTH_PORT,
}

def handle_query(data, addr, server):
    query = data.decode(FORMAT)
    print(f"TLD Server received query: {query}")

    if query in tld_records:
        server.sendto(str(tld_records[query]).encode(FORMAT), addr)
    else:
        server.sendto(str(AUTH_PORT).encode(FORMAT), addr)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((IP, TLD_PORT))
    print(f"TLD Server listening on {IP}:{TLD_PORT}")

    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        handle_query(data, addr, server)

if __name__ == "__main__":
    start_server()