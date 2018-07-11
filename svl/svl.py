import lark
import pkg_resources

debug_parser = lark.Lark(
    pkg_resources.resource_string("resources", "svl.lark").decode("utf-8")
)


def parse_svl(svl_string):
    return debug_parser.parse(svl_string)
