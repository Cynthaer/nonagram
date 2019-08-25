import pytest

from nonogramboard import State, NonogramBoard, as_states
from nonogramsolver import NonogramSolver


class TestNonogramBoard:
    def test_shape(self, blank_board):
        assert blank_board.shape == (5, 5)

    def test_get_and_set_line(self, blank_board):
        blank_board.line(0, 0)[:] = as_states([1, 1, 1, 2, 1])
        assert blank_board.tiles[0,0] == State.YES
        assert blank_board.tiles[0,2:].tolist() == [State.YES, State.NO, State.YES]

    def test_invalid_hints_fail(self):
        with pytest.raises(Exception):
            NonogramBoard([[1]], [[2]])

    def test_invalid_tile_shape_fails(self):
        with pytest.raises(Exception):
            NonogramBoard([[1]], [[1]], [[0, 0]])

    def test_identify_solved_lines(self, in_progress_board):
        board = in_progress_board
        assert board.solved(0, 0)
        assert not board.solved(3, 0)
        assert board.solved(4, 1)
        assert not board.solved(2, 1)

    def test_identify_solved_board(self, blank_board, in_progress_board, solved_board):
        assert not blank_board.solved()
        assert not in_progress_board.solved()
        assert solved_board.solved()


class TestNonogramSolver:
    def test_invalid_rule_raises_valueerror(self, blank_board):
        solver = NonogramSolver(blank_board)
        with pytest.raises(ValueError, message="'fake_rule' is not a valid rule."):
            solver._apply_rule('fake_rule', 0, 0)

    def test_skip_rule_if_line_is_solved(self, solved_board):
        solver = NonogramSolver(solved_board)
        assert not solver._apply_rule('full_hint', 4, 0)

    def test_full_hint_rule_fills_full_line(self, blank_board):
        solver = NonogramSolver(blank_board)
        assert solver._apply_rule('full_hint', 4, 1)
        assert solver.board.line(4, 1).tolist() == [State.YES, State.YES, State.YES, State.YES, State.YES]

    def test_full_hint_rule_fills_split_line(self, blank_board):
        solver = NonogramSolver(blank_board)
        assert solver._apply_rule('full_hint', 0, 0)
        assert solver.board.line(0, 0).tolist() == [State.YES, State.YES, State.YES, State.NO, State.YES]

    def test_full_hint_rule_ignores_irrelevant_line(self, blank_board):
        solver = NonogramSolver(blank_board)
        assert not solver._apply_rule('full_hint', 4, 0)
