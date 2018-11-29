from game_engine import GameState
from monte_carlo import play_to_the_end

def game_loop():
    state = GameState()

    while not state.is_finished():
        print(state)
        print(state.get_possible_next_move())
        grid_x, grid_y, cell_x, cell_y = map(int, input().split())
        state.play(grid_x, grid_y, cell_x, cell_y)

    print(state)
    print(f'Winner: {state.winner}')

if __name__ == '__main__':
    # game_loop()
    state = GameState()
    play_to_the_end(state)
