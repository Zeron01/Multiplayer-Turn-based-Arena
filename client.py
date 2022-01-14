import socket
import threading
import sys
import time
import os
import time

class Client:
    def __init__(self,name:str="Bob") -> None:
        self.name = name
        self.client:socket.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.message = "" 
    def receive(self,display = True):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                self.message = message
                if message == 'NICK':
                    self.client.send(self.name.encode('ascii'))
                    continue
                elif "NOTIFY" == message and os.name =='nt':
                    self.client.send("NOTIFY".encode("ascii"))
                    if not display:
                        print(f"{self.name} received a challenge")
                        time.sleep(5)
                        self.client.send("y".encode("ascii"))
                        print(f"{self.name} accepted")
                        time.sleep(0.2)
                    continue
                if not display:
                    continue
                if "Clear" in message:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(message.replace("Clear",""))
                else:
                    if message !="":
                        print(message)
            except (ConnectionResetError,BrokenPipeError):
                print("An error occurred")
                print("Enter to leave")
                self.client.close()
                break
            except ConnectionAbortedError:
                self.client.close()
                break
    def write(self):
        try:
            while True:
                message = input("")
                #line below is meant to hide the user input immediately after they enter, makes the chat rooms a lot more nicer to look at
                print("\033[A                             \033[A")
                try:  
                    self.client.send(message.encode('ascii'))
                except UnicodeEncodeError:
                    print("No special characters")
        except OSError:
            return
    def start(self):
        while True:
            try:
                fh = open('settings.txt')
                content = fh.readlines()
                fh.close()
                host = content[0][4:].rstrip("\n")
                port = content[1][6:].rstrip("\n")
                self.client.connect((host,int(port)))
                break
            except (socket.gaierror,ValueError):
                print("Error: Not valid format, please ensure the IPs and PORT are correct in settings.txt")
            except (ConnectionRefusedError):
                print("Error: No connection was made, please ensure that there is an active connection before attempting to connect")
            input ("Enter any key to quit\n")
            return -1
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.start()
    def debug(self,num:str="",command="fight"):
        if num == 0:
            num = ""
        while True:
            try:
                fh = open('settings.txt')
                content = fh.readlines()
                fh.close()
                host = content[0][4:].rstrip("\n")
                port = content[1][6:].rstrip("\n")
                self.client.connect((host,int(port)))
                break
            except (socket.gaierror,ValueError):
                print("Error: Settings have incorrect IP format")
                return -1
            except (ConnectionRefusedError):
                print("Error: No connection was made")
                return -1
        thread1 = threading.Thread(target=self.receive,args=(False,))
        thread1.start()
        while True:
            if "BOT" in self.name:
                break
            if self.message != "BEGIN":
                continue
            #line below is meant to hide the user input immediately after they enter, makes the chat rooms a lot more nicer to look at
            time.sleep(5)
            if command == "spectate":
                time.sleep(20)
                self.client.send(f"/{command} {num}".encode("ascii"))
            elif command == "fight": 
                self.client.send(f"/{command} [BOT]{num}".encode("ascii"))
            self.message = ""
     
def __main():
    x = input("Enter nickname\n>")
    player = Client(x)
    player.start()



if __name__ == "__main__":
    __main()