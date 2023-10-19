Make sure you have python 3.9.4+ to use the program <br />
<br />
Multiplayer implementation of my old game.<br />
<br />
If you want to see the old version in singleplayer: https://github.com/Zeron01/Singleplayer-Turn-Based-Arena<br />
<br />
<br />
Settings:<br />
<br />
    * Default IP: 127.0.0.1<br />
    * Default Port: 25565<br />
    * If need to be changed if the following are not available:<br />
    * edit settings.txt to the IP and ports you want<br />
<br />
How to run:<br />
  -run main.py<br />
  -If you want to auto-launch the userSim and client, type 'y' in the prompts<br />
  -If you wish to test the users fighting with the userSim<br />
      1) Enter "2" in the main.py window, this will allow for announcement mode<br />
      2) Enter "BEGIN" in the main.py window and the users will begin to force a battle<br />
<br />
  If you do not want to auto-launch the userSim and client, type 'n' for both prompts<br />
    You can manually launch userSim.py and client.py as long as the server is running<br />
  Use /help once logged in on the server in the client.py window<br /> <br />
Testing multiplayer commands:<br /> <br />
  ---To test the /fight command--- <br />
    (1) Open another client.py file<br /> 
    (2) Create another user<br />
    (3) Once that's connected to the server, enter /fight, hit enter<br />
    (4) Then a prompt will ask you who you want to fight. Enter the user you would want<br />
    (5) To fight, and if they accept the request, the fight will begin.<br /> 
    (!) You would need to be in the lobby to request any fights<br />
Example of /fight:<br />
--username: bob<br />
--username: bill<br />
      --If bob wants to fight bill <br />
      --bob would enter "/fight bill" <br />
      --bill on his screen would see:"Would you want to fight bob (y/n)"<br />
      --Based on bill's response, the fight will either begin, or not<br /><br />
    
  To test the /spectate,<br />
    There has to already be an ongoing fight with two users while there is a fight on-going, the user can enter "/spectate {Arena #}". <br />
    If the user wishes to leave, they can enter /leave and return to the lobby.<br />
    Ex: If there is an ongoing game in arena 1, a player would have to type "/spectate 1"<br />
