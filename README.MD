Make sure you have python 3.9.4+ to use the program <br />
<br />
Multiplayer implementation of my old game.<br />
<br />
If you want to see the old version in singleplayer: https://github.com/Zeron01/Singleplayer-Turn-Based-Arena<br />
<br />
Settings:<br />
<br />
Default IP: 127.0.0.1<br />
Default Port: 25565<br />
If need to be changed if the following are not available:<br />
- edit settings.txt to the IP and ports you want<br />
<br />
How to run:<br />
    - run main.py<br />
    - If you want to auto launch the userSim and client, type 'y' in the prompts<br />
        - Will launch a client window where the user will interact, and the userSim console to populate the server<br />
        - If you wish to test the users fighting with the userSim<br />
            1) Enter "2" in the main.py window, this will allow for announcement mode<br />
            2) Enter "BEGIN" in the main.py window and the users will begin to eventually force a battle<br />
<br />
    - If you do not want to auto launch the userSim and client, type 'n' for both prompts<br />
        - You can manually launch userSim.py and client.py as long as the server is running<br />
    - Use /help once logged in on the server in the client.py window<br />
Testing multiplayer commands:<br />
    - To test the /fight command, <br />
        Open another client.py file, create another user,<br />
        once that's connected to the server, enter /fight, hit enter<br />
        then a prompt will ask you who you would like to fight. Enter the user you would want<br />
        to fight, and if they accept the request, the fight will begin. Also one more condition,<br />
        you would need to be in the lobby to request any fights, you are unable to start a fight<br />
        within the chatrooms/spectate rooms. <br />
<br />
        Example of /fight:<br />
            username: bob<br />
            username: bill<br />
<br />
            If bob wants to fight bill, bob would enter "/fight bill"<br />
<br />            
            bill on his screen would see:<br />
                Would you want to fight bob (y/n)<br />
<br />
            Based on bill's response, the fight will either begin, or not<br />
<br />
    - To test the /spectate,<br />
        There has to already be an on-going fight with two users,<br />
        while there is a fight on-going, the user can enter "/spectate {Arena #}". From there, they will be able to watch the fight.<br />
        If the user wishes to leave, they can enter /leave and return to the lobby.<br />
        Ex: If there is an on-going game in arena 1, a player would have to type<br />
        /spectate 1<br />
