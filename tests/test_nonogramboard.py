import pytest

from nonogramboard import State, NonogramBoard, as_states
from nonogramsolver import NonogramSolver


class TestNonogramBoard:
    def test_shape(self, blank_board):
        assert blank_board.shape == (5, 5)

    def test_shape_with_zero_hint(self, blank_board_with_zero):
        assert blank_board_with_zero.shape == (3, 3)

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

    def test_identify_solved_line(self, in_progress_board):
        assert in_progress_board.solved(0, 0)
        assert not in_progress_board.solved(3, 0)
        assert in_progress_board.solved(4, 1)
        assert not in_progress_board.solved(2, 1)

    def test_identify_unsolved_zero_line(self, blank_board_with_zero):
        assert not blank_board_with_zero.solved(2, 0)

    def test_identify_solved_zero_line(self, blank_board_with_zero):
        blank_board_with_zero.line(2, 0)[:] = State.NO
        assert blank_board_with_zero.solved(2, 0)

    def test_identify_solved_board(self, blank_board, in_progress_board, solved_board):
        assert not blank_board.solved()
        assert not in_progress_board.solved()
        assert solved_board.solved()


class TestNonogramSolver:
    # rule: zero hint
    def test_zero_hint_fills_full_line(self, blank_board_with_zero):
        solver = NonogramSolver(blank_board_with_zero)
        assert solver._zero_hint(2, 0)
        assert solver.board.line(2, 0).tolist() == [State.NO, State.NO, State.NO]

    # rule: full hint
    def test_full_hint_fills_full_line(self, blank_board):
        solver = NonogramSolver(blank_board)
        assert solver._full_hint(4, 1)
        assert solver.board.line(4, 1).tolist() == [State.YES, State.YES, State.YES, State.YES, State.YES]

    def test_full_hint_fills_split_line(self, blank_board):
        solver = NonogramSolver(blank_board)
        assert solver._full_hint(0, 0)
        assert solver.board.line(0, 0).tolist() == [State.YES, State.YES, State.YES, State.NO, State.YES]

    def test_full_hint_ignores_irrelevant_line(self, blank_board):
        solver = NonogramSolver(blank_board)
        assert not solver._full_hint(4, 0)

    # rule: extend edge
    def test_extend_edge_works_for_true_edge_forward(self, in_progress_board_with_edges):
        solver = NonogramSolver(in_progress_board_with_edges)
        assert solver._extend_edge(0, 0)
        assert solver.board.line(0, 0).tolist() == [State.YES, State.YES, State.NO, State.BLANK]

    def test_extend_edge_works_for_true_edge_backward(self, in_progress_board_with_edges):
        solver = NonogramSolver(in_progress_board_with_edges)
        assert solver._extend_edge(3, 0)
        assert solver.board.line(3, 0).tolist() == [State.BLANK, State.NO, State.YES, State.YES]

    def test_extend_edge_works_for_full_line_forward(self, in_progress_board_with_edges):
        solver = NonogramSolver(in_progress_board_with_edges)
        assert solver._extend_edge(4, 0)
        assert solver.board.line(4, 0).tolist() == [State.YES, State.YES, State.YES, State.YES]

    def test_extend_edge_works_for_full_line_backward(self, in_progress_board_with_edges):
        solver = NonogramSolver(in_progress_board_with_edges)
        assert solver._extend_edge(5, 0)
        assert solver.board.line(5, 0).tolist() == [State.YES, State.YES, State.YES, State.YES]

    def test_extend_edge_works_for_soft_edge_forward(self, in_progress_board_with_edges):
        solver = NonogramSolver(in_progress_board_with_edges)
        assert solver._extend_edge(1, 0)
        assert solver.board.line(1, 0).tolist() == [State.NO, State.NO, State.YES, State.YES]

    def test_extend_edge_works_for_soft_edge_backward(self, in_progress_board_with_edges):
        solver = NonogramSolver(in_progress_board_with_edges)
        assert solver._extend_edge(2, 0)
        assert solver.board.line(2, 0).tolist() == [State.YES, State.YES, State.YES, State.NO]

