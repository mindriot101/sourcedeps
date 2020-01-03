import networkx as nx
import logging
from astroid import parse, nodes


# TODO: handle whether calls are function calls or object constructions

logger = logging.getLogger("sourcedeps")


def parse_tree(graph, node):
    logger.debug("got %r node", node)

    if hasattr(node, "body") and not isinstance(node, nodes.Const):
        logger.debug("node has body, iterating over children")
        # This node must be a container with a body, so iterate through the child statements
        children = node.body

        for child in children:
            parse_tree(graph, child)

    else:

        if isinstance(node, nodes.Expr):
            logger.debug("parsing expression")
            parse_tree(graph, node.value)
        elif isinstance(node, nodes.Call):
            logger.debug("parsing call")
            func = node.func

            # Handle if the function is a method
            if isinstance(func, nodes.Attribute):
                logger.debug("attribute assignment")
                method_name = func.attrname
                object_name = func.expr.name

                src = node.frame().name
                dst = f"{object_name}.{method_name}"

            else:
                logger.debug("not attribute assignment")
                name = func.name

                src = node.frame().name
                dst = name

            logger.debug("adding edge %s -> %s", src, dst)
            graph.add_edge(src, dst)
        elif isinstance(node, nodes.Assign):
            logger.debug("assignment")
            parse_tree(graph, node.value)
        else:
            logger.debug("got unknown node: %r", node)
            return


def parse_source(filename: str) -> nx.Graph:
    with open(filename, "r") as infile:
        source = infile.read()

    module = parse(source)
    g = nx.DiGraph()

    parse_tree(g, module)

    return g
