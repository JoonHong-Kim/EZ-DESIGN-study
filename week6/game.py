BLACK = 1
WHITE = 2


class Omok:
    def __init__(self):
        self.board = [[0] * 19 for _ in range(19)]
        self.current_player = BLACK
        self.forbidden_moves = set()
        self.directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    def play(self, row, col):

        self.board[row][col] = self.current_player
        self.update_forbidden_moves()
        if self.check_win(row, col):
            return {
                "board": self.board,
                "forbidden_moves": self.forbidden_moves,
                "winner": self.current_player,
                "turn": -1,
            }

        self.current_player = 3 - self.current_player

        return {
            "board": self.board,
            "forbidden_moves": self.forbidden_moves,
            "winner": -1,
            "turn": self.current_player,
        }

    def check_win(self, row, col):
        for d in self.directions:
            count = 1
            for i in range(1, 6):
                r, c = row + d[0] * i, col + d[1] * i
                if (
                    0 <= r < 19
                    and 0 <= c < 19
                    and self.board[r][c] == self.current_player
                ):
                    count += 1
                else:
                    break

            for i in range(1, 6):
                r, c = row - d[0] * i, col - d[1] * i
                if (
                    0 <= r < 19
                    and 0 <= c < 19
                    and self.board[r][c] == self.current_player
                ):
                    count += 1
                else:
                    break

            if count == 5:
                return True

        return False

    def update_forbidden_moves(self):
        self.forbidden_moves = set()
        for row in range(19):
            for col in range(19):
                if self.board[row][col] == 0:
                    if self.is_forbidden_move(row, col):
                        self.forbidden_moves.add((row, col))

    def is_forbidden_move(self, row, col):
        if self.board[row][col] != 0:
            return False

        self.board[row][col] = 1

        if self.check_double_three(row, col) or self.check_double_four(row, col):
            self.board[row][col] = 0
            return True

        self.board[row][col] = 0
        return False

    def check_double_three(self, row, col):

        count = 0

        for d in self.directions:
            if self.check_open_three(row, col, d[0], d[1]):
                count += 1

        return count >= 2

    def check_double_four(self, row, col):

        count = 0

        for d in self.directions:
            if self.check_open_four(row, col, d[0], d[1]):
                count += 1

        return count >= 2

    def check_open_three(self, row, col, dx, dy):
        count = 1
        empty_count = 0

        for i in range(1, 4):
            r, c = row + dx * i, col + dy * i
            if 0 <= r < 19 and 0 <= c < 19:
                if self.board[r][c] == 1:
                    count += 1
                elif self.board[r][c] == 0:
                    empty_count += 1
                    break
            else:
                break

        for i in range(1, 4):
            r, c = row - dx * i, col - dy * i
            if 0 <= r < 19 and 0 <= c < 19:
                if self.board[r][c] == 1:
                    count += 1
                elif self.board[r][c] == 0:
                    empty_count += 1
                    break
            else:
                break

        return count == 3 and empty_count == 2

    def check_open_four(self, row, col, dx, dy):
        count = 1
        empty_count = 0

        for i in range(1, 5):
            r, c = row + dx * i, col + dy * i
            if 0 <= r < 19 and 0 <= c < 19:
                if self.board[r][c] == 1:
                    count += 1
                elif self.board[r][c] == 0:
                    empty_count += 1
                    break
            else:
                break

        for i in range(1, 5):
            r, c = row - dx * i, col - dy * i
            if 0 <= r < 19 and 0 <= c < 19:
                if self.board[r][c] == 1:
                    count += 1
                elif self.board[r][c] == 0:
                    empty_count += 1
                    break
            else:
                break

        return count == 4 and empty_count == 2
