import socket
import threading
import sys
import time
import os
import time
nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = "127.0.0.1" # localhost
port = 25565
try:
    client.connect((host,port))
except:
    print("Failed to recieve a ping back, you probably did not join the hamachi, or the server isn't currently running")
    input("Enter to leave")
    sys.exit()
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'Clear':
                os.system('cls' if os.name == 'nt' else 'clear')
            elif "NOTIFY" == message and os.name =='nt':
                client.send("NOTIFY".encode("ascii"))
            else:
                if message !="":
                 print(message)
        except (ConnectionResetError,BrokenPipeError):
            print("An error occurred")
            print("Enter to leave")
            client.close()
            break
        except ConnectionAbortedError:
            client.close()
            break

def write():
    try:
        while True:
            message = input("")
            #line below is meant to hide the user input immediately after they enter, makes the chat rooms a lot more nicer to look at
            print("\033[A                             \033[A")
            try:  
                client.send(message.encode('ascii'))
            except UnicodeEncodeError:
                print("No special characters")
    except OSError:
        return
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

