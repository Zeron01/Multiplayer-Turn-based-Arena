Make sure you have python 3.9.4+ to use the program

Settings:

Default IP: 127.0.0.1
Default Port: 25565
If need to be changed if the following are not available:
- edit settings.txt to the IP and ports you want

How to run:
- run main.py

Instructions to play:
- Once you run the client.py file, you will be asked to enter a username,
  enter a username, and if the server is set up properly, you will be connected
  to the server. 

- When you first connect to the server, you can use the /help command
  to get a list of commands that are possible within the server. You are
  able to test the majority of the commands on a single user, but for the fight
  and spectate commands, there would need to be at least 2 users in the 
  server to request a fight.

Testing multiplayer commands:
    - To test the /fight command, 
        Open another client.py file, create another user,
        once that's connected to the server, enter /fight, hit enter
        then a prompt will ask you who you would like to fight. Enter the user you would want
        to fight, and if they accept the request, the fight will begin. Also one more condition,
        you would need to be in the lobby to request any fights, you are unable to start a fight
        within the chatrooms/spectate rooms. 

        Example of /fight:
            username: Bob
            username: Billy

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
