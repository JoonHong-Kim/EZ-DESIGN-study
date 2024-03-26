import pickle

import pygame

BLACK = 1
WHITE = 2
BACKGROUND = "images/board.jpg"
BOARD_SIZE = (820, 820)


class Replay:
    def __init__(self, path):
        with open(path, "rb") as f:
            self.data = pickle.load(f)
        self.pointer = 0
        self.init_pygame()
        self._draw_board()

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Omok")
        self.screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
        self.background = pygame.image.load(BACKGROUND).convert()

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

    def _update(self):
        status = self.data[self.pointer]
        self.board = status["board"]
        self.forbidden_moves = status["forbidden_moves"]

    def run(self):
        self._update()
        self._draw_omok()

        while True:
            pygame.time.wait(250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                # 키보드 좌우 방향으로 포인터 이동
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.pointer = max(0, self.pointer - 1)
                    elif event.key == pygame.K_RIGHT:
                        self.pointer = min(len(self.data) - 1, self.pointer + 1)
                    self._update()
                    self._draw_omok()


if __name__ == "__main__":
    replay = Replay("replay.pkl")
    replay.run()
