from svl.layout import (
    shift_node_position,
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


def test_tree_to_grid_single_plot_vcat():
    """ Tests that the tree_to_grid function works for a single plot.
    """
    tree = {
        "vcat": [{
            "plot": 1
        }]
    }

    answer = [{
        "plot": 1,
        "row_start": 0,
        "row_end": 1,
        "column_start": 0,
        "column_end": 1
    }]

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

    truth = [{
        "plot": 1,
        "row_start": 0,
        "row_end": 1,
        "column_start": 0,
        "column_end": 1
    }]

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

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 1
        }, {
            "plot": 2,
            "row_start": 1,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1
        }
    ]

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

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 1
        }, {
            "plot": 2,
            "row_start": 0,
            "row_end": 1,
            "column_start": 1,
            "column_end": 2
        }, {
            "plot": 3,
            "row_start": 0,
            "row_end": 1,
            "column_start": 2,
            "column_end": 3
        }
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_stacked_vcats():
    """ Tests that the tree_to_grid function returns the correct value for
        multilayered vcats.
    """
    tree = {
        "vcat": [
            {"plot": 1},
            {
                "vcat": [
                    {"plot": 2},
                    {"plot": 3}
                ]
            }
        ]
    }

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1
        }, {
            "plot": 2,
            "row_start": 2,
            "row_end": 3,
            "column_start": 0,
            "column_end": 1
        }, {
            "plot": 3,
            "row_start": 3,
            "row_end": 4,
            "column_start": 0,
            "column_end": 1
        }
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_stacked_hcats():
    """ Tests that the tree_to_grid function returns the correct value for
        multilayered hcats.
    """
    tree = {
        "hcat": [
            {"plot": 1},
            {
                "hcat": [
                    {"plot": 2},
                    {"plot": 3}
                ]
            }
        ]
    }

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 2
        }, {
            "plot": 2,
            "row_start": 0,
            "row_end": 1,
            "column_start": 2,
            "column_end": 3
        }, {
            "plot": 3,
            "row_start": 0,
            "row_end": 1,
            "column_start": 3,
            "column_end": 4
        }
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_hcat_vcat():
    """ Tests that the tree_to_grid function returns the correct value when
        a single plot is horizontally concatenated with two vertically
        concatenated plots.
    """
    tree = {
        "hcat": [
            {"plot": 1},
            {
                "vcat": [
                    {"plot": 2},
                    {"plot": 3}
                ]
            }
        ]
    }

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1
        }, {
            "plot": 2,
            "row_start": 0,
            "row_end": 1,
            "column_start": 1,
            "column_end": 2
        }, {
            "plot": 3,
            "row_start": 1,
            "row_end": 2,
            "column_start": 1,
            "column_end": 2
        }
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_vcat_hcat():
    """ Tests that the tree_to_grid function returns the correct answer when
        a single plot is vertically concatenated with two horizontally
        concatenated plots.
    """
    tree = {
        "vcat": [
            {"plot": 1},
            {
                "hcat": [
                    {"plot": 2},
                    {"plot": 3}
                ]
            }
        ]
    }

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 2
        }, {
            "plot": 2,
            "row_start": 1,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1
        }, {
            "plot": 3,
            "row_start": 1,
            "row_end": 2,
            "column_start": 1,
            "column_end": 2
        }
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_regular_grid_vcat():
    """ Tests that the tree_to_grid function returns the correct value when the
        plots are placed on a regular 2x2 grid with vertical concatenation.
    """
    tree = {
        "vcat": [
            {
                "hcat": [
                    {"plot": 1},
                    {"plot": 2}
                ]
            }, {
                "hcat": [
                    {"plot": 3},
                    {"plot": 4}
                ]
            }
        ]
    }

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 1
        }, {
            "plot": 2,
            "row_start": 0,
            "row_end": 1,
            "column_start": 1,
            "column_end": 2
        }, {
            "plot": 3,
            "row_start": 1,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1
        }, {
            "plot": 4,
            "row_start": 1,
            "row_end": 2,
            "column_start": 1,
            "column_end": 2
        }
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_mixed_hcat_vcat():
    """ Tests that the tree_to_grid function returns the correct value when
        there are mixed vcats and hcats.
    """
    tree = {
        "hcat": [
            {
                "vcat": [
                    {"plot": 1},
                    {"plot": 2}
                ]
            }, {
                "hcat": [
                    {"plot": 3},
                    {"plot": 4}
                ]
            }
        ]
    }

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 2
        }, {
            "plot": 2,
            "row_start": 1,
            "row_end": 2,
            "column_start": 0,
            "column_end": 2
        }, {
            "plot": 3,
            "row_start": 0,
            "row_end": 2,
            "column_start": 2,
            "column_end": 3
        }, {
            "plot": 4,
            "row_start": 0,
            "row_end": 2,
            "column_start": 3,
            "column_end": 4
        }
    ]

    answer = tree_to_grid(tree)

    assert truth == answer
