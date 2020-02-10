# Syntax Reference

This is a reference manual for the SVL syntax.

Notation (these are not syntax):

* `[ ]` means optional
* `|` is a logical OR.
* `{ }` is for grouping logical ORs when it's not obvious.
* `...` means the previous pattern is repeated.

If this method turns out to be incomprehensible I'll figure something else out.

## A Repeat of Boring Stuff

I mean this whole article is boring stuff, but this stuff is _really_ boring.

1. All keywords in SVL are case-**insensitive**, but field names, file names, and anything in quotes are not. By convention I will capitalize keywords but it's not required.
2. Comments start with `--` and extend to the end of the line.
3. All dataset and field names (basically anything not in quotes) must start with an underscore or letter, and can only contain letters, underscores or digits.
4. SVL is not sensitive to tabs or newlines. The entire program could be written on one line if you wanted.

## Scripts

Schematically, an entire SVL program looks like this.

```
[DATASETS dataset declaration, ...]
chart | CONCAT(chart, ...) | (chart, ...),
...
```

Dataset declarations and charts are described below.

`DATASETS` is optional.
After that you can create one or more charts, each of which is a chart by itself, a horizontal concatenation of one or more charts, or a vertical concatenation of one or more charts.

## `DATASETS`

Dataset declarations are made up of file declarations or SQL declarations.

```
DATASETS
    identifier {file_path | SQL sql_query},
    ...
```

`sql_query` and `file_path` are double quoted strings.

**NOTE** There has to be at least one file in the final program, which can either be declared in the script or passed in via the command line.

## `SCATTER`

```
SCATTER dataset_identifier
    {
        x_axis |
        y_axis |
        [FILTER quoted_string] |
        [TITLE quoted_string] |
        [split_by] |
        [color_by]
    },
    ...
```

Scatter requires an `X` and `Y` axis.
The quoted string following `FILTER` must be a valid SQL WHERE expression.
`SPLIT BY` and `COLOR BY` cannot both be present.

## `HISTOGRAM`

```
HISTOGRAM dataset_identifier
    {
        x_axis |
        y_axis |
        [FILTER quoted_string] |
        [TITLE quoted_string] |
        [split_by] |
        [STEP number] |
        [BINS integer]
    },
    ...
```

`STEP` will take any positive floating point number or integer.
`BINS` will take any positive integer.
`HISTOGRAM` can have an `X` or `Y` axis, but not both.
The quoted string following `FILTER` must be a valid SQL WHERE expression.

## `LINE`

```
LINE dataset_identifier
    {
        x_axis |
        y_axis |
        [FILTER quoted_string] |
        [TITLE quoted_string] |
        [split_by] |
        [color_by]
    },
    ...
```

`LINE` requires both an `X` and `Y` axis.
The quoted string following `FILTER` must be a valid SQL WHERE expression.
`SPLIT BY` and `COLOR BY` cannot both be present.

## `BAR`

```
BAR dataset_identifier
    {
        x_axis |
        y_axis |
        [FILTER quoted_string] |
        [TITLE quoted_string] |
        [split_by] |
        [color_by]
    }
```

`BAR` requires both an `X` and `Y` axis.
The quoted string following `FILTER` must be a valid SQL WHERE expression.
`SPLIT BY` and `COLOR BY` cannot both be present.

## `PIE`

```
PIE dataset_identifier
    {
        axis |
        [FILTER quoted_string] |
        [TITLE quoted_string] |
        [HOLE number]
    },
    ...
```

`PIE` requires one `AXIS`.
The quoted string following `FILTER` must be a valid SQL WHERE expression.
`HOLE` must take a floating point number between zero and one.

## `NUMBER`

```
NUMBER dataset_identifier
    {
        value |
        [FILTER quoted_string] |
        [TITLE quoted_string]
    },
    ...
```

`NUMBER` requires one `VALUE`.
If the provided value doesn't resolve to a single number, SVL will raise an error.

## `X`, `Y`, `AXIS`. `VALUE`

`X`, `Y` and `AXIS` all take the same properties.
`VALUE` can only be aggregated.
It does not accept temporal modifiers, labels or sorts.

```
{X | Y | AXIS | VALUE} {field_identifier | TRANSFORM quoted_string}
[
    AGG | BY temporal | LABEL quoted_string | SORT {ASC | DESC}
], ...
```

The quoted string following `TRANSFORM` must be a valid SQL SELECT expression.
`AGG` is one of `COUNT`, `MIN`, `MAX`, `AVG`, `SUM`.
Temporal is one of `YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`, `SECOND`.

## `SPLIT BY`

```
SPLIT BY {field_identifier | TRANSFORM quoted_string} [BY temporal | LABEL quoted_string], ...
```

The quoted string following `TRANSFORM` must be a valid SQL SELECT expression.
Temporal is one of `YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`, `SECOND`.
For the Plotly backend (currently the only one available), `LABEL` is a no-op, since adding legend titles to charts is fairly challenging for Plotly plots.

## `COLOR BY`

```
COLOR BY {field_identifier | TRANSFORM quoted_string}
[
    AGG | BY temporal | LABEL quoted_string | color_scale
],
...
```

The quoted string following `TRANSFORM` must be a valid SQL SELECT expression.
`AGG` is one of `COUNT`, `MIN`, `MAX`, `AVG`.
Temporal is one of `YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`, `SECOND`.
Color scale is a quoted string that corresponds to (for now) a [Plotly color scale](https://plot.ly/javascript/colorscales/).