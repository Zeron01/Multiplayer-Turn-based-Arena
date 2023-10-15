Make sure you have python 3.9.4+ to use the program

Multiplayer implementation of my old game
If you want to see the old version in singleplayer: https://github.com/Zeron01/Singleplayer-Turn-Based-Arena

Settings:

Default IP: 127.0.0.1
Default Port: 25565
If need to be changed if the following are not available:
- edit settings.txt to the IP and ports you want

How to run:
    - run main.py
    - If you want to auto launch the userSim and client, type 'y' in the prompts
        - Will launch a client window where the user will interact, and the userSim console to populate the server
        - If you wish to test the users fighting with the userSim
            1) Enter "2" in the main.py window, this will allow for announcement mode
            2) Enter "BEGIN" in the main.py window and the users will begin to eventually force a battle

    - If you do not want to auto launch the userSim and client, type 'n' for both prompts
        - You can manually launch userSim.py and client.py as long as the server is running
    - Use /help once logged in on the server in the client.py window
Testing multiplayer commands:
    - To test the /fight command, 
        Open another client.py file, create another user,
        once that's connected to the server, enter /fight, hit enter
        then a prompt will ask you who you would like to fight. Enter the user you would want
        to fight, and if they accept the request, the fight will begin. Also one more condition,
        you would need to be in the lobby to request any fights, you are unable to start a fight
        within the chatrooms/spectate rooms. 

        Example of /fight:
            username: bob
            username: bill

            If bob wants to fight bill, bob would enter "/fight bill"
            
            bill on his screen would see:
                Would you want to fight bob (y/n)

            Based on bill's response, the fight will either begin, or not

    - To test the /spectate,
        There has to already be an on-going fight with two users,
        while there is a fight on-going, the user can enter "/spectate {Arena #}". From there, they will be able to watch the fight.
        If the user wishes to leave, they can enter /leave and return to the lobby.
        Ex: If there is an on-going game in arena 1, a player would have to type
        /spectate 1
