from classes.Player import Player
import threading
class Room:
    #Operator Overloading
    def __init__(self,roomType):
        self.players: dict = {}
        self.logs: str = ""
        self.roomType = roomType
        self.lock = threading.Lock()
        self.recent = ""
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
    #End of overload
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
        if self.recent == message and not save:
            return
        self.recent = message
        if save:
            self.logs += message +"\n"
        kicked = []
        with self.lock:
            for key in self:
                try:
                    self[key].sendMsg(message)
                except OSError:
                    #If the client is no longer connected, disonnect them from the room
                    kicked.append(key)
    def addPlayer(self,avatar: Player):
        with self.lock:
            self.players[avatar.name] = avatar
        avatar.room = self
    def leave(self,avatar: Player):
        with self.lock:
            try:
                del self.players[avatar.name]
            except KeyError:
                pass
    def refresh(self):
        with self.lock:
            for key in self:
                    try:
                        self[key].sendMsg("Clear")
                    except ConnectionResetError:
                        continue
    def removeAll(self):
        self.players.clear()