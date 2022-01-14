import random
class Dialogue:
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