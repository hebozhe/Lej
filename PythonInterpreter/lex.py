'''
This module tokenizes Lej code.
'''
from node import (build_base_node, Node, make_terminal)


###############################################################################
# Building Terminal Nodes
###############################################################################


def build_litnamed_node(start: int, end: int, literal: str, scope: str) -> Node:
    '''
    summary: Build a Node for nodes whose literals are its name.

    params:
    start: int indicating which character in the Lej code begins the node.
    end: int indicating which character in the Lej code ends the node.
    literal: str indicating the literal characters that comprise the terminal.
    scope: str indicating the scope of the node.

    return Node containing the name 'def', 'as', 'change', or 'to'.
    '''
    base_node: Node = build_base_node(name=literal, start=start, end=end, scope=scope)
    return make_terminal(the_node=base_node, literal=literal)


def build_brousubexpr_node(start: int, end: int, literal: str, scope: str) -> Node:
    '''
    summary: Build a Node for Brouwerian primitives 'T', 'U', and 'F'.

    params:
    start: int indicating which character in the Lej code begins the node.
    end: int indicating which character in the Lej code ends the node.
    literal: str indicating the literal characters that comprise the terminal.
    scope: str indicating the scope of the node.

    return Node containing the name '<BROU-SUBEXPR>',
        plus a u_count attribute if its name is 'U', where its count indicates
        the number of unsure Brouwerians present in the program.
    '''
    base_node: Node = \
        build_base_node(name='<BROU-SUBEXPR>', start=start, end=end, scope=scope)
    term_node: Node = make_terminal(the_node=base_node, literal=literal)
    return term_node


def is_legal_id_token(token: str) -> bool:
    '''
    summary: Determine whether a given token is legally able be an ID node.
        Legal ID tokens start with a lowercase letter and use only camel casing
        with numeric values.
    '''
    if token[0] not in 'abcdefghijklmnopqrstuvwxyz':
        return False
    alnums: str = \
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return all(c in alnums for c in token)


def build_id_node(start: int, end: int, literal: str, scope: str) -> Node:
    '''
    summary: Build a Node for legal identifiers.
    params:
    start: int indicating which character in the Lej code begins the node.
    end: int indicating which character in the Lej code ends the node.
    literal: str indicating the literal characters that comprise the terminal.
    scope: str indicating the scope of the node.

    return Node containing the name '<ID>'.
    '''
    base_node: Node = \
        build_base_node(name='<ID>', start=start, end=end, scope=scope)
    return make_terminal(the_node=base_node, literal=literal)


def build_intsubexpr_node(start: int, end: int, literal: str, scope: str) -> Node:
    '''
    summary: Build an integer subexpression Node for integer literals.

    params:
    start: int indicating which character in the Lej code begins the node.
    end: int indicating which character in the Lej code ends the node.
    literal: str indicating the literal characters that comprise the terminal.
    scope: str indicating the scope of the node.

    return Node containing the name '<INT-SUBEXPR>'.
    '''
    base_node: Node = \
        build_base_node(name='<INT-SUBEXPR>', start=start, end=end, scope=scope)
    term_node: Node = make_terminal(the_node=base_node, literal=literal)
    return term_node


def build_delim_node(start: int, end: int, literal: str, scope: str) -> Node:
    '''
    summary: Build a Node for delimiter keywords.

    params:
    start: int indicating which character in the Lej code begins the node.
    end: int indicating which character in the Lej code ends the node.
    literal: str indicating the literal characters that comprise the terminal.
    scope: str indicating the scope of the node.

    return Node containing the name ' ', '[', ']', '(', ')', ',', ';', or ':'.
    '''
    name: str = ' ' if literal[0] in ' \t\n' else literal
    base_node: Node = \
        build_base_node(name=name, start=start, end=end, scope=scope)
    return make_terminal(the_node=base_node, literal=literal)


###############################################################################
# Mapping Terminal Nodes
###############################################################################


TERMINALS_MAP: dict[str, list[str]] = {
    # Nodes whose names are the literals:
    'KEYWORDS':
    [
        # Assignment and reassignment keywords:
        'def', 'as', 'change', 'to',
        # Type declarations:
        'brou', 'int', 'rat',
        # Logical operators:
        'and', 'or', 'not',
    ],
    # <ID> nodes are mined separately:
    # <INT-SUBEXPR> nodes are mined separately:
    # Brouwerians:
    '<BROU-SUBEXPR>':
    [
        # Primitive truth-values:
        'T', 'U', 'F',
    ],
    # Single-character symbols:
    'SYMBOLS':
    [
        # Arithmetic operators:
        '+', '-', '*', '/', '%', '.',
        # Arithmetic evaluators:
        '=', '>', '<',
        # Delimiters:
        '[', ']', '(', ')', ',', ';', ':',
    ],
    'WHITESPACES':
    [
        ' ', '\t', '\n',
    ]
}

