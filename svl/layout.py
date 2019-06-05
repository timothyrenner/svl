from toolz import compose, merge, concat
from functools import reduce

listconcat = compose(list, concat)

START_POSITION = {
    "row_start": 0,
    "row_end": 1,
    "column_start": 0,
    "column_end": 1,
}


def gcd(a, b):
    """ Computes the greatest common divisor between the two numbers using
        Euclid's algorithm.
    """
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def lcm(a, b):
    """ Computes the least common multiple between the two numbers.
    """
    return (a * b) / gcd(a, b)


def shift_node_position(
    node, row_shift, column_shift, row_stretch, column_stretch
):
    """ Shifts the position of a node in the plot layout tree, also adjusting
        the length units of the start / end values for the rows and columns.

        Parameters
        ----------
        node : dict
            The node of the plot tree as a dictionary.

        row_shift : int
            The number of cells to shift the rows by. Applied after stretching.

        column_shift : int
            The number of cells to shift the columns by. Applied after
            stretching.

        row_stretch : int
            The factor by which to stretch the rows. Applied prior to shifting.

        column_stretch : int
            The factor by which to stretch the columns. Applied prior to
            shifting.

        Returns
        -------
        dict
            The nodes with the row and column positions adjusted.
    """

    return merge(
        node,
        {
            "row_start": int(row_stretch * node["row_start"] + row_shift),
            "row_end": int(row_stretch * node["row_end"] + row_shift),
            "column_start": int(
                column_stretch * node["column_start"] + column_shift
            ),
            "column_end": int(
                column_stretch * node["column_end"] + column_shift
            ),
        },
    )


def tree_to_grid(tree):
    """ Transforms a parsed SVL tree without position information into a list
        of nodes with the grid positions.

        Parameters
        ----------
        tree : dict
            A parsed SVL tree.

        Returns
        -------
        list
            The nodes in the tree with their associated positions in a flat
            list.
    """
    if ("hcat" in tree) or ("vcat" in tree):
        cat = "hcat" if "hcat" in tree else "vcat"

        # Obtain subtrees. Note this flattens them.
        subtrees = [tree_to_grid(subtree) for subtree in tree[cat]]

        # Calculate the breadths in horizonal and vertical dimensions.
        # This is done by examining the maximum row and column end points of
        # each of the subtrees.
        row_breadths = [
            reduce(max, [n["row_end"] for n in subtree])
            for subtree in subtrees
        ]

        column_breadths = [
            reduce(max, [n["column_end"] for n in subtree])
            for subtree in subtrees
        ]

        # Use the breadths to determine the row / column length units. This
        # is the "final" length unit of the current tree.
        row_length_unit = reduce(lambda a, x: lcm(a, x), row_breadths)
        column_length_unit = reduce(lambda a, x: lcm(a, x), column_breadths)

        # Set the shift axis to vertical or horizontal.
        # vcat causes a row shift, hcat causes a column one.
        row_shift = row_length_unit if cat == "vcat" else 0
        column_shift = column_length_unit if cat == "hcat" else 0

        # Shift the positions of each of the subtrees.
        shifted_subtrees = [
            # Map the shift_node_position function to each subtree's nodes.
            [
                shift_node_position(
                    node,
                    row_shift * ii,
                    column_shift * ii,
                    # The stretch factor of the subtree depends on the breadth
                    # and the length unit of the total tree.
                    int(row_length_unit / row_breadths[ii]),
                    int(column_length_unit / column_breadths[ii]),
                )
                for node in subtree
            ]
            for ii, subtree in enumerate(subtrees)
        ]

        # Concatenate all of the shifted subtrees into a single list.
        return listconcat(shifted_subtrees)

    else:
        # For a leaf node, inject the start position of (0 / 1, 0 / 1) and
        # wrap into a list.
        return [merge(tree, START_POSITION)]
