# Day 13: Care Package
# Rank 81, 4

from utils import *


def would_you_like_to_play_a_game(values):
    runner = IntCode(values)
    runner.code[0] = 2
    score = 0
    game = defaultdict(int)
    is_first = True
    while runner.running:
        runner.run()
        ball = 0
        paddle = 0
        for i in range(0, len(runner.outputs), 3):
            x, y, tile_id = runner.outputs[i], runner.outputs[i + 1], runner.outputs[i + 2]
            if tile_id == 4:
                ball = x
            elif tile_id == 3:
                paddle = x
            if x == -1 and y == 0:
                score = tile_id
            else:
                game[(x, y)] = tile_id
        runner.outputs.clear()

        # Part 1, print the number of bricks after setup
        if is_first:
            is_first = False
            print_grid(game, GAME_OBJECTS)
            print('Bricks:', list(game.values()).count(2))

        # Uncomment to see progression of the game
        # print_grid(game, GAME_OBJECTS)

        # Simple paddle logic - move towards the ball
        runner.inputs.append(sign(ball - paddle))
    print('Score:', score)


GAME_OBJECTS = {0: ' ', 1: 'W', 2: 'X', 3: '=', 4: 'O'}

if __name__ == '__main__':
    would_you_like_to_play_a_game(get_input_intcode())
