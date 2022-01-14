import time
from classes.Player import Player
from classes.Room import Room
from classes.Dialogue import Dialogue
class Arena(Room):
    def __init__(self,player1:Player,player2:Player):
        super().__init__("Arena")
        self.player1:Player = player1
        self.player2:Player = player2
        self.addPlayer(player1)
        self.addPlayer(player2)
    def displayRoom(self) -> str:
        if len(self)==0:
            return "Current Occuptants: No one"
        else:
            message = "Current Occuptants:\n"
            for key in self:
                message+=">"+key
                if key != self.player1.name and key != self.player2.name:
                    message+=" (Spectating)"
                message+="\n"
            return message
    def combat(self)->None:
        fighter1 = self.player1.name
        fighter2 = self.player2.name
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
                    arena.broadcast(f'{fighter}: {Dialogue.criticalQuotes()}')
                    time.sleep(0.2)
                if dodge:
                    arena.broadcast(f'{opponent}: {Dialogue.dodgeQuotes()}')
                    time.sleep(0.2)
                    arena.broadcast(f'{opponent} dodges a{Dialogue.criticalCheck(critical)} strike from {fighter}\n')
                    time.sleep(0.2)
                else:
                    arena.broadcast(f'[{Player.formatComma(arena[fighter].health)}/{Player.formatComma(arena[fighter].maxHealth)} HP] {fighter} deals {Player.formatComma(damage)}{Dialogue.criticalCheck(critical)} damage to {opponent} [{Player.formatComma(arena[opponent].health)}/{Player.formatComma(arena[opponent].maxHealth)} HP]\n')
                    time.sleep(0.2)
                    arena[opponent].health-=damage
                time.sleep(1)
                if not arena[opponent].alive():
                    #Don't level up for now
                    #expGained, levelup = arena[fighter].killed(arena[opponent])
                    arena[fighter].wins+=1
                    arena.broadcast(f'\n{opponent}: {Dialogue.deathQuotes()}')
                    time.sleep(0.1)
                    arena.broadcast(f'{opponent} has fallen')
                    break
                opponent = fighter1
            turn+=1