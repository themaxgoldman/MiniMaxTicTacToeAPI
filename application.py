from tic_tac_toe_model import TicTacToeModel
from flask import Flask, redirect, request, abort
from tic_tac_toe_minimax import get_next_move
application = app = Flask(__name__)

board_size = 3


@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect('/move')

def mark_to_int(mark):
    mark_lower = mark.lower()
    if mark_lower == 'x':
        return 0
    if mark_lower == 'o':
        return 1
    abort(400)

def int_to_mark(i):
    if i == 0:
        return 'X'
    if i == 1:
        return 'O'
    abort(400)

@app.route('/move', methods=['POST'])
def move():
    player = mark_to_int(request.form.get('player'))
    board = [[None for x in range(board_size)]
             for y in range(board_size)]
    remaining_moves = {(x, y)
                       for x in range(board_size)
                       for y in range(board_size)}
    num_moves = 0
    for x in range(board_size):
        for y in range(board_size):
            spot = request.form.get(f'{x},{y}', None)
            if spot is not None:
                board[x][y] = mark_to_int(spot)
                remaining_moves.remove((x, y))
            else:
                num_moves += 1

    model = TicTacToeModel(board_size)
    model.current_player = player
    model.num_moves = num_moves
    model.board = board
    model.remaining_moves = remaining_moves

    next_move = get_next_move(player, model)
    response = {'player_to_move': int_to_mark(player), 'x': next_move[0], 'y': next_move[1]}
    print(model)
    print(response)
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)
