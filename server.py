import threading
import socket
import time
import random
from datetime import datetime
from typing import Tuple
import traceback

#Player Class to be implemented in C++
class Player:
    def __init__(self,name,client,health = 100,level = 1, exp = 0,expMax = 100,defense = 0)->None:
        self.name: str = name
        self.health: int = health
        self.level: int = level
        self.inventory = []
        self.exp: int = exp
        self.expMax: int = expMax
        self.maxHealth: int = self.health
        self.wins: int = 0
        self.defense: int = defense
        self.client: socket = client
        self.busy: bool = False
        self.room: Room = None
    def receiveMsg(self)->str:
        return self.client.recv(1024).decode("ascii")
    def sendMsg(self,message:str)->None:
        self.client.send(message.encode("ascii"))
    def levelup(self,addlevel:int=1)->None:
        if addlevel!=1:
            self.expMax = 50 *(addlevel+1)
            self.level = addlevel
            self.health = self.level*100
            self.maxHealth = self.health
            self.exp = 0
            self.defense=5*self.level
            return
        while self.exp >= self.expMax:
            self.level+=1
            self.health = self.level*100
            self.maxHealth = self.health
            self.exp -= self.expMax
            self.expMax+=50
            self.defense+=5
    def attack(self,other:'Player')->Tuple[int,bool,bool]: #yes
        player = self
        damage: int = ((player.level*15)-other.defense) + (random.randint(1,5*player.level))
        critical = player.critical(other)
        dodge = other.dodge()
        if damage < 0:
            damage = 1
        if critical:
            damage*=2
        return damage, critical,dodge
    def critical(self,other: 'Player')->bool:
        x = [True,False,False,False,False,False,False,False] #1/8 chance of landing a critical
        if self.level-other.level >= 10:
            return True #If the difference of level is greater than/equal to 10, 100% critical chance
        x = random.choice(x)
        return x 
    def dodge(self)->bool:
        x = random.choice([True,False,False,False,False,False,False,False]) #1/8 chance of dodging
        return x
    def alive(self)->bool:
        if self.health <=0:
            self.health = 0
            return False
        return True
    def killed(self,other: 'Player')->Tuple[int,bool]:
        expGained = other.level *50 + 50
        levelUp = False
        self.exp+=expGained
        if self.exp >=self.expMax:
            levelUp = True
            self.levelup()
        return expGained, levelUp
    def restorehealth(self)->None:
        self.health = self.maxHealth
    def __str__(self):
        text=("------------------------------\n")
        text += (f"Profile: {self.name}\n\nLevel: {formatComma(self.level)}\nHealth: {formatComma(self.health)}/{formatComma(self.maxHealth)}\nDefense: {formatComma(self.defense)}\nExp: {formatComma(self.exp)}/{formatComma(self.expMax)}\nWins: {formatComma(self.wins)}\nInventory: [")
        text+=']\n'
        if not self.alive():
            deadtext = (f"\nStatus: Dead")
            text+=deadtext
        else:
            alivetext = (f"\nStatus: Alive")
            text+=alivetext
        text+=("\n------------------------------")
        return text
#Helper function for Player / Dialogue class?
def criticalQuotes() -> str:
    dialogue = ["One of us has to die...","You will not live to see another day","I'll keep it simple","Pick a god and pray...","I didn't want to do this...","You're already dead.","I promise you won't leave in one piece","Don't waste my time.","I'll promise a swift death","Any last words?","Pay with your life","You're not worth my time","Start booking your funeral","I'll send you to hell","Just so you know, this isn't personal","Nothing personal kid","Don't take this personal","I'll make this quick","No one to save you now","Losing my patience","Pathetic","It didn't have to be this way"]
    return random.choice(dialogue)
def criticalCheck(check:bool) -> str:
    if check == True:
        return ' critical'
    else:
        return ''
def deathQuotes() -> str:
    dialogue = ["Not like this","NOOOOOOOOOOO","Impossible....","I...I never thought you'd be this good...","To end... like this?","What? Huh? What's happening?","NO! No, no, no!","No, no, no... I can't die like this",f"I'm sorry{random.choice([' mother...',' father...'])}","Why now....?","I was so close","I failed my family...","Goodbye...","..."]
    return random.choice(dialogue)
def dodgeQuotes() -> str:
    dialogue = ["You fool","Not even close", "Too slow", "I saw that from a mile away","You think that was going to hit me??","Miss me with that?","PIKACHU USE DODGE","was that ur best?","even my grandma could dodge that","you call that an attack?","are you even trying to hurt me?","Please...like that would ever hit me",f"I can be {random.choice(['sleeping','knocked out'])} and you still can't hit me"]
    return random.choice(dialogue)  
