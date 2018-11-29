from game_engine import GameState

from multiprocessing import Pool, cpu_count
from random import sample
from copy import deepcopy
from collections import Counter

def play_to_the_end(state):
    state = deepcopy(state)

    while not state.is_finished():
        move = sample(state.get_possible_next_move(), 1)[0]
        state.play(*move)

    return state.get_winner()

def evaluate_position(state, n):
    pool    = Pool(cpu_count())
    results = pool.map(play_to_the_end, [state] * n)
    pool.close()
    counter = Counter(results)

    return {
        0    : counter[0] / n,
        1    : counter[1] / n,
        None : counter[None] / n
    }

def find_best_next_move(state, n):
    possible_moves    = list(state.get_possible_next_move())
    n_next_move       = len(possible_moves)
    run_by_move       = n // n_next_move
    player            = state.get_player()
    move_to_win_proba = {}

    for move in possible_moves:
        move_state = deepcopy(state)
        move_state.play(*move)
        proba = evaluate_position(move_state, run_by_move)
        move_to_win_proba[move] = proba[player]

    result = sorted(move_to_win_proba.items(), key = lambda x: x[1], reverse = True)
    print(f'Number of game run by potential move: {run_by_move}')
    print(
        *(f'{xg} {yg} {xc} {yc} -> {100 * proba:5.2f}%' for (xg, yg, xc, yc), proba in result),
        sep = '\n'
    )

    return result[0][0]

if __name__ == '__main__':
    n       = 50000
    state   = GameState()
    # for i in range(30):
    #     win_0, win_1, draw = evaluate_position(state, n)
    #     print(f'[{i:2d}] {100 * win_0:5.2f}% {100 * win_1:5.2f}% {100 * draw:5.2f}%')
    state.play(1, 1, 1, 1)
    result = find_best_next_move(state, n)
    print(result)
