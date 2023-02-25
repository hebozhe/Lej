'''
This module defines and updates the Node struct/object.
'''
###############################################################################
# Nodes (Terminals and Nonterminals)
###############################################################################


class Node:
    '''
    summary: Define Nodes to cover all use needs.
    '''
    # Both terminals and nonterminals:
    name: str
    start: int
    end: int
    is_terminal: bool
    scope: str
    # Terminals only:
    literal: str
    u_count: int  # Only for 'U' Brouwerians.
    # Nonterminals only:
    left: 'Node'
    right: 'Node'


def build_base_node(name: str, start: int, end: int, scope: str) -> Node:
    '''
    summary: Build a fresh node given the descriptors.

    params:
    name: str indicating the name of the node.
    start: int indicating which position in the Lej code begins the node.
    end: int indicating which position in the Lej node ends the node.

    return: Node with the base attributes.
    '''
    base_node: Node = Node()
    base_node.name = name
    base_node.start = start
    base_node.end = end
    base_node.scope = scope
    return base_node


EmptyNode: Node = Node()


def make_terminal(the_node: Node, literal: str) -> Node:
    '''
    summary: Add data that only applies to terminal nodes.

    params:
    node: Node to be asserted as terminal.
    literal: str indicating the literal characters that comprise the terminal.

    return: Node of node with the extra terminal attributes.
    '''
    the_node.is_terminal = True
    the_node.literal = literal
    return the_node


def make_nonterminal(the_node: Node) -> Node:
    '''
    summary: Add data that only applies to nonterminal nodes.

    params:
    node: Node to be asserted as nonterminal.

    return: Node of node with the extra nonterminal attributes.
    '''
    the_node.is_terminal = False
    return the_node


def child(the_node: Node, context: list[Node]) -> Node:
    '''
    summary: Give left and right children to nonterminal Node classes
        with the children attribute defined (via make_terminal()).

    params:
    node: Node to be given left and right children.
    context: list[Node] from which the children are to be extracted.

    return: Node of node with the children.
    '''
    assert not the_node.is_terminal, \
        f'The node of name {the_node.name} is terminal, thus childless.'
    children: list[Node] = \
        [n for n in context if n.name[0] == '<' and n.name[-1] == '>']
    assert 0 < len(children) < 3, \
        f'The context {[n.name for n in context]} has {children} child nodes, '\
        'when it should have just 1 or 2.'
    the_node.left = children[0]
    if len(children) == 1:
        return the_node
    the_node.right = children[-1]
    return the_node
