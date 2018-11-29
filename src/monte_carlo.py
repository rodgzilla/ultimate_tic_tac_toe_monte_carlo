from game_engine import GameState
from random import sample
from copy import deepcopy
from collections import Counter

def play_to_the_end(state):
    state = deepcopy(state)

    while not state.is_finished():
        move = sample(state.get_possible_next_move(), 1)[0]
        state.play(*move)

    return state.get_winner()

if __name__ == '__main__':
    n       = 20000
    state   = GameState()
    results = [play_to_the_end(state) for _ in range(n)]
    print(Counter(results))
