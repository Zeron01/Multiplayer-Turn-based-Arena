import asyncio
import threading
import socket
import time
import fileIO
from datetime import datetime
from typing import Tuple
import traceback
from classes.Player import Player
from classes.Room import Room
from classes.Arena import Arena

import os
class Server:
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    players: dict = {} 
    serverRooms: dict = {} 
    __initialized:bool = False
    lock = threading.Lock()
    def initServer():
        if Server.__initialized:
            print("Server is already initialized")
            return True
        while True:
            try:
                host,port = fileIO.retrieveHostPort()
            except IOError:
                print("Server cannot be initialized, file failed to be read")
                return False
            except IndexError:
                if fileIO.updateHostPort() == -1:
                    print("Server cannot be initialized, file failed to be read")
                    return False
                print("Reverting file to default state, index error, reattempting with default")
                continue
            try:
                Server.server.bind((host,int(port)))
                Server.HOST  = host
                Server.PORT = int(port) 
                break
            except (socket.gaierror,ValueError):
                print("Not valid format, using default settings")
                if fileIO.updateHostPort() == -1:
                    print("Server cannot be initialized, file failed to be read")
                    return False
        Server.server.listen()
        print(f"Server is now listening for clients on {host}:{port}")
        Server.serverRooms["Lobby"] = Room("Lobby")
        Server.serverRooms["Chat"] = []
        Server.serverRooms["Arenas"] = []
        Server.serverRooms["Chat"].append(Room("Chat"))
        Server.serverRooms["Chat"].append(Room("Chat"))
        Server.serverRooms["Chat"].append(Room("Chat"))
        Server.__initialized = True
        return True
    def receive():
        if not Server.__initialized:
            print("Server has not been initialized, use Server.initServer() first")
            return
        while True:
            try:
                client, address = Server.server.accept()
                #print(f"Connected with {str(address)}")
                client.send('NICK'.encode('ascii'))
                nickname = client.recv(1024).decode('ascii')
                if nickname in Server.players:
                    x: str =nickname
                    index = 1
                    while nickname in Server.players:
                        nickname = x
                        nickname+=str(index)
                        index+=1
                    client.send(f"Your name is {nickname} since that user already exists".encode("ascii"))
                if len(nickname) >15:
                    nickname = nickname[0:15]
                    if nickname in Server.players:
                        client.send("\nInvalid name".encode("ascii"))
                        client.close()
                        continue
                avatar: Player = Player(nickname,client)
                Server.players[nickname] = avatar
                print(f"Nickname of the client is {nickname}")
                avatar.sendMsg('Connected to the server!')
                Server.serverRooms["Lobby"].addPlayer(avatar)
                time.sleep(0.1)
                Server.serverRooms["Lobby"].refresh()
                Server.serverRooms["Lobby"].broadcast(Server.sendChatRooms())
                Server.serverRooms["Lobby"].broadcast(f"{Server.getTime()} {nickname} joined the lobby")
                avatar.sendMsg("\nUse /help to list commands")
                thread = threading.Thread(target=Server.handleAvatar,args=(avatar,))
                thread.start()
            except Exception as e:
                print(e)
                continue
    def sendChatRooms() -> str:
        lobby = Server.serverRooms["Lobby"]
        rooms = Server.serverRooms["Chat"]
        arenas = Server.serverRooms["Arenas"]
        lobbyChat = f"\nLobby ({len(lobby)})\n"
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
        border = "\n"+"="*20
        return (border+lobbyChat+message+fights+border+'\n')
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
        for names in Server.players:
            profiles+=(str(Server.players[names]))
        return profiles
    def getCommands():
        message = """
        /list                 -> List the lobby rooms again\n
        /leaderboards         -> List the player leaderboards\n
        /profile              -> List your player profile\n
        /join {Room #}        -> Join a room by the room numbers\n
        /fight {Username}     -> Request to fight another player\n
        /spectate {Room #}    -> Watch an on-going fight in the arenas\n
        /leave                -> Leaves a room if inside spectating a fight or a chat room"""
        return message
    def handleCommands(avatar:Player,message:str):
        if message == "NOTIFY":
            return
        roomType = avatar.room.roomType
        if roomType == "Lobby":
            Server.handleLobby(avatar,message)
            return
        elif roomType == "Chat":
            Server.handleChatRooms(avatar,message)
        elif roomType == "Arena":
            Server.handleArena(avatar,message)
    def handleLobby(avatar:Player,message:str):
        rooms = Server.serverRooms["Chat"]
        lobby:Room = Server.serverRooms["Lobby"]
        arenas = Server.serverRooms["Arenas"]
        #implement switch case here
        if message =="/help":
            avatar.sendMsg(Server.getCommands())
            return
        if message[0:7] == "/fight ":
            name = message[7:len(message)]
            Server.handleRequests(avatar,name)
            return
        if message =="/list":
            avatar.sendMsg(Server.sendChatRooms())
            return
        if (message=="/leaderboards"):
            avatar.sendMsg(Server.getStats())
            return
        if (message=="/profile"):
            avatar.sendMsg(str(avatar))
            return
        if (message[0:10] =="/spectate "):
            message = message[10:len(message)]
            # message = avatar.receiveMsg()
            for index in range(0,len(arenas)):
                if message == str(index+1):
                    lobby.leave(avatar)
                    arenas[index].addPlayer(avatar)
                    lobby.broadcast(Server.sendChatRooms())
                    return
        if (message[0:6] =="/join "):
            # avatar.sendMsg("Which room?")
            # message = avatar.receiveMsg()
            message = message[6:len(message)]
            for index in range(0,len(rooms)):
                if message == str(index+1):
                    lobby.leave(avatar)
                    rooms[index].addPlayer(avatar)
                    lobby.refresh()
                    lobby.broadcast(Server.sendChatRooms())
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
            lobby:Room = Server.serverRooms["Lobby"]
            lobby.addPlayer(avatar)
            room.leave(avatar)
            lobby.refresh()
            lobby.broadcast(Server.sendChatRooms())
            lobby.broadcast(f"{avatar.name} joined the lobby")
            room.broadcast(f"{avatar.name} has left the room")
            print(f"{avatar.name} left a room")
            return
        else:
            if len(message) > 50:
                message = message[0:50]
            name = avatar.name
            name+=": "+message
            room.broadcast(f"{Server.getTime()} {name}",1)
            return
    def handleArena(avatar:Player,message:str):
        arena = avatar.room
        if message == "/leave":
            arena.leave(avatar)
            time.sleep(0.1)
            Server.serverRooms["Lobby"].addPlayer(avatar)
            avatar.sendMsg(Server.sendChatRooms())
            return
    def handleRequests(avatar:Player,name:str):
        if not (name in Server.players and name != avatar.name):
            avatar.sendMsg("Player not found")
            return
        avatar2:Player = Server.players[name]
        available = not avatar2.busy
        if not available or not avatar2.name in Server.serverRooms["Lobby"]:
            avatar.sendMsg("That player is currently in another room")
            return
        #This request appender to prevent other players from requesting this specific player
        avatar.busy = True
        avatar2.busy = True
        avatar.sendMsg("Sent fight request")
        print(f"{Server.getTime()} {avatar.name} requested to fight {avatar2.name}")
        avatar2.sendMsg(f"Would you want to fight {avatar.name} (y/n)?")
        avatar2.sendMsg(f"NOTIFY")
        try:
            if(avatar2.receiveMsg()=="y"):
                avatar.sendMsg("Player Confirmed")
                Server.gameRoom(avatar,avatar2) #this function can be replaced seamlessly
            else:
                print(f"{Server.getTime()} {avatar2.name} declined request")
                avatar2.sendMsg("Declined request")
                avatar2.sendMsg("You have declined the request")
                avatar.sendMsg("Declined request")
        except (ConnectionResetError,BrokenPipeError): #user left the applicaiton before accepting
            print("HERE NOW")
            pass
        avatar.busy = False
        avatar2.busy = False
    def handleAvatar(avatar:Player):
        while True:
            try:
                message = avatar.receiveMsg()
                try:
                    Server.handleCommands(avatar,message)
                except AttributeError as e:
                    pass
            #User leaves application normally
            except (ConnectionResetError,BrokenPipeError) as e:
                del Server.players[avatar.name]
                Server.roomCleanup(avatar)
                avatar.client.close()
                print(f"{Server.getTime()} {avatar.name} left the application")
                break
            #Unexpected error on the user side, or server side
            except Exception as e:
                del Server.players[avatar.name]
                traceback.print_exc()
                try:
                    x = str(e)
                    avatar.sendMsg(f"Restart Application, Fatal Error")
                except OSError:
                    pass
                Server.roomCleanup(avatar)
                avatar.client.close()
                print(f"{Server.getTime()} FATAL: {avatar.name} left the application")
                
                break
    def roomCleanup(avatar:Player):
        room = avatar.room
        avatar.room = None
        room.leave(avatar)
        room.refresh()
        with Server.lock:
            if room.roomType == "Lobby":
                room.broadcast(f"{Server.sendChatRooms()}\n{avatar.name} left the server")
            elif room.roomType == "Chat":
                print("Was in room")
                room.broadcast(f"{Server.sendChatRooms()}\n{avatar.name} unexpectedly left")   
            time.sleep(0.005)
    def gameRoom(player1: Player,player2: Player):
        #Creating room instances, as well as switching players to the designated rooms
        arenas = Server.serverRooms["Arenas"]
        lobby:Room = Server.serverRooms["Lobby"]
        lobby.leave(player1)
        lobby.leave(player2)
        arena: Arena = Arena(player1,player2)
        arena.refresh()
        arenas.append(arena)
        lobby.refresh()
        time.sleep(0.1)
        lobby.broadcast(Server.sendChatRooms())
        try:
            print(f"{Server.getTime()} Fight started between {player1.name} and {player2.name}")
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
            lobby.broadcast(Server.sendChatRooms())
            print(f"{Server.getTime()} Game ended")
        except KeyError:
            arenas.remove(arena)
            for x in arena:
                print(f"{arena[x].name} was freed from the fightRoom")
                lobby.addPlayer(arena[x])
            time.sleep(0.1)
            lobby.refresh()
            time.sleep(0.1)
            lobby.broadcast(Server.sendChatRooms())
            if player1.name not in arena:
                lobby.broadcast(f"\n{player1.name} quit\n")
            else:
                lobby.broadcast(f"\n{player2.name} quit\n")
            arena.removeAll()
    def adminCommands():
        if not Server.__initialized:
            print("Server not initialized")
            return
        while True:
            print("Menu Mode: \n(1) List all players\n(2) Send message to users\n(3) Kick a user\n")
            userinput = input(">")
            if userinput=="1":
                for key in Server.players:
                    print(f'{key} Busy status: {Server.players[key].busy}')
            elif userinput=="2":
                print("Announcement Mode")
                announcement = ""
                while True:
                    announcement = input()
                    if announcement == "exit":
                        break
                    Server.serverRooms["Lobby"].broadcast(announcement)
            elif userinput=="3":
                kicked = input("Kick who?\n>")
                if kicked in Server.players:
                    Server.players[kicked].sendMsg("You have been kicked by the admin")
                    Server.players[kicked].client.close()