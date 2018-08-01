from toolz import compose, mapcat, merge
from functools import reduce

listmapcat = compose(list, mapcat)

START_POSITION = {
    "row_start": 0,
    "row_end": 1,
    "column_start": 0,
    "column_end": 1
}


def shift_position(node, row_shift, column_shift, row_stretch, column_stretch):
    return merge(
        node,
        {
            "row_start": row_stretch * node["row_start"] + row_shift,
            "row_end": row_stretch * node["row_end"] + row_shift,
            "column_start":
                column_stretch * node["column_start"] + column_shift,
            "column_end": column_stretch * node["column_end"] + column_shift
        }
    )


def shift_tree_positions(
    tree,
    row_shift,
    column_shift,
    row_stretch,
    column_stretch
):
    if len(tree["nodes"]) > 1:
        return {
            "cat": tree["cat"],
            "nodes": [
                shift_tree_positions(
                    subtree,
                    row_shift,
                    column_shift,
                    row_stretch,
                    column_stretch
                ) for subtree in tree["nodes"]
            ]
        }
    else:
        return {
            "cat": tree["cat"],
            "nodes": [
                # We know tree["nodes"] only has one dict in it :).
                shift_position(
                    tree["nodes"][0],
                    row_shift,
                    column_shift,
                    row_stretch,
                    column_stretch
                )
            ]
        }


def tree_to_grid(tree, parent_cat=None):
    if ("hcat" in tree) or ("vcat" in tree):
        cat = "hcat" if "hcat" in tree else "vcat"

        # Obtain subtrees. On the first traversal down, "nodes" and "cat"
        # have note been injected as fields.
        subtrees = [
            tree_to_grid(subtree, parent_cat=cat) for subtree in tree[cat]
        ]

        # Calculate the breadths in horizonal and vertical dimensions.
        # This is done by examining whether each subtree is in a vcat or
        # hcat. vcats set column sizes, hcats set row sizes.
        # This seems counterintuitive, but two side by side columns
        # (via hcat) actually need their rows adjusted, while two
        # stacked rows (via vcat) need their columns adjusted to fit.
        row_breadths = [
            len(subtree["nodes"]) if subtree["cat"] == "hcat" else 1
            for subtree in subtrees
        ]

        column_breadths = [
            len(subtree["nodes"]) if subtree["cat"] == "vcat" else 1
            for subtree in subtrees
        ]

        # Use the breadths to determine the row / column length units.
        row_length_unit = reduce(lambda a, x: a*x, row_breadths)
        column_length_unit = reduce(lambda a, x: a*x, column_breadths)

        # Set the shift axis to vertical or horizontal.
        # vcat causes a row shift, hcat causes a column one.
        row_shift = row_length_unit if cat == "vcat" else 0
        column_shift = column_length_unit if cat == "hcat" else 0

        # Shift the positions of each of the nodes.
        shifted_subtrees = [
            shift_tree_positions(
                subtree,
                row_shift * ii,
                column_shift * ii,
                row_length_unit / row_breadths[ii],
                column_length_unit / column_breadths[ii]
            )
            for ii, subtree in enumerate(subtrees)
        ]

        return {"cat": parent_cat, "nodes": shifted_subtrees}

    else:
        # For a leaf node, wrap it in a container that indicates which cat it
        # belongs to so we know how to stretch it, and inject the start
        # position in the nodes.
        return {"cat": parent_cat, "nodes": [merge(tree, START_POSITION)]}


def flatten_tree(tree):
    if "cat" in tree:
        return listmapcat(flatten_tree, tree["nodes"])
    else:
        # Return the tree as a single element list. This
        # makes listmapcat behave on leaf nodes.
        return [tree]
