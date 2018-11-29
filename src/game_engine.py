import unittest

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
        # self.board = [[[[None, None, None], [None, None, None], [0, None, None]],
        #                1,
        #                [[None, None, None], [None, None, None], [None, 1, None]]],
        #               [[[0, None, None], [None, None, None], [None, None, None]],
        #                [[None, None, None], [None, None, None], [None, None, None]],
        #                0],
        #               [[[None, None, None], [None, None, None], [None, None, None]],
        #                [[None, None, None], [None, None, None], [None, None, None]],
        #                [[0, None, None], [None, None, None], [None, None, None]]]]

    def play(self, grid_x, grid_y, cell_x, cell_y):
        pass

    def get_global_board(self):
        pass

    def get_local_board(self):
        pass

    def get_possible_next_move(self):
        return []

    def is_finished(self):
        pass

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
                    line_repr[1].append(f'#{small_grid}#|')
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
        state.play(0, 0, 0, 0)
        with self.assertRaises(ValueError):
            state.play(0, 0, 0, 0)

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
        self.assertEqual(set(state.get_possible_next_move()), possible_moves)

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
            set(state.get_possible_next_move()),
            possible_moves
        )
        state.play(0, 0, 0, 1)
        possible_moves = {
            (0, 1, x, y)
            for x in range(3)
            for y in range(3)
        }
        self.assertEqual(
            set(state.get_possible_next_move()),
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
            set(state.get_possible_next_move()),
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


if __name__ == '__main__':
    state = GameState()
    print(state)
    unittest.main()
