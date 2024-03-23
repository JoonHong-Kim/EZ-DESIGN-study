import pickle
import socket


class Client:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def receive(self):
        print("waiting for data")
        receive = self.socket.recv(16384)
        print("received data")
        return pickle.loads(receive)

    def send(self, data):
        self.socket.send(pickle.dumps(data))
