import socket
import random

class BankServer:
    def __init__(self):
        self.users = {
            "araf": {
                "password": "1234",
                "balance": 10000
            },
            "zisan": {
                "password": "1234",
                "balance": 10000
            }
        }
        self.dict = list()
        self.hostname = socket.gethostname()
        self.host = socket.gethostbyname(self.hostname)
        self.port = 4532
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', self.port))
        print(f"Server started on port {self.port}")
        self.server_socket.listen(5)
        self.conn, self.address = self.server_socket.accept()
        print("Connection from: " + str(self.address))

    def run(self):
        while True:
            data = self.conn.recv(1024).decode()
            if not data:
                break
            if data in self.users:
                user = data
                data = self.conn.recv(1024).decode()
                if data == self.users[user]['password']:
                    self.conn.send(('40').encode())
                    while True:
                        choice = self.conn.recv(1024).decode()
                        print('choice', choice)
                        if choice == 'close':
                            return
                        if int(choice) == 1:  # choice 1 for checking balance
                            print('choice: ', choice)
                            self.conn.send(('Your Balance is: ' + str(self.users[user]['balance'])).encode())
                        elif int(choice) == 3:  # choice3 for cash deposit
                            amnt = self.conn.recv(1024).decode()
                            amnt = int(amnt)
                            print('deposited amount: ', amnt)
                            rand = random.randint(0, 100)
                            print('rand', rand)
                            if rand > 70:
                                self.conn.send(('555').encode())
                            else:
                               self.users[user]['balance'] = self.users[user]['balance'] + amnt
                               self.conn.send(('New amount added. Your Balance is: ' + str(self.users[user]['balance'])).encode())
                        else:
                            amnt = self.conn.recv(1024).decode()  # for cash withdrawal
                            amnt = int(amnt)
                            print(amnt)
                            id = self.conn.recv(1024).decode()
                            print(f"id={id}")
                            print('requested withdrawn amount: ', amnt)
                            if id in self.dict:
                                self.conn.send(('502').encode())
                            elif amnt > self.users[user]['balance']:  # if requested amount is greater than acc balance
                                self.conn.send(('501').encode())
                            else:
                                rand = random.randint(0, 100)
                                print('rand', rand)
                                if rand > 70:
                                    self.conn.send(('555').encode())
                                else:
                                    self.dict.append(id)
                                    self.users[user]['balance'] = self.users[user]['balance'] - amnt
                                    self.conn.send(('Withdrawn successful. Your Balance is: ' + str(self.users[user]['balance'])).encode())
                    print(self.dict)
                else:
                    print('Invalid Password')  # if password is not match
                    self.conn.send(('404').encode())
            else:
                print('Invalid User') # if user id is not match 
                self.conn.send(('404').encode())
        self.conn.close()  # close the connection

server = BankServer()
server.run()