import copy
import pickle
import socket

from game import Omok

BLACK = 1
WHITE = 2


class Server:
    def __init__(self, host="localhost", port=12345):
        self.host = host
        self.port = port
        self.socket = None
        self.clients = []
        self.game = None
        self.replay = []

    def setup_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)
        print(f"Server started on {self.host}:{self.port}")

    def setup_game(self):
        self.game = Omok()

    def handle_clients(self):
        turn = 0
        while True:
            try:
                data = self.clients[turn].recv(1024)
                if not data:
                    print("no data")
                    break
                data = pickle.loads(data)
                row, col = data
                result = copy.deepcopy(self.game.play(row, col))
                self.replay.append(result)
                response = pickle.dumps(result)
                for client_socket in self.clients:
                    client_socket.send(response)
                if result["winner"] != -1:
                    if result["winner"] == BLACK:
                        print("Black player wins!")
                    elif result["winner"] == WHITE:
                        print("White player wins!")
                    break

                turn = 1 - turn
            except ConnectionResetError:
                print("Client disconnected")
                break

        for client_socket in self.clients:
            replay_data = pickle.dumps(self.replay)
            client_socket.send(replay_data)
            client_socket.recv(1024)
            client_socket.close()

    def run(self):
        self.setup_socket()
        self.setup_game()
        print("Waiting for clients...")
        color = BLACK
        init_data = {
            "board": self.game.board,
            "forbidden_moves": self.game.forbidden_moves,
            "winner": -1,
            "turn": 1,
            "color": color,
        }
        while len(self.clients) < 2:
            client_socket, client_address = self.socket.accept()
            print(f"Client {client_address} connected")
            client_socket.send(pickle.dumps(init_data))
            self.clients.append(client_socket)

            init_data["color"] = WHITE
        print("Game started")
        self.handle_clients()


if __name__ == "__main__":
    server = Server()
    server.run()
