'''
This module defines and updates the Node struct/object.
'''
from typing import Self

###############################################################################
# Nodes (Terminals and Nonterminals)
###############################################################################


class Node:
    '''
    summary: Define a Node
    '''

    def __init__(self, name: str, start: int, end: int, scope: str,
                 action: str, terminal: bool, literal: str,
                 children: tuple[int, int], left: Self | None,
                 right: Self | None):
        self.name = name
        self.start = start
        self.end = end
        self.scope = scope
        self.action = action
        self.terminal = terminal
        self.literal = literal
        self.children = children
        self.left = left
        self.right = right


def build_new_term(name: str, start: int, end: int, scope: str,
                   action: str, literal: str) -> Node:
    '''
    summary: Builds and returns a new terminal Node.
    '''
    return Node(name, start, end, scope, action, True, literal,
                tuple(), None, None)


# Builds a new nonterminal Node.
def build_new_nonterm(name: str, start: int, end: int,
                      scope: str, action: str, children: tuple[int, int],
                      match_span: list[Node]) -> Node:
    '''
    summary: Builds and returns a new nonterminal Node.
    '''
    left = right = None
    # Leave left and right undefined until a long enough match_span arises.
    if len(match_span) < children[1] + 1:
        left = right = None
    else:
        if children[0] == children[1]:
            left = match_span[children[0]]
            right = None
        else:
            left = match_span[children[0]]
            right = match_span[children[1]]
    return Node(name, start, end, scope, action, False, '',
                children, left, right)
