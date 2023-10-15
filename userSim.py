import fileIO
import threading
import time
import socket
class UserSim:
    listsBots = []
    listsFighters = []
    __initialized = False
    def initLists(number = 4):
        if number > 10:
            print("Number too high, setting to 10")
            number = 10
        if UserSim.__initialized:
            print("Already initialized")
            return
        print("Initializing BOTS")
        for x in range(1,number+1):
            UserSim.listsBots.append(Bots(f"[BOT]{x}"))
            UserSim.listsFighters.append(Bots(f"[B0T]{x}"))
        UserSim.__initialized = True
    def start():
        if not UserSim.__initialized:
            print("Not initialized")
            return
        time.sleep(0.5)
        try:
            host,port = fileIO.retrieveHostPort()
        except (IOError,IndexError):
            print("Error when parsing settings, exiting...")
            return -1
        print("Preparing first half of bots")
        for bot in UserSim.listsBots:
            bot.client.connect((host,int(port)))
            bot.sendMsg(bot.name)
            time.sleep(0.15)
        print("Preparing second half of bots")
        for bot2 in UserSim.listsFighters:
            bot2.client.connect((host,int(port)))
            bot2.sendMsg(bot2.name) 
            time.sleep(0.15)
        print("Ready to begin simulation\nTo begin:\n1) On the main.py window, enter '2' to enter announcement mode\n2) Enter 'BEGIN' to start the user base simulation")
        while True:
            if UserSim.listsBots[0].receiveMsg() != "BEGIN":
                continue
            for (bot,bot2) in zip(UserSim.listsBots, UserSim.listsFighters):
                bot.sendMsg(f"/fight {bot2.name}")
                bot2.sendMsg("y")
                bot2.sendMsg("y")
            print("Cooldown: Waiting 25 seconds for next...")
            time.sleep(25)
            print("Able to run again fight command again")
class Bots:
    def __init__(self,name:str="Bob") -> None:
        self.name = name
        self.client:socket.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.message = "" 
    def receiveMsg(self)->str:
        return self.client.recv(1024).decode("ascii")
    def sendMsg(self,message:str)->None:
        self.client.send(message.encode("ascii"))


if __name__ == "__main__":
    print("Initializing...")
    UserSim.initLists()
    UserSim.start()
    input(":")

