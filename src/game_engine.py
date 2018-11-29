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
        self.board = [[[[None, None, None], [None, None, None], [0, None, None]],
                       1,
                       [[None, None, None], [None, None, None], [None, 1, None]]],
                      [[[0, None, None], [None, None, None], [None, None, None]],
                       [[None, None, None], [None, None, None], [None, None, None]],
                       0],
                      [[[None, None, None], [None, None, None], [None, None, None]],
                       [[None, None, None], [None, None, None], [None, None, None]],
                       [[0, None, None], [None, None, None], [None, None, None]]]]


    def play(self, grid_x, grid_y, cell_x, cell_y):
        pass

    def get_global_board(self):
        pass

    def get_local_board(self):
        pass

    def get_possible_next_move(self):
        pass

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
    def test_init(self):
        pass

    def test_play(self):
        pass

    def test_get_global_board(self):
        pass

    def test_get_local_board(self):
        pass

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
        pass

    def test_get_possible_next_move_multi_grid(self):
        pass

    def test_is_finished(self):
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
