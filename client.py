import socket
import random

def randStr()-> str:
    base= "123456abcedfXYZQKS7890!#?&$"
    git= ""
    for i in range(6):
        git= git + base[random.randint(0, len(base)-1)]

    return git

def crypt(inp: str, salt: str, passwd: str)-> str:
    wp= salt+passwd
    table_let= "abcdefghijklmnopqrstuvwxyz"
    table_num= "1234567890"
    table_upp= table_let.upper()
    table_sym= "~!@#$%^&*()_+-=[]{};':\",.<>/?\\|`"
    table= table_let+table_num+table_upp+table_sym
    objects= []
    onjects =[]
    i= 0

    for c in inp:
        j= 0
        if not c in table:
            onjects.append(127)
            continue

        for x in table:
            if x == c:
                onjects.append(j)

            j= j + 1


    for c in wp:
        j= 0
        if not c in table:
            objects.append(127)
            continue

        for x in table:
            if x == c:
                objects.append(j)

            j= j + 1

    for o in onjects:
        onjects[i]= o + objects[i]
        i= i + 1

    table= table + table_sym + table + table_upp + table_sym + table_upp + table + table + "uwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwu"
    string_of_doom= ""
    for w in onjects:
        string_of_doom= string_of_doom + table[w]

    return string_of_doom

class Client:
    def __init__(self, port, auth)-> None:
        self.host= '0.0.0.0'
        self.port= port
        self.auth= auth
        self.connection: socket.socket

    def connect(self)-> int:
        self.connection= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.host, self.port))

        greet= randStr()
        self.connection.send(len(greet).to_bytes(4))
        g_l= self.connection.recv(len(greet))
        if not int().from_bytes(g_l) == len(greet):
            return 504
        self.connection.send(greet.encode())
        read_rand= self.connection.recv(4)
        self.connection.send(read_rand)
        ranmom= self.connection.recv(int().from_bytes(read_rand))
        encshion= crypt(ranmom.decode(), greet, self.auth)
        self.connection.send(len(encshion).to_bytes(4))
        enc_l= self.connection.recv(4)
        if not int().from_bytes(enc_l) == len(encshion):
            return 504
        self.connection.send(encshion.encode())
        resp= self.connection.recv(4)

        return int().from_bytes(resp)

    def disconnect(self)-> None:
        self.connection.close()

if __name__ == '__main__':
    cli= Client(10390, "balls")
    print(cli.connect())
