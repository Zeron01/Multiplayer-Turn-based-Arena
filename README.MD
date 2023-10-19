
Make sure you have python 3.9.4+ to use the program

Multiplayer implementation of my old game
	- https://github.com/Zeron01/Singleplayer-Turn-Based-Arena

#### Settings:
- Default IP: 127.0.0.1
- Default Port: 25565
- Edit settings.txt to desired IP and ports if needed

#### How to run:
- run main.py
- If you want to auto-launch userSim and client, type 'y' in the prompts
- If you want to test the users fighting with the userSim
	- Enter "2" in the main.py window, this will allow for announcement mode
	- Enter "BEGIN" in the main.py window and the users will begin to force a battle
- You can manually launch userSim.py, and client.py, given that the server is running

#### Testing Multiplayer Commands

- ##### /fight
	- Open another client.py file 
	- Create the user
	- Once connected, enter /fight {username}
	- If the opposing user accepts, fight will begin
	- !! Need to be in lobby in order to request fights
	- Example:
		- username: bob
		- username: bill
			- If bob wants to fight bill
			- Bob would enter "/fight bill"
			- Bill would type 'y' once prompted "Would you want to fight bob"
			- Fight will begin once accepted
- ##### /spectate 
	- Requires an on-going fight, follow steps in /fight to do so, or follow userSim steps
	- If there's already a fight
	- User can enter "/spectate {Arena #}"
	- If they wish to leave the spectate, enter "/leave"
	- Example:
		- If there is an on-going game in Arena 1, a player would type "/spectate 1"
