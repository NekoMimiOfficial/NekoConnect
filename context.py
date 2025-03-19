"""
typesetting example for the context object
"""

class ctx:
    def __init__(self):
        self.op: int
        self.data: bytes
        self.len= len(self.data)

    def recv(self, packets: int)-> bytes:
        return bytes()

    def send(self, data: bytes)-> None:
        return

    def close(self)-> None:
        return

    def db_get(self, cell: str)-> str:
        return str()

    def db_store(self, cell: str, data: str)-> bool:
        return bool()

    def warn(self, message: str)-> None:
        return

    def error(self, message: str)-> None:
        return