def formatComma(number) -> str:
    return "{:,}".format(number)

#Room Class to be implemented in C++
class Room:
    def __init__(self,roomType):
        self.players: dict = {}
        self.logs: str = ""
        self.roomType = roomType
    def __getitem__(self, key:str)->Player:
        return self.players[key]
    def __contains__(self,key:str)->bool:
        if key in self.players:
            return True
        return False
    def __len__(self)->int:
         return len(self.players)
    def __iter__(self):
        return iter(self.players)
    def keys(self):
        return self.players.keys()
    def items(self):
        return self.players.items()
    def values(self):
        return self.players.values()
    def displayRoom(self)->str:
        if len(self)==0:
            return "Current Occuptants: No one"
        else:
            message = "Current Occuptants:\n"
            for key in self:
                message+=">"+key
                message+="\n"
            return message
    def broadcast(self,message: str,save: bool=False):
        if save:
            self.logs += message +"\n"
        kicked = []
        for key in self:
            try:
                self[key].sendMsg(message)
            except OSError:
                kicked.append(key)
        for player in kicked:
            self.leave(self[player])
    def addPlayer(self,avatar: Player):
        self.players[avatar.name] = avatar
        avatar.room = self
    def leave(self,avatar: Player):
        del self.players[avatar.name]
    def refresh(self):
        for key in self:
            self[key].sendMsg("Clear")
    def removeAll(self):
        self.players.clear()
#Arena Class 
class Arena(Room):
    def __init__(self,player1:str,player2:str):
        super().__init__("Arena")
        self.player1:str = player1
        self.player2:str = player2
        self.addPlayer(players[player1])
        self.addPlayer(players[player2])
    def displayRoom(self) -> str:
        if len(self)==0:
            return "Current Occuptants: No one"
        else:
            message = "Current Occuptants:\n"
            for key in self:
                message+=">"+key
                if key != self.player1 and key != self.player2:
                    message+=" (Spectating)"
                message+="\n"
            return message
    def combat(self)->None:
        fighter1 = self.player1
        fighter2 = self.player2
        arena = self
        turn = 1
        arena.broadcast(f'-->[{fighter1} vs. {fighter2}]<--\n\n')
        arena[fighter1].restorehealth()
        arena[fighter2].restorehealth()
        while arena[fighter1].health > 0 and arena[fighter2].health > 0:
            arena.broadcast(f'Turn {turn}\n\n')
            opponent=fighter2
            for fighter in (fighter1,fighter2):
                arena.broadcast(f'->[{fighter}\'s turn]<-\n')
                time.sleep(0.1)
                damage, critical, dodge = arena[fighter].attack(arena[opponent])
                if critical:
                    arena.broadcast(f'{fighter}: {criticalQuotes()}')
                    time.sleep(0.2)
                if dodge:
                    arena.broadcast(f'{opponent}: {dodgeQuotes()}')
                    time.sleep(0.2)
                    arena.broadcast(f'{opponent} dodges a{criticalCheck(critical)} strike from {fighter}\n')
                    time.sleep(0.2)
                else:
                    arena.broadcast(f'[{formatComma(arena[fighter].health)}/{formatComma(arena[fighter].maxHealth)} HP] {fighter} deals {formatComma(damage)}{criticalCheck(critical)} damage to {opponent} [{formatComma(arena[opponent].health)}/{formatComma(arena[opponent].maxHealth)} HP]\n')
                    time.sleep(0.2)
                    arena[opponent].health-=damage
                time.sleep(1)
                if not arena[opponent].alive():
                    expGained, levelup = arena[fighter].killed(arena[opponent])
                    arena[fighter].wins+=1
                    arena.broadcast(f'\n{opponent}: {deathQuotes()}')
                    time.sleep(0.1)
                    arena.broadcast(f'{opponent} has fallen')
                    break
                opponent = fighter1
            turn+=1
