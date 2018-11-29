from game_engine import GameState
from monte_carlo import find_best_next_move

def game_loop_human_vs_ai(n = 20000):
    state = GameState()

    while not state.is_finished():
        if state.get_player() == 0:
            print(state)
            print(*(f'{a} {b} {c} {d}' for a, b, c, d in state.get_possible_next_move()), sep = ', ')
            grid_x, grid_y, cell_x, cell_y = map(int, input().split())
            state.play(grid_x, grid_y, cell_x, cell_y)
            print(state)
        else:
            next_ai_move = find_best_next_move(state, n)
            state.play(*next_ai_move)

    print(state)
    print(f'Winner: {state.winner}')

def game_loop_ai_vs_ai(n = 20000):
    state = GameState()

    while not state.is_finished():
        # if state.get_player() == 0:
        #     print(state)
        #     print(*(f'{a} {b} {c} {d}' for a, b, c, d in state.get_possible_next_move()), sep = ', ')
        #     grid_x, grid_y, cell_x, cell_y = map(int, input().split())
        #     state.play(grid_x, grid_y, cell_x, cell_y)
        #     print(state)
        # else:
        print(state)
        next_ai_move = find_best_next_move(state, n)
        state.play(*next_ai_move)

    print(state)
    print(f'Winner: {state.winner}')

if __name__ == '__main__':
    # game_loop_human_vs_ai()
    game_loop_ai_vs_ai()
