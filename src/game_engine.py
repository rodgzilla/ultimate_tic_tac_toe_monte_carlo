import unittest

        # self.board = [[[[None, None, None], [None, None, None], [0, None, None]],
        #                1,
        #                [[None, None, None], [None, None, None], [None, 1, None]]],
        #               [[[0, None, None], [None, None, None], [None, None, None]],
        #                [[None, None, None], [None, None, None], [None, None, None]],
        #                0],
        #               [[[None, None, None], [None, None, None], [None, None, None]],
        #                [[None, None, None], [None, None, None], [None, None, None]],
        #                [[0, None, None], [None, None, None], [None, None, None]]]]

class GameState():
    def __init__(self):
        self.player = 0
        self.board = [
            [
                [
                    [None] * 3        # line of small grid
                    for _ in range(3) # small grid
                ] for _ in range(3)   # line of big grid
            ] for _ in range(3)       # big grid
        ]
        self.possible_moves = {
            (grid_x, grid_y, cell_x, cell_y)
            for grid_x in range(3)
            for grid_y in range(3)
            for cell_x in range(3)
            for cell_y in range(3)
        }
        self.finished    = False
        self.move_number = 0
        self.winner      = None

    def _check_victory(self, grid_x, grid_y, cell_x, cell_y):
        board  = self.board[grid_x][grid_y]
        player = board[cell_x][cell_y]

        if all(board[cell_x][i] == player for i in range(3)) or \
           all(board[i][cell_y] == player for i in range(3)) or \
           all(board[i][i]      == player for i in range(3)) or \
           all(board[i][2 - i]  == player for i in range(3)):
            return True

        return False

    def _check_finished(self, grid_x, grid_y):
        player = self.board[grid_x][grid_y]

        if all(self.board[grid_x][i] == player for i in range(3)) or \
           all(self.board[i][grid_y] == player for i in range(3)) or \
           all(self.board[i][i]      == player for i in range(3)) or \
           all(self.board[i][2 - i]  == player for i in range(3)):
            return True

        return False

    def _update_possible_moves(self, grid_x, grid_y):
        self.possible_moves = set()
        if isinstance(self.board[grid_x][grid_y], int) or \
           all(self.board[grid_x][grid_y][cell_x][cell_y] is not None
               for cell_x in range(3)
               for cell_y in range(3)):
            for g_x in range(3):
                for g_y in range(3):
                    if isinstance(self.board[g_x][g_y], int):
                        continue
                    for cell_x in range(3):
                        for cell_y in range(3):
                            if self.board[g_x][g_y][cell_x][cell_y] is None:
                                self.possible_moves.add((g_x, g_y, cell_x, cell_y))
        else:
            for cell_x in range(3):
                for cell_y in range(3):
                    self.possible_moves.add((grid_x, grid_y, cell_x, cell_y))


    def play(self, grid_x, grid_y, cell_x, cell_y):
        if self.finished:
            raise ValueError('Game is already finished.')

        if not (grid_x, grid_y, cell_x, cell_y) in self.possible_moves:
            raise ValueError(f'{(grid_x, grid_y, cell_x, cell_y)} is not '
                             'a possible move on this board')

        if not (0 <= grid_x <= 2) or \
           not (0 <= grid_y <= 2) or \
           not (0 <= cell_x <= 2) or \
           not (0 <= cell_y <= 2):
            raise ValueError('Coordinates must be in [0, 1, 2].')

        if isinstance(self.board[grid_x][grid_y], int):
            raise ValueError('Not possible to play in won grid.')

        if self.board[grid_x][grid_y][cell_x][cell_y] is not None:
            raise ValueError('Cell already occupied.')

        self.board[grid_x][grid_y][cell_x][cell_y] = self.player
        self.move_number += 1

        if self._check_victory(grid_x, grid_y, cell_x, cell_y):
            self.board[grid_x][grid_y] = self.player
            if self._check_finished(grid_x, grid_y):
                self.finished = True
                self.winner = self.player
            if self.move_number == 89:
                self.finished = True

        if not self.finished:
            self._update_possible_moves(cell_x, cell_y)

        self.player = 1 - self.player

    def get_possible_next_move(self):
        return self.possible_moves

    def is_finished(self):
        return self.finished

    def get_winner(self):
        return self.winner

    def __repr__(self):
        print_mapping = {
            0    : 'X',
            1    : 'O',
            None : ' '
        }
        repr_lines = [
            f'Next player: {self.player}',
            '-' * 13
        ]
        for big_grid_line in self.board:
            line_repr = [['|'] for _ in range(3)]
            for small_grid in big_grid_line:
                if isinstance(small_grid, int):
                    line_repr[0].append('###|')
                    line_repr[1].append(f'#{print_mapping[small_grid]}#|')
                    line_repr[2].append('###|')
                else:
                    for line_idx, small_grid_line in enumerate(small_grid):
                        for cell in small_grid_line:
                            line_repr[line_idx].append(print_mapping[cell])
                        line_repr[line_idx].append('|')
            repr_lines.extend(''.join(line) for line in line_repr)
            repr_lines.append('-' * 13)

        return '\n'.join(repr_lines)

