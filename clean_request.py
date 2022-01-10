import tic_tac_toe_model
from flask import abort, Response

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

def model_from_request(request):
    if 'player' not in request.form:
        abort(Response("missing current player", 400))
    player = mark_to_int(request.form.get('player'))
    model = tic_tac_toe_model.TicTacToeModel()
    moves = []
    for x in range(3):
        for y in range(3):
            spot = request.form.get(f'{x}-{y}', None)
            if spot is not None:
                moves.append(((x,y),mark_to_int(spot)))
    try:
        model.make_moves_on_empty_board(moves)
    except ValueError as e:
        abort(Response("Invalid board state", 400))
    if(player != model.current_player):
        abort(Response(f"{int_to_mark(player)} is not the current player on given board", 400))
    if(model.filled()):
        abort(Response("Board is filled", 400))
    return model