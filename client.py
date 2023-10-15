import socket
import threading
import sys
import time
import os
import time
import fileIO
class Client:
    def __init__(self,name:str="Bob") -> None:
        self.name = name
        self.client:socket.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.message = "" 
    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                self.message = message
                if message == 'NICK':
                    self.client.send(self.name.encode('ascii'))
                    continue
                elif "NOTIFY" == message:
                    if  os.name =='nt': self.client.send("NOTIFY".encode("ascii"))
                    continue
                if  len(message) >= len("Clear") and message[0:5]=="Clear":
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
    def write(self,visible):
        try:
            while True:
                message = input("")
                #line below is meant to hide the user input immediately after they enter, makes the chat rooms a lot more nicer to look at
                if not visible:print("\033[A                             \033[A")
                try:  
                    self.client.send(message.encode('ascii'))
                except UnicodeEncodeError:
                    print("No special characters")
        except OSError:
            return
    def start(self):
        print("----------")
        print("Warning: You should not see this message")
        print("\033[A                             \033[A")
        print("Did you see a warning message above? (y/n)")
        visible = False
        while True:
            check = input(">")
            if check == 'y':
                visible = True
                print("Not capable of clearing user input")
                time.sleep(1)
                break
            elif check == 'n':
                break
            else:
                print("Please choose valid option")
        try:
            host,port = fileIO.retrieveHostPort()
        except (IOError,IndexError):
            print("Error when parsing settings, exiting...")
            return -1
        try:
            self.client.connect((host,int(port)))
            receive_thread = threading.Thread(target=self.receive)
            receive_thread.start()
            write_thread = threading.Thread(target=self.write,args=(visible,))
            write_thread.start()
        except (socket.gaierror,ValueError):
            print("Error: Not valid format, please ensure the IPs and PORT are correct in settings.txt")
            return -1
        except (ConnectionRefusedError):
            print("Error: No connection was made, please ensure that there is an active connection before attempting to connect")
            return -1
def __main():
    x = input("Enter nickname\n>")
    player = Client(x)
    player.start()
if __name__ == "__main__":
    __main()