class TestGameEngine(unittest.TestCase):
    def test_play(self):
        state = GameState()
        with self.assertRaises(ValueError):
            state.play(-5, 0, 10, 15)

        self.assertEqual(state.player, 0)
        state.play(0, 0, 0, 0)
        self.assertEqual(state.player, 1)

        with self.assertRaises(ValueError):
            state.play(0, 0, 0, 0)

        with self.assertRaises(ValueError):
            state.play(2, 2, 2, 2)

        moves = [
            (0, 0, 0, 1),
            (0, 1, 0, 0),
            (0, 0, 1, 1),
            (1, 1, 0, 0),
            (0, 0, 2, 1),
            (2, 1, 0, 0),
        ]

        for move in moves:
            state.play(*move)

        with self.assertRaises(ValueError):
            state.play(0, 0, 2, 2)

    def test_get_possible_next_move_initial(self):
        state          = GameState()
        possible_moves = {
            (grid_x, grid_y, cell_x, cell_y)
            for grid_x in range(3)
            for grid_y in range(3)
            for cell_x in range(3)
            for cell_y in range(3)
        }
        self.assertEqual(
            state.get_possible_next_move(),
            possible_moves
        )

    def test_get_possible_next_move_single_grid(self):
        state = GameState()
        state.play(0, 0, 0, 0)
        possible_moves = {
            (0, 0, x, y)
            for x in range(3)
            for y in range(3)
            if not (x == 0 and y == 0)
        }
        self.assertEqual(
            state.get_possible_next_move(),
            possible_moves
        )
        state.play(0, 0, 0, 1)
        possible_moves = {
            (0, 1, x, y)
            for x in range(3)
            for y in range(3)
        }
        self.assertEqual(
            state.get_possible_next_move(),
            possible_moves
        )

    def test_get_possible_next_move_multi_grid(self):
        # We fill the top left cell as quickly as possible and then
        # play a top left cell in a small grid to allow the opponent
        # to play anywhere on the board.
        moves = [
            (0, 0, 0, 0),
            (0, 0, 0, 1),
            (0, 1, 0, 0),
            (0, 0, 1, 1),
            (1, 1, 0, 0),
            (0, 0, 2, 1),
            (2, 1, 0, 0),
        ]

        # Create the board and play the moves.
        state = GameState()
        for move in moves:
            state.play(*move)

        all_moves = {
            (grid_x, grid_y, cell_x, cell_y)
            for grid_x in range(3)
            for grid_y in range(3)
            for cell_x in range(3)
            for cell_y in range(3)
        }
        impossible_moves = {
            # cells in the top left cell
            (0, 0, 0, 0),
            (0, 0, 0, 1),
            (0, 0, 0, 2),
            (0, 0, 1, 0),
            (0, 0, 1, 1),
            (0, 0, 1, 2),
            (0, 0, 2, 0),
            (0, 0, 2, 1),
            (0, 0, 2, 2),
            # cells already filled
            (0, 1, 0, 0),
            (1, 1, 0, 0),
            (2, 1, 0, 0),
        }

        possible_moves = all_moves - impossible_moves
        self.assertEqual(
            state.get_possible_next_move(),
            possible_moves
        )

    def test_is_finished(self):
        # We finish the game quickly and check during the completion
        # and after the last move whether the game state indicates
        # finished or not.
        state = GameState()
        self.assertFalse(state.is_finished())
        moves = [
            (0, 0, 0, 0),
            (0, 0, 0, 1),
            (0, 1, 1, 1),
            (1, 1, 0, 0),
            (0, 0, 1, 1),
            (1, 1, 0, 1),
            (0, 1, 0, 1),
            (0, 1, 0, 2),
            (0, 2, 0, 2),
            (0, 2, 0, 1),
            (0, 1, 2, 1),
            (2, 1, 0, 0),
            (0, 0, 2, 2),
            (2, 2, 0, 2),
            (0, 2, 1, 1),
            (1, 1, 0, 2),
            (0, 2, 2, 0)
        ]

        for move in moves[:6]:
            state.play(*move)

        self.assertFalse(state.is_finished())

        for move in moves[6:]:
            state.play(*move)
        self.assertTrue(state.is_finished())
        print(state)
        self.assertEqual(state.get_winner(), 0)


if __name__ == '__main__':
    state = GameState()
    unittest.main()
