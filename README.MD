Make sure you have python 3.9.4+ to use the program <br />
<br />
Multiplayer implementation of my old game.<br />
<br />
If you want to see the old version in singleplayer: https://github.com/Zeron01/Singleplayer-Turn-Based-Arena<br />
<br />
<br />
Settings:<br />
<br />
&emsp;Default IP: 127.0.0.1<br />
&emsp;Default Port: 25565<br />
&emsp;If need to be changed if the following are not available:<br />
&emsp;edit settings.txt to the IP and ports you want<br />
<br />
How to run:<br />
&emsp;run main.py<br />
&emsp;If you want to auto-launch the userSim and client, type 'y' in the prompts<br />
&emsp;&emsp; Will launch a client window where the user will interact, and the userSim console to populate the server<br />
&emsp;&emsp;If you wish to test the users fighting with the userSim<br />
&emsp;&emsp;&emsp;1) Enter "2" in the main.py window, this will allow for announcement mode<br />
&emsp;&emsp;&emsp;2) Enter "BEGIN" in the main.py window and the users will begin to force a battle<br />
<br />
&emsp;If you do not want to auto-launch the userSim and client, type 'n' for both prompts<br />
&emsp;&emsp;You can manually launch userSim.py and client.py as long as the server is running<br />
&emsp;Use /help once logged in on the server in the client.py window<br />
Testing multiplayer commands:<br />
&emsp;To test the /fight command, <br />
&emsp;&emsp;(1) Open another client.py file<br /> 
&emsp;&emsp;(2) Create another user<br />
&emsp;&emsp;(3) Once that's connected to the server, enter /fight, hit enter<br />
&emsp;&emsp;(4) Then a prompt will ask you who you want to fight. Enter the user you would want<br />
&emsp;&emsp;(5) To fight, and if they accept the request, the fight will begin.<br /> 
&emsp;&emsp;(!) You would need to be in the lobby to request any fights, you are unable to start a fight within the chatrooms/spectate rooms. <br />
&emsp;&emsp;Example of /fight:<br />
&emsp;&emsp;&emsp;username: bob<br />
&emsp;&emsp;&emsp;username: bill<br />
&emsp;&emsp;&emsp;If bob wants to fight bill, bob would enter "/fight bill" <br />
&emsp;&emsp;&emsp;bill on his screen would see:"Would you want to fight bob (y/n)"<br />
&emsp;&emsp;&emsp;Based on bill's response, the fight will either begin, or not<br />
    
&emsp;To test the /spectate,<br />
&emsp;&emsp;There has to already be an ongoing fight with two users while there is a fight on-going, the user can enter "/spectate {Arena #}". <br />
&emsp;&emsp;If the user wishes to leave, they can enter /leave and return to the lobby.<br />
&emsp;&emsp;Ex: If there is an ongoing game in arena 1, a player would have to type "/spectate 1"<br />
