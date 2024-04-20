import socket
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

LINK_UPDATE_DURATION = 30
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
neighour = []
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
    neighour.append(int(numbers[1]))
    adjMatrix[int(numbers[0])][int(numbers[1])] = int(numbers[2])
    # adjMatrix[int(numbers[1])][int(numbers[0])] = int(numbers[2])
  
  # for row in adjMatrix:
  #   s_print(row)
  
  s_print(splittedData)

def dijkstra(graph, start):
  num_vertices = len(graph)
  start_time = time.time() * 1000

  shortest_distances = np.full(num_vertices, np.inf)
  parent = np.full(num_vertices, -1)
  visited = np.full(num_vertices, False)
  shortest_distances[start] = 0

  for _ in range(num_vertices):
      min_dist = np.inf
      min_index = -1
      
      # Find the vertex with the shortest distance
      for v in range(num_vertices):
          if not visited[v] and shortest_distances[v] < min_dist:
              min_dist = shortest_distances[v]
              min_index = v
      
      visited[min_index] = True
      
      # Update distances for vertices adjacent to the current vertex
      for v in range(num_vertices):
          if not visited[v] and graph[min_index][v] != 0 and shortest_distances[min_index] != np.inf:
              new_dist = shortest_distances[min_index] + graph[min_index][v]
              if new_dist < shortest_distances[v]:
                parent[v] = min_index
                shortest_distances[v] = new_dist

  end_time = time.time() * 1000
  total_time = end_time - start_time
  s_print(Color.GREEN + f"Dijkstra's Algorithm Running Time: {total_time}ms" + Color.END)
                  
  return shortest_distances, parent


# returns a string
# slight modification needed
def create_packet(content: str):
  global message_id
  packet_id = f"{ID}00000000{message_id}"
  message_id += 1
  LSP = f"{packet_id}#{TTL}#{content}"
  s_print(f"Packet sent: {packet_id}")
  return LSP

# packet = in string, should be converted to bytes before sending
def sendPacket(ADDRESS , packet: str , packetID):
  try:
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    s.connect(ADDRESS)
    
    s.send(packet.encode(ENCODER))
    checker[packetID] = 1
    return True
    
  except Exception as e :
    # traceback.s_print_exc()
    s_print(f"Connection failed to {ADDRESS}")
    return False
  
  
# packet = string
def broadCast(packet: str):
  decodePacket = packet.split("#")
  if(decodePacket[0] in checker ):
    return
  s_print(f"Broadcast packet_id: {decodePacket[ID_INDEX]}")
  
  currentReceivers = neighour
  
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

  shortest_distance, parent = dijkstra(adjMatrix, ID)
  s_print("Ran Dijkstra. Current state is: ")
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
    neighbourToUpdateIndex = random.randint(0, len(neighour) - 1)
    neighbourToUpdate = neighour[neighbourToUpdateIndex]
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
  LSP = create_packet(fileInformation)
  
  broadCastThread = threading.Thread(target=broadCast, args=(LSP,))
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