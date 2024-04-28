import socket
import sys
import threading
import os
import numpy as np
import traceback
import time
import random
from threading import Lock

s_s_print_lock = Lock()
current_filename = os.path.basename(__file__)

def get_router_id():
  id_str = current_filename[6:-3]
  id = int(id_str)
  return id

LINK_UPDATE_DURATION = 60
ROWS = 10
COLS = 10
ID_INDEX = 0
TTL_INDEX = 1
CONTENT_INDEX = 2
message_id = 0
ID = get_router_id() 
TTL = 6
ENCODER = "utf-8"
IP_ADDRESS = "localhost"

FILENAME = f"Router{ID}.txt"

checker = {}

fileInformation = ""
NEIGHBOUR_ADDRESS = {
  1 : (IP_ADDRESS, 8888),
  2 : (IP_ADDRESS, 8889),
  3 : (IP_ADDRESS, 8890),
  4 : (IP_ADDRESS, 8891),
  5 : (IP_ADDRESS, 8892),
  6 : (IP_ADDRESS, 8893)
}
neighbour = []
adjMatrix = np.array (np.full((ROWS, COLS), np.inf) )
distanceArray = np.array (np.full((ROWS , COLS) , np.inf))

class Color:
  RED = '\033[91m'
  GREEN = '\033[92m'
  END = "\033[0m"

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return "An error occurred: {}".format(e)

# thread safe print function
def s_print(*a, **b):
  with s_s_print_lock:
      print(*a, **b)

def construct_initial_graph():
  global fileInformation
  fileInformation = read_file(FILENAME)
  splittedData = fileInformation.split("\n")
  for data in splittedData:
    numbers = data.split(",")
    neighbour.append(int(numbers[1]))
    adjMatrix[int(numbers[0])][int(numbers[1])] = int(numbers[2])
  s_print(splittedData)

def bellman_ford(graph, start):
    num_vertices = int(sys.argv[1]) + 1
    start_time = time.time() * 1000

    shortest_distances = np.full(num_vertices, np.inf)
    parent = np.full(num_vertices, -1)
    shortest_distances[start] = 0

    # Relax edges |V| - 1 times
    for _ in range(num_vertices - 1):
        for v in range(num_vertices):
            for w in range(num_vertices):
                if graph[v][w] != 0 and shortest_distances[v] != np.inf:
                    new_dist = shortest_distances[v] + graph[v][w]
                    if new_dist < shortest_distances[w]:
                        parent[w] = v
                        shortest_distances[w] = new_dist

    # Check for negative-weight cycles
    for v in range(num_vertices):
        for w in range(num_vertices):
            if graph[v][w] != 0 and shortest_distances[v] != np.inf:
                new_dist = shortest_distances[v] + graph[v][w]
                if new_dist < shortest_distances[w]:
                    s_print(Color.RED + "Graph contains a negative-weight cycle" + Color.END)
                    return None, None

    end_time = time.time() * 1000
    total_time = end_time - start_time
    s_print(Color.GREEN + f"Bellman-Ford Algorithm Running Time: {total_time}ms" + Color.END)

    return shortest_distances, parent


# returns a string
# slight modification needed
def create_packet(content: str):
  global message_id
  packet_id = f"{ID}00000000{message_id}"
  message_id += 1
  DVP = f"{packet_id}#{TTL}#{content}"
  s_print(f"Packet sent: {packet_id}")
  return DVP

# packet = in string, should be converted to bytes before sending
def sendPacket(ADDRESS , packet: str , packetID):
  try:
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    s.connect(ADDRESS)
    
    s.send(packet.encode(ENCODER))
    checker[packetID] = 1
    return True
    
  except Exception as e :
    s_print(f"Connection failed to {ADDRESS}")
    return False
  
  
# packet = string
def broadCast(packet: str):
  decodePacket = packet.split("#")
  if(decodePacket[0] in checker ):
    return
  s_print(f"Broadcast packet_id: {decodePacket[ID_INDEX]}")
  
  currentReceivers = neighbour
  
  while len(currentReceivers) > 0:
    flag = False
    temp = []
    for i in currentReceivers:
      ret = sendPacket(NEIGHBOUR_ADDRESS[i] , packet , decodePacket[0])
      if ret is False:
        temp.append(i)
      time.sleep(5)
    currentReceivers = temp
          
  

# got string with , and newLine for each entry  
def updateGraph(info):
  global distanceArray
  for row in info:
    data = row.split(",")
    s_print(f"data is {data}")
    adjMatrix[int(data[0])][int(data[1])] = int(data[2])

  shortest_distance, parent = bellman_ford(adjMatrix, ID)
  s_print("Ran Bellman-Ford. Current state is: ")
  for i in range(1, len(shortest_distance)):
    if i<=6:
      s_print(f"Node: {i}, shortest distance: {shortest_distance[i]}, parent: {parent[i]}")
      

def addToGraph(content):
    splittedRow = content.split("\n")
    updateGraph(splittedRow)


def packetReceive(client_socket, addr):
  message = client_socket.recv(1024)
  packet = message.decode(ENCODER)
  
  splitted = packet.split("#")
  addToGraph(splitted[CONTENT_INDEX])
  
  broadCastThread = threading.Thread(target=broadCast, args=(packet,))
  broadCastThread.start()
  
def UpdateLinkCost():
  while True:
    time.sleep(LINK_UPDATE_DURATION)
    neighbourToUpdateIndex = random.randint(0, len(neighbour) - 1)
    neighbourToUpdate = neighbour[neighbourToUpdateIndex]
    new_weight = random.randint(1, 100)
    new_link = f"{ID},{neighbourToUpdate},{new_weight}"
    
    s_print(Color.RED + f"updated link {new_link}" + Color.END)
    
    addToGraph(new_link)
    packet = create_packet(new_link)
    broadCast(packet)

def main():
  construct_initial_graph()
  
  # handle_client()
  host = IP_ADDRESS
  port = 8887 + ID

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind((host, port))
  server_socket.listen(5)
  DVP = create_packet(fileInformation)
  
  broadCastThread = threading.Thread(target=broadCast, args=(DVP,))
  broadCastThread.start()
  
  updateLinkWeightThread = threading.Thread(target=UpdateLinkCost, args=())
  updateLinkWeightThread.start()

  s_print(f"[*] Listening on {host}:{port}")

  try:
    while True:
        client_socket, addr = server_socket.accept()
        s_print(f"Connected to {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=packetReceive, args=(client_socket, addr,))
        client_handler.start()
  except KeyboardInterrupt:
    s_print(Color.RED + "\nServer Closed."+ Color.END)
  finally:
    server_socket.close()

if __name__ == "__main__":
    main()