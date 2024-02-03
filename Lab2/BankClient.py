import socket
import time
import random

class BankClient:
    def __init__(self):
        self.host = 'localhost'
        self.port = 4532
        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))
        self.id = 0

    def send_withdraw_req(self, wit):
        self.client_socket.send(wit.encode())
        time.sleep(1)
        strid = str(self.id)
        self.client_socket.send(strid.encode())

    def run(self):
        us = input('Enter your username: ')
        self.client_socket.send(us.encode())
        pas = input('Enter your password: ')
        self.client_socket.send(pas.encode())
        cc = self.client_socket.recv(1024).decode()
        if cc == '404':
            print('invalid Data')
            self.client_socket.close()
            return
        while True:
            print('Please Select')  # ATM booth menu option
            print('1.CHECK BALANCE')
            print('2.CASH WIHDRAWAL')
            print('3.CASH DEPOSITE')
            choose = input('ENTER : ')  # enter desired option
            self.client_socket.send(choose.encode())
            if choose == '1':
                print(self.client_socket.recv(1024).decode())
            elif choose == '3':
                dep = input('Enter amount :')  # enter deposit amount
                if int(dep) <= 0:
                    print('Invalid amount')
                else:
                    while True:
                        self.client_socket.send(dep.encode())
                        dd = self.client_socket.recv(1024).decode()
                        print(dd)
                        if dd == "555":
                            print("Transaction Failed")
                            print('Try Again?')
                            print('1.YES')
                            print('2.NO')
                            try_again = input('ENTER : ')
                            if try_again == '1':  # press 1 for again go back to the menu
                                self.client_socket.send(('3').encode())  # press 2 for closing connection
                                time.sleep(0.5)
                                continue
                            else:
                                break
                        else:
                            break
                    
            elif choose == '2':
                self.id = random.randint(0, 10)
                wit = input('Enter amount :')  # enter withdrawal amount
                print(wit)
                wi = int(wit)
                if wi <= 0:
                    print('Invalid amount')
                else:
                    while True:
                        self.send_withdraw_req(wit)  # send request id, withdrawal amount
                        rr = self.client_socket.recv(1024).decode()
                        print(rr)
                        if rr == '501':
                            print('Insufficient Balance')
                            break
                        if rr == '502':
                            print('Already requested')
                            break
                        elif rr == '555':
                            print("Transaction Failed")
                            print('Try Again?')
                            print('1.YES')
                            print('2.NO')
                            try_again = input('ENTER : ')
                            if try_again == '1':  # press 1 for again go back to the menu
                                self.client_socket.send(('2').encode())  # press 2 for closing connection
                                time.sleep(0.5)
                                continue
                            else:
                                break
                        else:
                            break
            print('Anything else')  # after executing one request
            print('1.YES')
            print('2.NO')
            a = input('ENTER : ')  # enter the desired option
            if a == '2':
                self.client_socket.send(('close').encode())
                break
        self.client_socket.close()  # close the connection

client = BankClient()
client.run()