import tic_tac_toe_model

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
        abort(400)
    player = mark_to_int(request.form.get('player'))
    model = tic_tac_toe_model.TicTacToeModel()
    moves = []
    for x in range(3):
        for y in range(3):
            spot = request.form.get(f'{x}-{y}', None)
            if spot is not None:
                moves.append(((x,y),mark_to_int(spot)))
    model.make_moves(moves)
    return model