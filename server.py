import socket
import random
import multiprocessing

def randstr_gen(str_len= 8)-> str:
    hexassert= "123ab456cde789f0"
    result= ""

    for j in range(str_len):
        result= result + random.choice(hexassert)

    return result

class Packet:
    def __init__(self):
        self.packet_len: bytes        #4 bytes
        self.opcode_len: bytes        #1 byte
        self.greeter_len: bytes       #1 byte
        self.data_len: bytes          #4 bytes
        self.hash_len: bytes          #1 byte
        self.randstr_len: bytes       #1 byte
        self.greeter: bytes
        self.opcode: bytes
        self.randstr: bytes
        self.data: bytes
        self.hash: bytes

        self.r_greeter: str
        self.r_opcode: int
        self.r_randstr: str
        self.r_hash: str

class Server:
    def __init__(self, port):
        self.host= "0.0.0.0"
        self.port= port
        self.server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bound= False
        self.running= False

    def handler(self):
        while True:
            conn, addr= self.server.accept()
            fail_request= Packet()
            fail_request.greeter= "nekoconnect-server".encode()
            fail_request.opcode= int(400).to_bytes(1)
            fail_request.randstr= randstr_gen().encode()
            fail_request.data= int(400).to_bytes(1)
            fail_request.opcode_len= int(1).to_bytes(1)
            fail_request.greeter_len= int(1).to_bytes(1)
            fail_request.data_len= int(1).to_bytes(4)

    def bind(self):
        self.server.bind((self.host, self.port))
        self.bound= True

    def run(self):
        if self.bound and not self.running:
            mp= multiprocessing.Process(target=self.handler)
            mp.start()

if __name__ == '__main__':
    print(randstr_gen(8))