def gameRoom(player1: Player,player2: Player):
    arenas = serverRooms["Arenas"]
    lobby:Room = serverRooms["Lobby"]
    lobby.leave(player1)
    lobby.leave(player2)
    arena: Arena = Arena(player1.name,player2.name)
    arena.refresh()
    arenas.append(arena)
    lobby.refresh()
    time.sleep(0.1)
    lobby.broadcast(sendChatRooms())
    try:
        print(f"{getTime()} Fight started between {player1.name} and {player2.name}")
        arena.combat()
        arenas.remove(arena)
        time.sleep(0.5)
        player1.sendMsg(str(player1))
        player2.sendMsg(str(player2))
        for player in arena:
            lobby.addPlayer(arena[player])
        arena.broadcast("Game Over")
        arena.removeAll()
        time.sleep(1)
        lobby.broadcast(sendChatRooms())
        print(f"{getTime()} Game ended")
    except KeyError:
        arenas.remove(arena)
        for x in arena:
            print(f"{arena[x].name} was freed from the fightRoom")
            lobby.addPlayer(arena[x])
        time.sleep(0.1)
        lobby.refresh()
        time.sleep(0.1)
        lobby.broadcast(sendChatRooms())
        if player1.name not in arena:
            lobby.broadcast(f"\n{player1.name} rage quit lmao")
        else:
            lobby.broadcast(f"\n{player2.name} rage quit lmao")
        arena.removeAll()


#Static server class to be implemented in C++
host = "127.0.0.1" # localhost
port = 25565       # port
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
players = {}
serverRooms = {}
def sendChatRooms() -> str:
    lobby = serverRooms["Lobby"]
    rooms = serverRooms["Chat"]
    arenas = serverRooms["Arenas"]
    lobbyChat = "\nLobby\n"
    for people in lobby:
        lobbyChat+=">"+lobby[people].name
        lobbyChat+="\n"
    lobbyChat+="\n"
    message = "Available chatrooms\n\n"
    for x in range(0,len(rooms)):
        message+= "Room "+str(x+1)+"\n"+rooms[x].displayRoom()
        message+="\n\n"
    fights = "Arenas\n\n"
    for x in range(0,len(arenas)):
        fights+= "Arena "+str(x+1)+"\n"+arenas[x].displayRoom()
        fights+="\n\n"
    return (lobbyChat+message+fights)
def handleCommands(avatar:Player,message:str):
    if message == "NOTIFY":
        return
    roomType = avatar.room.roomType
    if roomType == "Lobby":
        handleLobby(avatar,message)
        return
    elif roomType == "Chat":
        handleChatRooms(avatar,message)
    elif roomType == "Arena":
        handleArena(avatar,message)
def handleLobby(avatar:Player,message:str):
    rooms = serverRooms["Chat"]
    lobby:Room = serverRooms["Lobby"]
    arenas = serverRooms["Arenas"]
    if message =="/help":
        avatar.sendMsg(getCommands())
        return
    if message == "/fight":
        handleRequests(avatar)
        return
    if message =="/list":
        avatar.sendMsg(sendChatRooms())
        return
    if (message=="/leaderboards"):
        avatar.sendMsg(getStats())
        return
    if (message=="/profile"):
        avatar.sendMsg(str(avatar))
        return
    if (message =="/spectate"):
        avatar.sendMsg("Which room?")
        message = avatar.receiveMsg()
        for index in range(0,len(arenas)):
            if message == str(index+1):
                lobby.leave(avatar)
                arenas[index].addPlayer(avatar)
                lobby.broadcast(sendChatRooms())
                return
    if (message =="/join"):
        avatar.sendMsg("Which room?")
        message = avatar.receiveMsg()
        for index in range(0,len(rooms)):
            if message == str(index+1):
                lobby.leave(avatar)
                rooms[index].addPlayer(avatar)
                lobby.refresh()
                lobby.broadcast(sendChatRooms())
                lobby.broadcast(f"{avatar.name} left the lobby")
                print(f"{avatar.name} entered room {index+1}")
                avatar.sendMsg("Clear")
                avatar.sendMsg(f"Room {index+1}:")
                avatar.sendMsg(rooms[index].displayRoom())
                avatar.sendMsg(rooms[index].logs)
                rooms[index].broadcast(f"{avatar.name} entered the room ")
                return
    avatar.sendMsg("Invalid input")
    time.sleep(0.1)
def handleChatRooms(avatar:Player,message:str):
    room = avatar.room
    if(message =="/leave"):
        lobby:Room = serverRooms["Lobby"]
        lobby.addPlayer(avatar)
        room.leave(avatar)
        lobby.refresh()
        lobby.broadcast(sendChatRooms())
        lobby.broadcast(f"{avatar.name} joined the lobby")
        room.broadcast(f"{avatar.name} has left the room")
        print(f"{avatar.name} left a room")
        return
    else:
        if len(message) > 50:
            message = message[0:50]
        name = avatar.name
        name+=": "+message
        room.broadcast(f"{getTime()} {name}",1)
        return
def handleArena(avatar:Player,message:str):
    arena = avatar.room
    if message == "/leave":
        arena.leave(avatar)
        time.sleep(0.1)
        serverRooms["Lobby"].addPlayer(avatar)
        avatar.sendMsg(sendChatRooms())
        return
