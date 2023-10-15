
from typing import IO, Tuple
def retrieveHostPort() -> Tuple[str,str]:
        try:
            fh = open('settings.txt')
        except IOError:
            raise IOError
        content = fh.readlines()
        fh.close()
        try:
            host = content[0][4:].rstrip("\n")
            port = content[1][6:].rstrip("\n")
            #Successful file read
            return host,port
        except IndexError:
            raise IndexError

def updateHostPort(host:str="127.0.0.1",port:str="25565"):
    try:
        fh = open('settings.txt','w')
    except IOError:
        print("Error: Failed to open file")
        return -1
    fh.write(f"IP: {host}\nPORT: {str(port)}")
    fh.close()
    return 1