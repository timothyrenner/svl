from svl.compiler.layout import shift_node_position, tree_to_grid, gcd, lcm


def test_gcd():
    """ Tests that the gcd function returns the correct answer.
    """
    a = 54
    b = 24

    truth = 6

    answer = gcd(a, b)

    assert truth == answer


def test_lcm():
    """ Tests that the lcm function returns the correct answer.
    """
    a = 3
    b = 2

    truth = 6

    answer = lcm(a, b)

    assert truth == answer


def test_shift_node_position():
    """ Tests that the shift_node_position function returns the correct value.
    """

    node = {"row_start": 0, "row_end": 1, "column_start": 2, "column_end": 3}

    row_shift = 3
    row_stretch = 3
    column_shift = 2
    column_stretch = 2

    truth = {"row_start": 3, "row_end": 6, "column_start": 6, "column_end": 8}

    answer = shift_node_position(
        node, row_shift, column_shift, row_stretch, column_stretch
    )

    assert truth == answer


def test_tree_to_grid_single_plot_vcat():
    """ Tests that the tree_to_grid function works for a single plot.
    """
    tree = {"vcat": [{"plot": 1}]}

    answer = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 1,
        }
    ]

    truth = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_single_plot_hcat():
    """ Tests that the tree_to_grid function works correctly for a single
        hcat plot.
    """
    tree = {"hcat": [{"plot": 1}]}

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 1,
        }
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_multiple_plots_vcat():
    """ Tests that the tree_to_grid function returns the correct value when the
        tree contains multiple vcat plots.
    """
    tree = {"vcat": [{"plot": 1}, {"plot": 2}]}

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 1,
        },
        {
            "plot": 2,
            "row_start": 1,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1,
        },
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_multiple_plots_hcat():
    """ Tests that the tree_to_grid function returns the correct value when
        there are multiple horizontally concatenated plots.
    """

    tree = {"hcat": [{"plot": 1}, {"plot": 2}, {"plot": 3}]}

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 1,
        },
        {
            "plot": 2,
            "row_start": 0,
            "row_end": 1,
            "column_start": 1,
            "column_end": 2,
        },
        {
            "plot": 3,
            "row_start": 0,
            "row_end": 1,
            "column_start": 2,
            "column_end": 3,
        },
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_stacked_vcats():
    """ Tests that the tree_to_grid function returns the correct value for
        multilayered vcats.
    """
    tree = {"vcat": [{"plot": 1}, {"vcat": [{"plot": 2}, {"plot": 3}]}]}

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1,
        },
        {
            "plot": 2,
            "row_start": 2,
            "row_end": 3,
            "column_start": 0,
            "column_end": 1,
        },
        {
            "plot": 3,
            "row_start": 3,
            "row_end": 4,
            "column_start": 0,
            "column_end": 1,
        },
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_stacked_hcats():
    """ Tests that the tree_to_grid function returns the correct value for
        multilayered hcats.
    """
    tree = {"hcat": [{"plot": 1}, {"hcat": [{"plot": 2}, {"plot": 3}]}]}

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 2,
        },
        {
            "plot": 2,
            "row_start": 0,
            "row_end": 1,
            "column_start": 2,
            "column_end": 3,
        },
        {
            "plot": 3,
            "row_start": 0,
            "row_end": 1,
            "column_start": 3,
            "column_end": 4,
        },
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_hcat_vcat():
    """ Tests that the tree_to_grid function returns the correct value when
        a single plot is horizontally concatenated with two vertically
        concatenated plots.
    """
    tree = {"hcat": [{"plot": 1}, {"vcat": [{"plot": 2}, {"plot": 3}]}]}

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1,
        },
        {
            "plot": 2,
            "row_start": 0,
            "row_end": 1,
            "column_start": 1,
            "column_end": 2,
        },
        {
            "plot": 3,
            "row_start": 1,
            "row_end": 2,
            "column_start": 1,
            "column_end": 2,
        },
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_vcat_hcat():
    """ Tests that the tree_to_grid function returns the correct answer when
        a single plot is vertically concatenated with two horizontally
        concatenated plots.
    """
    tree = {"vcat": [{"plot": 1}, {"hcat": [{"plot": 2}, {"plot": 3}]}]}

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 2,
        },
        {
            "plot": 2,
            "row_start": 1,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1,
        },
        {
            "plot": 3,
            "row_start": 1,
            "row_end": 2,
            "column_start": 1,
            "column_end": 2,
        },
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_regular_grid_vcat():
    """ Tests that the tree_to_grid function returns the correct value when the
        plots are placed on a regular 2x2 grid with vertical concatenation.
    """
    tree = {
        "vcat": [
            {"hcat": [{"plot": 1}, {"plot": 2}]},
            {"hcat": [{"plot": 3}, {"plot": 4}]},
        ]
    }

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 1,
        },
        {
            "plot": 2,
            "row_start": 0,
            "row_end": 1,
            "column_start": 1,
            "column_end": 2,
        },
        {
            "plot": 3,
            "row_start": 1,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1,
        },
        {
            "plot": 4,
            "row_start": 1,
            "row_end": 2,
            "column_start": 1,
            "column_end": 2,
        },
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_regular_grid_hcat():
    """ Tests that the tree_to_grid function returns the correct value when the
        plots are placed on a regular 2x2 grid with horizontal concatenation.
    """

    tree = {
        "hcat": [
            {"vcat": [{"plot": 1}, {"plot": 2}]},
            {"vcat": [{"plot": 3}, {"plot": 4}]},
        ]
    }

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 1,
        },
        {
            "plot": 2,
            "row_start": 1,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1,
        },
        {
            "plot": 3,
            "row_start": 0,
            "row_end": 1,
            "column_start": 1,
            "column_end": 2,
        },
        {
            "plot": 4,
            "row_start": 1,
            "row_end": 2,
            "column_start": 1,
            "column_end": 2,
        },
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_mixed_hcat_vcat():
    """ Tests that the tree_to_grid function returns the correct value when
        there are mixed vcats and hcats.
    """
    tree = {
        "hcat": [
            {"vcat": [{"plot": 1}, {"plot": 2}]},
            {"hcat": [{"plot": 3}, {"plot": 4}]},
        ]
    }

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 1,
            "column_start": 0,
            "column_end": 2,
        },
        {
            "plot": 2,
            "row_start": 1,
            "row_end": 2,
            "column_start": 0,
            "column_end": 2,
        },
        {
            "plot": 3,
            "row_start": 0,
            "row_end": 2,
            "column_start": 2,
            "column_end": 3,
        },
        {
            "plot": 4,
            "row_start": 0,
            "row_end": 2,
            "column_start": 3,
            "column_end": 4,
        },
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_mixed_vcat_hcat():
    """ Tests that the tree_to_grid function returns the correct value when
        there are mixed vcats and hcats.
    """
    tree = {
        "vcat": [
            {"hcat": [{"plot": 1}, {"plot": 2}]},
            {"vcat": [{"plot": 3}, {"plot": 4}]},
        ]
    }

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 2,
            "column_start": 0,
            "column_end": 1,
        },
        {
            "plot": 2,
            "row_start": 0,
            "row_end": 2,
            "column_start": 1,
            "column_end": 2,
        },
        {
            "plot": 3,
            "row_start": 2,
            "row_end": 3,
            "column_start": 0,
            "column_end": 2,
        },
        {
            "plot": 4,
            "row_start": 3,
            "row_end": 4,
            "column_start": 0,
            "column_end": 2,
        },
    ]

    answer = tree_to_grid(tree)

    assert truth == answer