def handleRequests(avatar:Player):
    avatar.sendMsg("Fight who?") #can be any command 
    name = avatar.receiveMsg()
    if not (name in players and name != avatar.name):
        avatar.sendMsg("Player not found")
        return
    avatar2:Player = players[name]
    available = not avatar2.busy
    if not available or not avatar2.name in serverRooms["Lobby"]:
        avatar.sendMsg("That player is currently in another room")
        return
    #This request appender to prevent other players from requesting this specific player
    #avatar.request.append(avatar2)
    avatar.busy = True
    avatar2.busy = True
    avatar.sendMsg("Sent fight request")
    print(f"{getTime()} {avatar.name} requested to fight {avatar2.name}")
    avatar2.sendMsg(f"Would you want to fight {avatar.name} (y/n)?")
    avatar2.sendMsg(f"NOTIFY")
    try:
        if(avatar2.receiveMsg()=="y"):
            avatar.sendMsg("Player Confirmed")
            gameRoom(avatar,avatar2) #this function can be replaced seamlessly
        else:
            avatar2.sendMsg("Declined request")
            avatar2.sendMsg("You have declined the request")
            avatar.sendMsg("Declined request")
    except (ConnectionResetError,BrokenPipeError): #user left the applicaiton before accepting
        print("HERE NOW")
        pass
    #avatar.request.remove(avatar2)
    avatar.busy = False
    avatar2.busy = False
def handleAvatar(avatar:Player):
    while True:
        try:
            message = avatar.receiveMsg()
            try:
                handleCommands(avatar,message)
            except AttributeError as e:
                pass
        except socket.timeout:
            pass
        except (ConnectionResetError,BrokenPipeError) as e:
            avatar.client.close()
            roomCleanup(avatar)
            print(f"{avatar.name} left the application")
            del players[avatar.name]
            
            break
        except Exception as e:
            traceback.print_exc()
            try:
                x = str(e)
                avatar.sendMsg(f"Restart Application, Fatal Error")
            except OSError:
                pass
            roomCleanup(avatar)
            avatar.client.close()
            print(f"FATAL: {avatar.name} left the application")
            del players[avatar.name]
            break
def roomCleanup(avatar:Player):
    room = avatar.room
    avatar.room = None
    room.leave(avatar)
    room.refresh()
    if room.roomType == "Lobby":
        room.broadcast(f"{sendChatRooms()}\n{avatar.name} left the server")
    elif room.roomType == "Chat":
        print("Was in room")
        room.broadcast(f"{sendChatRooms()}\n{avatar.name} unexpectedly left")
def receive():
    print("Server is now listening for clients")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        if nickname in players:
            x: str =nickname
            index = 1
            while nickname in players:
                nickname = x
                nickname+=str(index)
                index+=1
            client.send(f"Your name is {nickname} since that user already exists".encode("ascii"))
        if len(nickname) >15:
            nickname = nickname[0:15]
        avatar: Player = Player(nickname,client)
        players[nickname] = avatar
        print(f"Nickname of the client is {nickname}")
        avatar.sendMsg('Connected to the server!')
        serverRooms["Lobby"].addPlayer(avatar)
        time.sleep(0.1)
        serverRooms["Lobby"].refresh()
        serverRooms["Lobby"].broadcast(sendChatRooms())
        serverRooms["Lobby"].broadcast(f"{nickname} joined the lobby")
        avatar.sendMsg("\nUse /help to list commands")
        thread = threading.Thread(target=handleAvatar,args=(avatar,))
        thread.start()
def getTime():
    now = datetime.now()
    hours = int(now.hour)
    if hours > 12:
        hours-=12
    minutes = (now.minute)
    if minutes <10:
        minutes = "0"+str(minutes)
    return f"[{hours}:{minutes}]"
def getStats():
    profiles: str = ""
    for names in players:
        profiles+=(str(players[names]))
    return profiles
def getCommands():
    message = """
    /list         -> List the lobby rooms again\n
    /leaderboards -> List the player leaderboards\n
    /profile      -> List your player profile\n
    /join         -> Join a room by the room numbers\n
    /fight        -> Request to fight another player\n
    /spectate     -> Watch an on-going fight in the arenas\n
    /leave        -> Leaves a room if inside spectating a fight or a chat room"""
    return message
def initServer():
    serverRooms["Lobby"] = Room("Lobby")
    serverRooms["Chat"] = []
    serverRooms["Arenas"] = []
    serverRooms["Chat"].append(Room("Chat"))
    serverRooms["Chat"].append(Room("Chat"))
    serverRooms["Chat"].append(Room("Chat"))
initServer()
receive()