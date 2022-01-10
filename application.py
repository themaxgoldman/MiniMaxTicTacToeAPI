from tic_tac_toe_model import TicTacToeModel
from flask import Flask, redirect, request, abort
from tic_tac_toe_minimax import get_next_move
from clean_request import model_from_request, int_to_mark
application = app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect('/move')

@app.route('/move', methods=['POST'])
def move():
    model = model_from_request(request)
    player = model.current_player

    next_move = get_next_move(player, model)
    response = {'player_to_move': int_to_mark(player), 'x': next_move[0], 'y': next_move[1]}
    
    print(response)
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)
