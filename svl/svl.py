import lark
import pkg_resources

from toolz import merge, partition_all


class SVLTransformer(lark.Transformer):

    def visualization(self, items):
        return merge(*items)

    def datasets(self, items):
        return {
            "datasets": dict(
                map(
                    lambda x: (str(x[0]), x[1][1:-1]),
                    partition_all(2, items)
                )
            )
        }

    def charts(self, items):
        return {
            "vcat": items
        }

    def vcat(self, items):
        return {
            "vcat": items
        }

    def hcat(self, items):
        return {
            "hcat": items
        }

    def chart(self, items):
        return merge(*items)

    def title(self, items):
        return {"title": str(items[0])[1:-1]}

    def filter(self, items):
        return {"filter": str(items[0])[1:-1]}

    def xy_chart(self, items):
        return merge(*items)

    def histogram_chart(self, items):
        return merge({"type": "histogram"}, *items[1:])

    def pie_chart(self, items):
        return merge({"type": "pie"}, *items[1:])

    def markxy(self, items):
        return {"type": str(items[0]).lower()}

    def data(self, items):
        return {"data": str(items[0])}

    def histogram_opts(self, items):
        return merge(*items)

    def pie_opts(self, items):
        return merge(*items)

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

    def split_by(self, items):
        return {"split_by": merge(*items)}

    def field(self, items):
        if (len(items) == 1) and (isinstance(items[0], dict)):
            return {"field": items[0]}
        elif len(items) == 1:
            return {"field": str(items[0])}
        else:
            return merge(
                {"field": str(items[0])},
                *items[1:]
            )

    def temporal(self, items):
        return {"temporal": str(items[0])}

    def transform(self, items):
        return {"transform": str(items[0])[1:-1]}

    def aggregation(self, items):
        return {"agg": str(items[0])}


debug_parser = lark.Lark(
    pkg_resources.resource_string("resources", "svl.lark").decode("utf-8")
)


parser = lark.Lark(
    pkg_resources.resource_string("resources", "svl.lark").decode("utf-8"),
    parser="lalr",
    transformer=SVLTransformer()
)


def parse_svl(svl_string, debug=False):
    if debug:
        return debug_parser.parse(svl_string)
    else:
        return parser.parse(svl_string)