###############################################################################
# Tokenize a Program
###############################################################################


def choose_alnum_build(token: str, start: int, end: int, scope: str) -> Node:
    '''
    summary: Determine which Node kind should be generated
        from the alphanumeric strings that comprise nodes.

    params:
    token: str to be checked against TERMINALS_MAP.
    start: int indicating which character in the Lej code begins the node.
    end: int indicating which character in the Lej code ends the node.
    scope: str indicating the scope of the node.

    return: Node of the correct kind.
    '''
    if token in TERMINALS_MAP['<BROU-SUBEXPR>']:
        return build_brousubexpr_node(start=start, end=end, literal=token, scope=scope)
    if token in TERMINALS_MAP['KEYWORDS']:
        return build_litnamed_node(start=start, end=end, literal=token, scope=scope)
    if is_legal_id_token(token=token):
        return build_id_node(start=start, end=end, literal=token, scope=scope)
    print(f'The token "{token}" at [{start} {end}] is not legal Lej.')
    exit(1)


def set_u_counts(terminals: list[Node]) -> list[Node]:
    '''
    summary: Visit all of the terminal nodes in a list of terminals
        and give it a u_count based on its order in the program
        if it's a 'U' Brouwerian node.

    params:
    terminals: list[Node] of terminal nodes.

    return: list[Node] of terminals, with the relevant 'U' Brouwerian
        u_count values placed.
    '''
    unknowns_count: int = 1
    for node in terminals:
        if node.literal == 'U':
            node.u_count = unknowns_count
            unknowns_count += 1
    return terminals


def tokenize(lej_pgrm: str) -> list[Node]:
    '''
    summary: Going through every character in the string of a Lej program,
        spit out correct terminal nodes from the program, or throw an error
        if something is syntactically wrong.

    params:
    lej_prog: str of a program

    return: list[Node] of the terminals of the language.
    '''
    terminals: list[Node] = []
    pos: int = 0
    prog_len: int = len(lej_pgrm)
    digits: str = '0123456789'
    lowers: str = 'abcdefghijklmnopqrstuvwxyz'
    uppers: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alnums: str = lowers + uppers + digits
    spaces: str = ''.join(TERMINALS_MAP['WHITESPACES'])
    scopes: list[str] = ['global']
    # TODO: Update scopes based on function calls and returns.
    while pos < prog_len:
        start = pos
        # Initial backtick '`' characters set off comments.
        if lej_pgrm[pos] == '`':
            pos += 1
            while lej_pgrm[pos] != '`':
                pos += 1
                if pos == prog_len:
                    print('You are missing a closing \'`\' character in a comment.')
                    exit(1)
            pos += 1
            continue
        # Initial whitespaces convert to a single delimiter node.
        elif lej_pgrm[pos] in spaces:
            while pos < prog_len and lej_pgrm[pos] in spaces:
                pos += 1
            continue
        # Initial symbols are all self-named.
        elif lej_pgrm[pos] in TERMINALS_MAP['SYMBOLS']:
            pos += 1
            token = lej_pgrm[start]
            terminals.append(build_litnamed_node(start=start, end=pos, literal=token, scope=scopes[-1]))
        # Initial digit strings convert to <INT-SUBEXPR>.
        elif lej_pgrm[pos] in digits:
            while pos < prog_len and lej_pgrm[pos] in digits:
                pos += 1
            end = pos
            token = lej_pgrm[start:end]
            terminals.append(build_intsubexpr_node(start=start, end=end, literal=token, scope=scopes[-1]))
        # Initial alphabetic strings convert to keywords or <ID>.
        elif lej_pgrm[pos] in alnums:
            while pos < prog_len and lej_pgrm[pos] in alnums:
                pos += 1
            end = pos
            token = lej_pgrm[start:end]
            terminals.append(choose_alnum_build(token=token, start=start, end=end, scope=scopes[-1]))
        else:
            print(f'"{lej_pgrm[pos]}" at position {pos} is invalid.')
            exit(1)
    terminals = set_u_counts(terminals=terminals)
    return terminals


if __name__ == '__main__':
    sample_program: str = \
        '''
        def brou isTrue as T;
        def brou isAlsoTrue as T;
        def brou isUnsure as U;
        def brou isAlsoUnsure as U;
        def brou isFalse as F;
        def brou isAlsoFalse as F;

        change isFalse to isFalse and isTrue;
        change isFalse to isFalse or isFalse;
        change isFalse to not isTrue;
        change isFalse to not (isTrue or isFalse);

        def int firstInt as 12;
        def rat firstRat as firstInt / 2.2;
        def brou areEqual as (firstInt = 12) and (firstRat > 3);
        '''
    print([f'{node.name}' for node in tokenize(lej_pgrm=sample_program)])
