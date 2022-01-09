import unittest
from tic_tac_toe_model import TicTacToeModel


class TicTacToeModelTestCases(unittest.TestCase):

    def setUp(self):
        self.empty_board = TicTacToeModel()

        self.mid_game_board = TicTacToeModel()
        mid_game_board_moves = []
        mid_game_board_moves.append(((0, 0), 0))
        mid_game_board_moves.append(((0, 1), 1))
        mid_game_board_moves.append(((0, 2), 0))
        mid_game_board_moves.append(((2, 1), 1))
        mid_game_board_moves.append(((1, 1), 0))
        self.mid_game_board.make_moves(mid_game_board_moves)

    def test_default_size(self):
        self.assertEqual(self.empty_board.board_size, 3)

    def test_empty_board(self):
        self.assertEqual(len(self.empty_board), 0)
        self.assertEqual(self.empty_board.board,
                         [[None, None, None],
                          [None, None, None],
                          [None, None, None]])
        self.assertEqual(
            self.empty_board.remaining_moves,
            {(0, 0),
             (0, 1),
             (0, 2),
             (1, 0),
             (1, 1),
             (1, 2),
             (2, 0),
             (2, 1),
             (2, 2)})

    def test_make_move_x_out_of_range(self):
        with self.assertRaises(ValueError):
            self.empty_board.make_move((3, 1), 0)
        with self.assertRaises(ValueError):
            self.empty_board.make_move((-1, 1), 0)

    def test_make_move_y_out_of_range(self):
        with self.assertRaises(ValueError):
            self.empty_board.make_move((1, 3), 0)
        with self.assertRaises(ValueError):
            self.empty_board.make_move((1, -1), 0)

    def test_make_move_invalid_player(self):
        with self.assertRaises(ValueError):
            self.empty_board.make_move((1, 2), -1)
        with self.assertRaises(ValueError):
            self.empty_board.make_move((1, 2), 2)

    def test_make_move_invalid_move(self):
        with self.assertRaises(ValueError):
            self.empty_board.make_move((0, 0), 1)

    def test_make_move_spot_taken(self):
        with self.assertRaises(ValueError):
            self.mid_game_board.make_move((0, 0), 1)
        with self.assertRaises(ValueError):
            self.mid_game_board.make_move((0, 1), 1)

    def test_make_move_wrong_player(self):
        with self.assertRaises(ValueError):
            self.empty_board.make_move((1, 2), 1)
        with self.assertRaises(ValueError):
            self.mid_game_board.make_move((2, 2), 0)

    def test_make_move_empty_board(self):
        self.empty_board.make_move((1, 1), 0)
        self.assertEqual(len(self.empty_board), 1)
        self.assertEqual(self.empty_board.board,
                         [[None, None, None],
                          [None, 0,    None],
                          [None, None, None]])
        self.assertEqual(
            self.empty_board.remaining_moves,
            {(0, 0),
             (0, 1),
             (0, 2),
             (1, 0),
             (1, 2),
             (2, 0),
             (2, 1),
             (2, 2)})
        self.empty_board.make_move((0, 0), 1)
        self.assertEqual(len(self.empty_board), 2)
        self.assertEqual(self.empty_board.board,
                         [[1,    None, None],
                          [None, 0,    None],
                          [None, None, None]])
        self.assertEqual(
            self.empty_board.remaining_moves,
            {(0, 1),
             (0, 2),
             (1, 0),
             (1, 2),
             (2, 0),
             (2, 1),
             (2, 2)})

    def test_make_move_mid_game_board(self):
        self.mid_game_board.make_move((2, 2), 1)
        self.assertEqual(len(self.mid_game_board), 6)
        self.assertEqual(self.mid_game_board.board,
                         [[0,    1, 0],
                          [None, 0, None],
                          [None, 1, 1]])
        self.assertEqual(
            self.mid_game_board.remaining_moves,
            {(1, 0),
             (1, 2),
             (2, 0)})
        self.mid_game_board.make_move((2, 0), 0)
        self.assertEqual(len(self.mid_game_board), 7)
        self.assertEqual(self.mid_game_board.board,
                         [[0,    1, 0],
                          [None, 0, None],
                          [0,    1, 1]])
        self.assertEqual(
            self.mid_game_board.remaining_moves,
            {(1, 0),
             (1, 2)})

    def test_check_winner_empty_spot(self):
        with self.assertRaises(ValueError):
            self.mid_game_board.check_winner((1, 2))

    def test_check_winner_x_out_of_range(self):
        with self.assertRaises(ValueError):
            self.empty_board.check_winner((3, 0))
        with self.assertRaises(ValueError):
            self.empty_board.check_winner((-1, 0))

    def test_check_winner_y_out_of_range(self):
        with self.assertRaises(ValueError):
            self.empty_board.check_winner((0, 3))
        with self.assertRaises(ValueError):
            self.empty_board.check_winner((0, -1))

    def test_check_winner_empty_board(self):
        self.assertFalse(self.empty_board.check_winner((0, 0)))

    def test_check_winner_no_winner(self):
        self.assertFalse(self.mid_game_board.check_winner((0, 0)))
        self.assertFalse(self.mid_game_board.check_winner((0, 1)))
        self.assertFalse(self.mid_game_board.check_winner((0, 2)))
        self.assertFalse(self.mid_game_board.check_winner((1, 1)))
        self.assertFalse(self.mid_game_board.check_winner((2, 1)))

    def test_check_winner_column_0(self):
        winning_board = TicTacToeModel()
        moves_to_make = [((1,1),0), ((0,0),1), ((0,2),0), ((1,0),1), ((1,2),0), ((2,0),1), ((2,1),0), ((2,2),1)]
        winning_board.make_moves(moves_to_make)
        self.assertTrue(winning_board.check_winner((0, 0)))
        self.assertTrue(winning_board.check_winner((1, 0)))
        self.assertTrue(winning_board.check_winner((2, 0)))

    def test_check_winner_column_1(self):
        winning_board = TicTacToeModel()
        moves_to_make = [((1,1),0), ((0,0),1), ((0,1),0), ((0,2),1), ((2,1),0)]
        winning_board.make_moves(moves_to_make)
        self.assertTrue(winning_board.check_winner((0, 1)))
        self.assertTrue(winning_board.check_winner((1, 1)))
        self.assertTrue(winning_board.check_winner((2, 1)))

    def test_check_winner_column_2(self):
        winning_board = TicTacToeModel()
        moves_to_make = [((0,0),0), ((0,2),1), ((0,1),0), ((1,2),1), ((1,1),0), ((2,2),1)]
        winning_board.make_moves(moves_to_make)
        self.assertTrue(winning_board.check_winner((0, 2)))
        self.assertTrue(winning_board.check_winner((1, 2)))
        self.assertTrue(winning_board.check_winner((2, 2)))

    def test_check_winner_row_0(self):
        winning_board = TicTacToeModel()
        moves_to_make = [((0,0),0), ((2,0),1), ((0,1),0), ((1,1),1), ((0,2),0), ((1,2),1), ((2,2),0)]
        winning_board.make_moves(moves_to_make)
        self.assertTrue(winning_board.check_winner((0, 0)))
        self.assertTrue(winning_board.check_winner((0, 1)))
        self.assertTrue(winning_board.check_winner((0, 2)))

    def test_check_winner_row_1(self):
        winning_board = TicTacToeModel()
        moves_to_make = [((0,0),0), ((1,0),1), ((2,1),0), ((1,1),1), ((0,2),0), ((2,0),1), ((2,2),0), ((1,2),1)]
        winning_board.make_moves(moves_to_make)
        self.assertTrue(winning_board.check_winner((1, 0)))
        self.assertTrue(winning_board.check_winner((1, 1)))
        self.assertTrue(winning_board.check_winner((1, 2)))

    def test_check_winner_row_2(self):
        winning_board = TicTacToeModel()
        moves_to_make = [((2,0),0), ((1,0),1), ((2,1),0), ((1,1),1), ((2,2),0)]
        winning_board.make_moves(moves_to_make)
        self.assertTrue(winning_board.check_winner((2, 0)))
        self.assertTrue(winning_board.check_winner((2, 1)))
        self.assertTrue(winning_board.check_winner((2, 2)))

    def test_check_winner_left_right_diag(self):
        winning_board = TicTacToeModel()
        moves_to_make = [((1,0),0), ((0,0),1), ((2,0),0), ((1,1),1), ((2,1),0), ((2,2),1)]
        winning_board.make_moves(moves_to_make)
        self.assertTrue(winning_board.check_winner((0, 0)))
        self.assertTrue(winning_board.check_winner((1, 1)))
        self.assertTrue(winning_board.check_winner((2, 2)))

    def test_check_winner_right_left_diag(self):
        winning_board = TicTacToeModel()
        moves_to_make = [((0,0),0), ((1,0),1), ((2,0),0), ((1,2),1), ((1,1),0), ((2,2),1), ((0,2),0)]
        winning_board.make_moves(moves_to_make)
        self.assertTrue(winning_board.check_winner((0, 2)))
        self.assertTrue(winning_board.check_winner((1, 1)))
        self.assertTrue(winning_board.check_winner((2, 0)))




    def test_check_filled(self):
        self.assertFalse(self.empty_board.filled())
        self.empty_board.make_move((0, 0), 0)
        self.assertFalse(self.empty_board.filled())
        self.empty_board.make_move((1, 0), 1)
        self.assertFalse(self.empty_board.filled())
        self.empty_board.make_move((2, 0), 0)
        self.assertFalse(self.empty_board.filled())
        self.empty_board.make_move((0, 2), 1)
        self.assertFalse(self.empty_board.filled())
        self.empty_board.make_move((0, 1), 0)
        self.assertFalse(self.empty_board.filled())
        self.empty_board.make_move((2, 1), 1)
        self.assertFalse(self.empty_board.filled())
        self.empty_board.make_move((1, 1), 0)
        self.assertFalse(self.empty_board.filled())
        self.empty_board.make_move((2, 2), 1)
        self.assertFalse(self.empty_board.filled())
        self.empty_board.make_move((1, 2), 0)
        self.assertTrue(self.empty_board.filled())
        self.assertEqual(
            self.empty_board.remaining_moves, set())

    def test_copy(self):
        copy = self.mid_game_board.copy()
        self.assertEqual(len(copy), 5)
        self.assertEqual(copy.current_player, 1)
        self.assertEqual(copy.board, self.mid_game_board.board)
        self.assertEqual(copy.remaining_moves, {
                         (1, 0), (1, 2), (2, 0), (2, 2)})

        copy_board_before = copy.board.copy()
        self.mid_game_board.make_move((1, 0), 1)

        self.assertEqual(len(copy), 5)
        self.assertEqual(copy.current_player, 1)
        self.assertEqual(copy.board, copy_board_before)
        self.assertEqual(copy.remaining_moves, {
                         (1, 0), (1, 2), (2, 0), (2, 2)})

    def test_undo_move_no_move(self):
        with self.assertRaises(ValueError):
            self.empty_board.undo_move()

    def test_undo_move_mid_game(self):
        self.assertEqual(self.mid_game_board.moves[4], (1, 1))
        self.mid_game_board.undo_move()
        self.assertEqual(self.mid_game_board.moves[3], (2, 1))
        self.assertEqual(len(self.mid_game_board), 4)
        self.assertEqual(self.mid_game_board.remaining_moves,
                         {(1, 0), (1, 2), (2, 0), (2, 2), (1, 1)})
        self.assertEqual(self.mid_game_board.current_player, 0)


if __name__ == "__main__":
    unittest.main()