def test_tree_to_grid_doomsday():
    """ The gnarliest of tests.
    """
    tree = {
        "vcat": [
            {
                "hcat": [
                    {"plot": 1},
                    {"vcat": [{"plot": 2}, {"plot": 3}, {"plot": 4}]},
                    {
                        "vcat": [
                            {"plot": 5},
                            {"hcat": [{"plot": 6}, {"plot": 7}]},
                        ]
                    },
                    {
                        "vcat": [
                            {"hcat": [{"plot": 8}, {"plot": 9}]},
                            {"plot": 10},
                        ]
                    },
                ]
            },
            {"plot": 11},
        ]
    }

    truth = [
        {
            "plot": 1,
            "row_start": 0,
            "row_end": 6,
            "column_start": 0,
            "column_end": 2,
        },
        {
            "plot": 2,
            "row_start": 0,
            "row_end": 2,
            "column_start": 2,
            "column_end": 4,
        },
        {
            "plot": 3,
            "row_start": 2,
            "row_end": 4,
            "column_start": 2,
            "column_end": 4,
        },
        {
            "plot": 4,
            "row_start": 4,
            "row_end": 6,
            "column_start": 2,
            "column_end": 4,
        },
        {
            "plot": 5,
            "row_start": 0,
            "row_end": 3,
            "column_start": 4,
            "column_end": 6,
        },
        {
            "plot": 6,
            "row_start": 3,
            "row_end": 6,
            "column_start": 4,
            "column_end": 5,
        },
        {
            "plot": 7,
            "row_start": 3,
            "row_end": 6,
            "column_start": 5,
            "column_end": 6,
        },
        {
            "plot": 8,
            "row_start": 0,
            "row_end": 3,
            "column_start": 6,
            "column_end": 7,
        },
        {
            "plot": 9,
            "row_start": 0,
            "row_end": 3,
            "column_start": 7,
            "column_end": 8,
        },
        {
            "plot": 10,
            "row_start": 3,
            "row_end": 6,
            "column_start": 6,
            "column_end": 8,
        },
        {
            "plot": 11,
            "row_start": 6,
            "row_end": 12,
            "column_start": 0,
            "column_end": 8,
        },
    ]

    answer = tree_to_grid(tree)

    assert truth == answer
