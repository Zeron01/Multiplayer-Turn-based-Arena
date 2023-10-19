## Multiplayer Turn-based Arena
Make sure you have python 3.9.4+ to use the program

Multiplayer implementation of my old game
	- https://github.com/Zeron01/Singleplayer-Turn-Based-Arena

#### Settings:
- Default IP: 127.0.0.1
- Default Port: 25565
- Edit settings.txt to desired IP and ports if needed

#### How to run:
- Run main.py
- Once server is online, launch client.py
- Enter desired username
- You should have been able to connect to the server
- If not, adjust settings.txt to IP and ports available on system

#### Multiplayer Commands
- ##### /fight {username}
	- Able to fight other users in auto-turned based combat
	- To do so
		- Open another client.py file 
		- Create the user
		- Once connected, enter /fight {username}
		- If the opposing user accepts, fight willl begin
		- !! Need to be in lobby in order to request fights
		- Example:
			- username: bob
			- username: bill
				- If bob wants to fight billl
				- Bob would enter "/fight bill"
				- Bill would type 'y' once prompted "Would you want to fight bob"
				- Fight will begin once accepted
- ##### /spectate {Arena #}
	- Able to spectate other people fighting
	- To do so:
		- Requires an on-going fight, follow steps in /fight to do so, or follow userSim steps
		- User can enter "/spectate {Arena #}"
		- If they wish to leave the spectate, enter "/leave"
		- Example:
			- If there is an on-going game in Arena 1, a player would type "/spectate 1"
- ##### /list
	- Lists all the lobby rooms
- ##### /leaderboards
	- Lists the player leaderboards
- ##### /profile
	- List your profile, and user stats
- ##### /join {Room #}
	- Join a chatroom listed in the lobby
- ##### /leave
	- If in a chatroom, or in a arena; go back to lobby

#### Automatic Battles
- Without having to launch multiple client.py files,  launch the userSim.py file while the server is running
- Once done, a bunch of bots would join the server
- If you wish the bots to fight against each other
	- Enter "2" in the main.py window (announcement mode)
	- Enter "BEGIN" in the main.py window
	- Bots will then force a battle
	- Enter "exit" in main.py to leave announcement mode
	- Suggested to have at least one client in the server in order to view the arenas getting populated
