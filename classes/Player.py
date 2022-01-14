import random
from typing import Tuple
import socket
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
        from classes.Room import Room
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
    def attack(self,other:'Player')->Tuple[int,bool,bool]: #damage, critical, dodge
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
        text += (f"Profile: {self.name}\n\nLevel: {Player.formatComma(self.level)}\nHealth: {Player.formatComma(self.health)}/{Player.formatComma(self.maxHealth)}\nDefense: {Player.formatComma(self.defense)}\nExp: {Player.formatComma(self.exp)}/{Player.formatComma(self.expMax)}\nWins: {Player.formatComma(self.wins)}\nInventory: [")
        text+=']\n'
        if not self.alive():
            deadtext = (f"\nStatus: Dead")
            text+=deadtext
        else:
            alivetext = (f"\nStatus: Alive")
            text+=alivetext
        text+=("\n------------------------------")
        return text
    def formatComma(number) -> str:
        return "{:,}".format(number)