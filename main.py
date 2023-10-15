from classes.Server import Server
import threading
import time
import subprocess
def handleInput(message) -> bool:
    while True:
        x = input(f"{message}\n>")
        if x == "y":
            return True
        elif x == "n":
            return False
        else:
            print("Please enter valid input")

def main():
    print("Setting up server")
    if not Server.initServer():
        print("Server has failed to start...exiting")
        return
    client = handleInput("Would you like to connect to the server using a client (opens another console)? (y/n)")
    sim = handleInput("Would you like to simulate a user base (adds 12 users)? (y/n)")
    threadRecieve = threading.Thread(target=Server.receive)
    threadWrite = threading.Thread(target=Server.adminCommands)
    threadRecieve.start()
    threadWrite.start()
    if sim:
        subprocess.call('start py userSim.py', shell=True)
        time.sleep(5)
    if client:
        subprocess.call('start py client.py', shell=True)
if __name__ == "__main__":
    main()