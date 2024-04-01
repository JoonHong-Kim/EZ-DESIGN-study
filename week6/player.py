import pickle

import pygame
from client import Client

BLACK = 1
WHITE = 2
BACKGROUND = "images/board.jpg"
BOARD_SIZE = (820, 820)


class Player:
    board = [[0] * 19 for _ in range(19)]
    forbidden_moves = None
    winner = None
    turn = None
    color = None

    def __init__(self, client):
        self.client = client
        self.init_pygame()
        self._draw_board()

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Omok")
        self.screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
        self.background = pygame.image.load(BACKGROUND).convert()
        self.clickable = False

    def _draw_board(self):
        outline = pygame.Rect(45, 45, 720, 720)
        pygame.draw.rect(self.background, BLACK, outline, 3)
        outline.inflate_ip(20, 20)
        for i in range(18):
            for j in range(18):
                rect = pygame.Rect(45 + (40 * i), 45 + (40 * j), 40, 40)
                pygame.draw.rect(self.background, BLACK, rect, 1)
        for i in range(3):
            for j in range(3):
                coords = (165 + (240 * i), 165 + (240 * j))
                pygame.draw.circle(self.background, BLACK, coords, 5, 0)
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    def _draw_stone(self, row, col, color):
        coords = (45 + col * 40, 45 + row * 40)
        if color == BLACK:
            color_value = (0, 0, 0)
        else:
            color_value = (255, 255, 255)
        pygame.draw.circle(self.screen, color_value, coords, 20, 0)
        pygame.display.update()

    def _draw_forbidden_mark(self):
        for row, col in self.forbidden_moves:
            coords = (45 + col * 40, 45 + row * 40)
            x, y = coords
            offset = 15  # X의 크기를 조절하는 값
            pygame.draw.line(
                self.screen,
                (255, 0, 0),
                (x - offset, y - offset),
                (x + offset, y + offset),
                3,
            )
            pygame.draw.line(
                self.screen,
                (255, 0, 0),
                (x - offset, y + offset),
                (x + offset, y - offset),
                3,
            )
            pygame.display.update()

    def _draw_omok(self):
        self._draw_board()
        self._draw_forbidden_mark()
        for row in range(19):
            for col in range(19):
                if self.board[row][col] != 0:
                    self._draw_stone(row, col, self.board[row][col])

    def _update(self, board, forbidden_moves, winner, turn):
        self.board = board
        self.forbidden_moves = forbidden_moves
        self._draw_omok()
        self.turn = turn
        self.winner = winner

    def _receive_data(self):
        data = self.client.receive()
        print(data)
        if data.get("color"):
            self.color = data["color"]
        self._update(
            data["board"], data["forbidden_moves"], data["winner"], data["turn"],
        )
        if self.winner != -1:
            self._draw_win()
            return True
        return False

    def _draw_win(self):
        font = pygame.font.Font(None, 36)
        if self.winner == -1:
            return
        if self.winner == self.color:
            text = font.render("You Win", True, (0, 0, 0))
        else:
            text = font.render("You Lose", True, (0, 0, 0))
        text_rect = text.get_rect(centerx=self.screen.get_width() // 2, top=50)
        box_width = text_rect.width + 20
        box_height = text_rect.height + 20
        box_rect = pygame.Rect(0, 0, box_width, box_height)
        box_rect.center = (self.screen.get_width() // 2, text_rect.centery)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect)
        self.screen.blit(text, text_rect)
        pygame.display.update()
        # pygame.time.wait(10000)

    def run(self):
        clickable = False
        while True:
            if not clickable:
                try:
                    is_terminated = self._receive_data()
                    clickable = self.turn == self.color
                    if is_terminated:
                        break
                except ConnectionError:
                    break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if not clickable:
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row = int(round(((y - 45) / 40.0), 0))
                    col = int(round(((x - 45) / 40.0), 0))
                    if not (0 <= row < 19 and 0 <= col < 19):
                        break
                    if self.board[row][col] != 0:
                        break
                    if self.color == BLACK and (row, col) in self.forbidden_moves:
                        break
                    self.client.send((row, col))
                    clickable = False

        replay = self.client.receive()
        if replay:
            pickle.dump(replay, open("replay.pkl", "wb"))
            self.client.send("ack")


if __name__ == "__main__":
    server_host = "localhost"
    server_port = 12345
    client = Client(server_host, server_port)
    player = Player(client)
    player.run()
