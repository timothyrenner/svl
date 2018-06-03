import lark
import pkg_resources

from toolz import merge, partition_all, thread_last


def unquote_string(string):
    return string[1:-1]


class SVLToVegaLiteTransformer(lark.Transformer):

    
    def visualization(self, items):
        return merge(
            {"$schema": "https://vega.github.io/schema/vega-lite/v2.0.json"},
            *items
        )

    
    def datasets(self, items):
        return {
            "datasets": dict(
                map(
                    lambda x: (str(x[0]), unquote_string(x[1])),
                    partition_all(2, items)
                )
            )
        }
    
    
    def views(self, items):
        return {
            "vconcat": items
        }


    def hconcat(self, items):
        return {
            "hconcat": items
        }


    def vconcat(self, items):
        return {
            "vconcat": items
        }


    def view(self, items):
        return merge(*items)


    def encoding(self, items):
        return {
            "encoding": merge(*items)
        }


    def x(self, items):
        return {
            "x": merge(*items)
        }

    
    def y(self, items):
        return {
            "y": merge(*items)
        }

    
    def mark(self, items):
        return {"mark": str(items[0]).lower()}

    
    def field(self, items):
        return {"field": str(items[0])}

    
    def bin(self, items):
        if len(items) == 0:
            return {"bin": True}
        else:
            return {"bin": {"step": items[0]}}

    
    def aggregation(self, items):
        return {
            "aggregate": unquote_string(str(items[0])),
            "type": "quantitative"
        }

    
    def field_type(self, items):
        return {"type": unquote_string(str(items[0]))}
    
    
    def data(self, items):
        return {
            "data": {
                "name": str(items[0])
            }
        }

    
# This parser has the transformer embedded for speed.
parser = lark.Lark(
    pkg_resources.resource_string("resources", "svl.lark").decode('utf-8'),
    parser="lalr",
    transformer=SVLToVegaLiteTransformer()
)


# This one returns the tree to make it easier to debug.
debug_parser = lark.Lark(
    pkg_resources.resource_string("resources", "svl.lark").decode("utf-8")
)


def parse_svl(svl_string, debug=False):
    if debug:
        return debug_parser.parse(svl_string)
    else:
        return parser.parse(svl_string)

