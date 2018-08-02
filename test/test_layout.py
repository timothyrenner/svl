from svl.layout import (
    shift_node_position,
    shift_tree_positions,
    tree_to_grid
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

    tree = {
        "cat": "vcat",
        "nodes": [
            {
                "cat": "hcat",
                "nodes": [{
                    "plot": 1,
                    "row_start": 0,
                    "row_end": 1,
                    "column_start": 1,
                    "column_end": 2
                }]
            }, {
                "cat": "hcat",
                "nodes": [{
                    "plot": 2,
                    "row_start": 1,
                    "row_end": 2,
                    "column_start": 0,
                    "column_end": 1
                }]
            }
        ]
    }

    row_shift = 3
    column_shift = 2
    row_stretch = 3
    column_stretch = 2

    truth = {
        "cat": "vcat",
        "nodes": [
            {
                "cat": "hcat",
                "nodes": [{
                    "plot": 1,
                    "row_start": 3,
                    "row_end": 6,
                    "column_start": 4,
                    "column_end": 6
                }]
            }, {
                "cat": "hcat",
                "nodes": [{
                    "plot": 2,
                    "row_start": 6,
                    "row_end": 9,
                    "column_start": 2,
                    "column_end": 4
                }]
            }
        ]
    }

    answer = shift_tree_positions(
        tree,
        row_shift,
        column_shift,
        row_stretch,
        column_stretch
    )

    assert truth == answer


def test_tree_to_grid_single_plot_vcat():
    """ Tests that the tree_to_grid function works for a single plot.
    """
    tree = {
        "vcat": [{
            "plot": 1
        }]
    }

    answer = {
        "cat": None,
        "nodes": [{
            "cat": "vcat",
            "nodes": [{
                "plot": 1,
                "row_start": 0,
                "row_end": 1,
                "column_start": 0,
                "column_end": 1
            }]
        }]
    }

    truth = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_single_plot_hcat():
    """ Tests that the tree_to_grid function works correctly for a single
        hcat plot.
    """
    tree = {
        "hcat": [{
            "plot": 1
        }]
    }

    truth = {
        "cat": None,
        "nodes": [{
            "cat": "hcat",
            "nodes": [{
                "plot": 1,
                "row_start": 0,
                "row_end": 1,
                "column_start": 0,
                "column_end": 1
            }]
        }]
    }

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_multiple_plots_vcat():
    """ Tests that the tree_to_grid function returns the correct value when the
        tree contains multiple vcat plots.
    """
    tree = {
        "vcat": [
            {"plot": 1},
            {"plot": 2}
        ]
    }

    truth = {
        "cat": None,
        "nodes": [
            {
                "cat": "vcat",
                "nodes": [{
                    "plot": 1,
                    "row_start": 0,
                    "row_end": 1,
                    "column_start": 0,
                    "column_end": 1
                }]
            }, {
                "cat": "vcat",
                "nodes": [{
                    "plot": 2,
                    "row_start": 1,
                    "row_end": 2,
                    "column_start": 0,
                    "column_end": 1
                }]
            }
        ]
    }

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_multiple_plots_hcat():
    """ Tests that the tree_to_grid function returns the correct value when
        there are multiple horizontally concatenated plots.
    """

    tree = {
        "hcat": [
            {"plot": 1},
            {"plot": 2},
            {"plot": 3}
        ]
    }

    truth = {
        "cat": None,
        "nodes": [
            {
                "cat": "hcat",
                "nodes": [{
                    "plot": 1,
                    "row_start": 0,
                    "row_end": 1,
                    "column_start": 0,
                    "column_end": 1
                }]
            }, {
                "cat": "hcat",
                "nodes": [{
                    "plot": 2,
                    "row_start": 0,
                    "row_end": 1,
                    "column_start": 1,
                    "column_end": 2
                }]
            }, {
                "cat": "hcat",
                "nodes": [{
                    "plot": 3,
                    "row_start": 0,
                    "row_end": 1,
                    "column_start": 2,
                    "column_end": 3
                }]
            }
        ]
    }

    answer = tree_to_grid(tree)

    assert truth == answer
