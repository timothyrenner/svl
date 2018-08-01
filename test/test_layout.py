from svl.layout import (
    shift_node_position,
    shift_tree_positions
)


def test_shift_node_position():
    """ Tests that the shift_node_position function returns the correct value.
    """

    node = {
        "row_start": 0,
        "row_end": 1,
        "column_start": 2,
        "column_end": 3
    }

    row_shift = 3
    row_stretch = 3
    column_shift = 2
    column_stretch = 2

    truth = {
        "row_start": 3,
        "row_end": 6,
        "column_start": 6,
        "column_end": 8
    }

    answer = shift_node_position(
        node,
        row_shift,
        column_shift,
        row_stretch,
        column_stretch
    )

    assert truth == answer


def test_shift_tree_positions():
    """ Tests that the shift_tree_positions function returns the correct value.
    """

    assert False  # TODO: implement.
