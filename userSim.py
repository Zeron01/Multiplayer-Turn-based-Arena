from client import Client
import threading
import time
class UserSim:
    listsBots = []
    listsFighters = []
    __initialized = False
    def initLists(number = 6):
        if UserSim.__initialized:
            print("Already initialized")
            return
        print("Initializing BOTS")
        for x in range(number):
            if x == 0:
                x = ""
            UserSim.listsBots.append(Client(f"[BOT]{x}"))
            UserSim.listsFighters.append(Client(f"[A]Fighter{x}"))
        UserSim.__initialized = True
    def start():
        if not UserSim.__initialized:
            print("Not initialized")
            return
        time.sleep(0.5)
        print("Preparing first half of threads")
        for bot in UserSim.listsBots:
            thread = threading.Thread(target=bot.debug)
            thread.start()
        index = 0
        print("Preparing second half of threads")
        for player in UserSim.listsFighters:
            thread = threading.Thread(target=player.debug,args=(index,))
            thread.start()
            index+=1
        print("\n\nIn order to have the bots fight each other, go into (2) in the menu and enter 'BEGIN' to start the simulation")



if __name__ == "__main__":
    print("Initializing...")
    UserSim.initLists()
    UserSim.start()
    input("")

