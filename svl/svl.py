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

    def mark2d(self, items):
        return {"type": str(items[0]).lower()}

    def mark1d(self, items):
        return {"type": str(items[0]).lower()}

    def data(self, items):
        return {"data": str(items[0])}

    def mark1d_opts(self, items):
        return merge(*items)

    def bins(self, items):
        return {"bins": int(items[0])}

    def step(self, items):
        return {"step": float(items[0])}

    def dimensions(self, items):
        return merge(*items)

    def x(self, items):
        return {"x": merge(*items)}

    def y(self, items):
        return {"y": merge(*items)}

    def color(self, items):
        return {"color": merge(*items)}

    def field(self, items):
        return {"field": str(items[0])}

    def temporal(self, items):
        return {"temporal": str(items[0])}

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
