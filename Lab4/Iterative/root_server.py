import socket

IP = 'localhost'
ROOT_PORT = 8001
TLD_PORT = 8002
BUFFER_SIZE = 1024
FORMAT = "utf-8"

root_records = {
    'bd': TLD_PORT,
    'com': TLD_PORT,
}

def handle_query(data, addr, server):
    query = data.decode(FORMAT).split('.')[-1]  
    print(f"Root Server received query: {query}")

    if query in root_records:
        server.sendto(str(root_records[query]).encode(FORMAT), addr)
    else:
        server.sendto(str(TLD_PORT).encode(FORMAT), addr)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((IP, ROOT_PORT))
    print(f"Root Server listening on {IP}:{ROOT_PORT}")

    while True:
        data, addr = server.recvfrom(BUFFER_SIZE)
        handle_query(data, addr, server)

if __name__ == "__main__":
    start_server()