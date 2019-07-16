import lark
import pkg_resources

from toolz import merge, get
from lark import UnexpectedInput, UnexpectedCharacters

from svl.compiler.errors import SVL_SYNTAX_ERRORS, SvlSyntaxError


class SVLTransformer(lark.Transformer):
    def visualization(self, items):
        return merge(*items)

    def datasets(self, items):
        return {"datasets": merge(*items)}

    def file_dataset(self, items):
        return {items[0]: {"file": items[1][1:-1]}}

    def sql_dataset(self, items):
        return {items[0]: {"sql": items[1][1:-1]}}

    def charts(self, items):
        return {"vcat": items}

    def vcat(self, items):
        return {"vcat": items}

    def hcat(self, items):
        return {"hcat": items}

    def chart(self, items):
        return merge(*items)

    def title(self, items):
        return {"title": str(items[0])[1:-1]}

    def filter(self, items):
        return {"filter": str(items[0])[1:-1]}

    def xy_chart(self, items):
        return merge(*items)

    def histogram_chart(self, items):
        return merge({"type": "histogram"}, *items)

    def pie_chart(self, items):
        return merge({"type": "pie"}, *items)

    def markxy(self, items):
        return {"type": str(items[0]).lower()}

    def data(self, items):
        return {"data": str(items[0])}

    def label(self, items):
        return {"label": str(items[0])[1:-1]}

    def bins(self, items):
        return {"bins": int(items[0])}

    def step(self, items):
        return {"step": float(items[0])}

    def hole(self, items):
        return {"hole": float(items[0])}

    def dimensions(self, items):
        return merge(*items)

    def x(self, items):
        return {"x": merge(*items)}

    def y(self, items):
        return {"y": merge(*items)}

    def color_by(self, items):
        return {"color_by": merge(*items)}

    def axis(self, items):
        return {"axis": merge(*items)}

    def split_by(self, items):
        return {"split_by": merge(*items)}

    def field(self, items):
        return {"field": str(items[0])}

    def temporal(self, items):
        return {"temporal": str(items[0]).upper()}

    def transform(self, items):
        # Don't touch the case of the transforms - that gets passed to SQL
        # as-is.
        return {"transform": str(items[0])[1:-1]}

    def aggregation(self, items):
        return {"agg": str(items[0]).upper()}

    def sort(self, items):
        return {"sort": str(items[0]).upper()}

    def color_scale(self, items):
        return {"color_scale": str(items[0][1:-1])}


debug_parser = lark.Lark(
    pkg_resources.resource_string("resources", "svl.lark").decode("utf-8")
)


parser = lark.Lark(
    pkg_resources.resource_string("resources", "svl.lark").decode("utf-8"),
    parser="lalr",
    transformer=SVLTransformer(),
)


def parse_svl(svl_string, debug=False, **kwargs):
    if debug:
        return debug_parser.parse(svl_string)
    else:

        try:
            parsed_svl = parser.parse(svl_string)
        except (UnexpectedInput, UnexpectedCharacters) as u:
            exception_class = u.match_examples(parser.parse, SVL_SYNTAX_ERRORS)
            if not exception_class:
                raise SvlSyntaxError(
                    u.get_context(svl_string), u.line, u.column
                )
            else:
                raise exception_class(
                    u.get_context(svl_string), u.line, u.column
                )

        parsed_svl["datasets"] = merge(
            # Either DATASETS is there or is empty.
            get("datasets", parsed_svl, {}),
            # Convert each kwarg into a file dataset spec.
            {k: {"file": v} for k, v in kwargs.items()},
        )

        return parsed_svl
