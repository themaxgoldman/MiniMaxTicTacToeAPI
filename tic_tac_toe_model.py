from enum import Enum
import copy


def player_mark(player):
    """ Gets the mark to display for a player

    Args:
        player (int): the player

    Returns:
        str: the mark for the player
    """
    if player == 1:
        return "O"
    elif player == 0:
        return "X"
    else:
        return " "


class TicTacToeModel:

    checked_boards = dict()

    def __init__(self, board_size=3):
        """ Initializes a model with given size

        Args:
            board_size (int, optional): size of the board, defaults to 3.
        """
        self.board_size = board_size
        self.num_moves = 0
        self.current_player = 0
        self.board = [[None for x in range(self.board_size)]
                      for y in range(self.board_size)]
        self.remaining_moves = {
            (x, y) for x in range(self.board_size)
            for y in range(self.board_size)}
        self.winner = None
        self.moves = list()

    def __str__(self):
        """ Returns a string description of the model's board
            |---|---|---|
            | O |   | X |
            |---|---|---|
            | X |   | O |
            |---|---|---|
            |   |   | X |
            |---|---|---|

        Returns:
            str: the string description of the board
        """
        divider = "|---" * self.board_size + "|"
        final_str = "\n"
        for x in range(self.board_size):
            row = "|"
            for y in range(self.board_size):
                row += " " + player_mark(self.board[x][y]) + " |"
            final_str = final_str + divider + '\n'
            final_str = final_str + row + '\n'
        final_str = final_str + divider + '\n'
        return final_str

    def __len__(self):
        """ Returns the length, in this case the number
            of moves so far in the model


        Returns:
            int: the number of moves in the model
        """
        return self.num_moves

    def copy(self):
        """ Gives a deep copy of the model

        Returns:
            TicTacToeModel: the deep copy
        """
        copied = TicTacToeModel(board_size=self.board_size)
        copied.num_moves = self.num_moves
        copied.current_player = self.current_player
        copied.board = self.board.copy()
        copied.remaining_moves = self.remaining_moves.copy()
        copied.winner = self.winner
        copied.moves = self.moves.copy()
        return copied

    def check_winner(self, spot):
        """ Checks if there is a winner, only checks rows, columns,
            and diagonals of the given spot, no guarantee about
            other spots

        Args:
            spot ((int,int)): the spot to check at

        Raises:
            ValueError: x out of range of board size
            ValueError: y out of range of board size
            ValueError: spot is empty

        Returns:
            bool: true if winning state at the spot, false otherwise
        """
        if spot[0] >= self.board_size or spot[0] < 0:
            raise ValueError("x: {x} out of range: {board_size}".format(
                x=spot[0], board_size=(self.board_size - 1)))
        if spot[1] >= self.board_size or spot[1] < 0:
            raise ValueError(
                "y: {} out of range: {}".format(spot[1], self.board_size - 1))
        if self.num_moves < self.board_size * 2 - 1:
            return False
        player = self.board[spot[0]][spot[1]]
        if player is None:
            raise ValueError("empty spot given")

        if self.winner is not None:
            return True

        is_winning_state = False
        column_win = True
        row_win = True

        rl_diag_win = True
        for i in range(self.board_size):
            column_win = column_win and self.board[i][spot[1]] == player
            row_win = row_win and self.board[spot[0]][i] == player

        lr_diag_win = False
        if spot[0] == spot[1]:
            lr_diag_win = True
            for i in range(self.board_size):
                lr_diag_win = lr_diag_win and (
                    self.board[i][i] == player)

        rl_diag_win = False
        if spot[0] + spot[1] == self.board_size - 1:
            rl_diag_win = True
            for i in range(self.board_size):
                rl_diag_win = rl_diag_win and (
                    self.board[i][self.board_size - 1 - i] == player)

        is_winning_state = column_win or row_win or lr_diag_win or rl_diag_win
        if is_winning_state:
            self.winner = player
        return is_winning_state

    def make_move(self, move, player):
        """ Makes the given move on the board

        Args:
            move ((int, int)): the move to make
            player (int): the player who is making the move

        Raises:
            ValueError: x out of range of board size
            ValueError: y out of range of board size
            ValueError: invalid player (only 0 or 1)
            ValueError: incorrect player
            ValueError: invalid move, spot taken
        """
        if move[0] >= self.board_size or move[0] < 0:
            raise ValueError(
                "x: {x} out of range: {range}".format(
                    x=move[0],
                    range=(self.board_size - 1)))
        if move[1] >= self.board_size or move[1] < 0:
            raise ValueError(
                "y: {y} out of range: {range}".format(y=move[1],
                                                      range=(
                                                          self.board_size-1)))
        if player < 0 or player > 1:
            raise ValueError("invalid player")
        if self.current_player != player:
            raise ValueError("player is not current player")
        if self.board[move[0]][move[1]] is not None:
            raise ValueError("invalid move, spot already taken")
        self.board[move[0]][move[1]] = player
        self.current_player = (self.current_player + 1) % 2
        self.num_moves += 1
        self.remaining_moves.remove(move)
        self.moves.append(move)

    def undo_move(self):
        """ Undo the last move

        Raises:
            ValueError: no moves to undo
        """
        if len(self.moves) == 0:
            raise ValueError("no moves to undo")
        last_move = self.moves.pop()
        self.board[last_move[0]][last_move[1]] = None
        self.current_player = (self.current_player + 1) % 2
        self.num_moves -= 1
        self.remaining_moves.add(last_move)
        self.winner = None

    def filled(self):
        """ Returns whether or not the board is filled

        Returns:
            bool: True if the board is filled, false otherwise
        """
        return self.num_moves >= self.board_size ** 2
