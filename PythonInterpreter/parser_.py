'''
This module parses Lej code into an AST bottom-up,
according to the generation rules provided herein.
'''
from node import Node, build_new_nonterm

###############################################################################
# Mapping Nonterminal Nodes
###############################################################################

NONTERMINALS_MAP: dict[str, Node] = \
    {  # Completed lines:
    'CODE-BLOCK CODE-BLOCK': \
    build_new_nonterm('CODE-BLOCK', 0, 0, 'g', 'BOTH', (0, 1), []),
    'ASGN-STMT': \
    build_new_nonterm('CODE-BLOCK', 0, 0, 'g', 'LEFT', (0, 0), []),
    # VAL (logical value) assignments and operations:
    'DEF VAL-VAR AS VAL-EXPR ;': \
    build_new_nonterm('ASGN-STMT', 0, 0, 'g', 'assign_val', (1, 3), []),
    'VAL ID': \
    build_new_nonterm('VAL-VAR', 0, 0, 'g', 'id_assert', (1, 1), []),
    'NOT VAL-SUBEXPR': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'build_not', (1, 1), []),
    'NOT VAL-VAR': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'build_not', (1, 1), []),
    '( VAL-SUBEXPR OR VAL-SUBEXPR )': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'build_or', (1, 3), []),
    '( VAL-VAR OR VAL-SUBEXPR )': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'build_or', (1, 3), []),
    '( VAL-SUBEXPR OR VAL-VAR )': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'build_or', (1, 3), []),
    '( VAL-VAR OR VAL-VAR )': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'build_or', (1, 3), []),
    '( VAL-SUBEXPR AND VAL-SUBEXPR )': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'build_and', (1, 3), []),
    '( VAL-VAR AND VAL-SUBEXPR )': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'build_and', (1, 3), []),
    '( VAL-SUBEXPR AND VAL-VAR )': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'build_and', (1, 3), []),
    '( VAL-VAR AND VAL-VAR )': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'build_and', (1, 3), []),
    '( VAL-VAR )': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'LEFT', (1, 1), []),
    '( VAL-SUBEXPR )': \
    build_new_nonterm('VAL-SUBEXPR', 0, 0, 'g', 'LEFT', (1, 1), []),
    'VAL-SUBEXPR OR VAL-SUBEXPR': \
    build_new_nonterm('VAL-EXPR', 0, 0, 'g', 'build_or', (0, 2), []),
    'VAL-VAR OR VAL-SUBEXPR': \
    build_new_nonterm('VAL-EXPR', 0, 0, 'g', 'build_or', (0, 2), []),
    'VAL-SUBEXPR OR VAL-VAR': \
    build_new_nonterm('VAL-EXPR', 0, 0, 'g', 'build_or', (0, 2), []),
    'VAL-VAR OR VAL-VAR': \
    build_new_nonterm('VAL-EXPR', 0, 0, 'g', 'build_or', (0, 2), []),
    'VAL-SUBEXPR AND VAL-SUBEXPR': \
    build_new_nonterm('VAL-EXPR', 0, 0, 'g', 'build_and', (0, 2), []),
    'VAL-VAR AND VAL-SUBEXPR': \
    build_new_nonterm('VAL-EXPR', 0, 0, 'g', 'build_and', (0, 2), []),
    'VAL-SUBEXPR AND VAL-VAR': \
    build_new_nonterm('VAL-EXPR', 0, 0, 'g', 'build_and', (0, 2), []),
    'VAL-VAR AND VAL-VAR': \
    build_new_nonterm('VAL-EXPR', 0, 0, 'g', 'build_and', (0, 2), []),
    'VAL-SUBEXPR': \
    build_new_nonterm('VAL-EXPR', 0, 0, 'g', 'LEFT', (0, 0), [])}

###############################################################################
# Recursive, Iterative Parser
###############################################################################


def extract_node_names(from_nodes: list[Node]) -> str:
    '''
    summary: Extract the name attribute from `from_nodes` and return them
        as a space-separated string.
    '''
    return ' '.join(node.name for node in from_nodes)


def id_assert(into_tokens: list[Node], with_id: Node) -> list[Node]:
    '''
    summary: Check if there is an ID in `into_tokens`
        with the same literal value as the left child of `with_id`,
        and build a new nonterminal `VAL-VAR` node using that ID node if found.
    '''
    assert isinstance(with_id.left, Node)
    updated_tokens: list[Node] = []
    for node in into_tokens:
        if node.name == 'ID' and node.literal == with_id.left.literal:
            name = with_id.name
            start = node.start
            end = node.end
            scope = node.scope
            xid_node = build_new_nonterm(name, start, end, scope,
                                         'LEFT', (0, 0), [node])
            updated_tokens.append(xid_node)
        else:
            updated_tokens.append(node)
    return updated_tokens


def parse(lej_tokens: list[Node]) -> Node:
    '''
    summary: Iteratively check `lej_tokens` for `NONERMINALS_MAP` matches
        and replace the matched sublist with the corresponding Node
        and the relevant children from the matched sublist.
        Continue this until `lej_tokens` only one nonterminal Node remains,
        and return that Node.

        Along the way, reassert any found `<TYPE>-ID` Node
            as the parent Node type of terminal Nodes with the same ID literal.
    '''
    for j in range(5, 0, -1):
        i = 0
        while i < (len(lej_tokens) - j) + 1:
            tok_slice = lej_tokens[i:i+j]
            tok_names = extract_node_names(tok_slice)
            new_node = None
            if tok_names in NONTERMINALS_MAP:
                nonterm: Node = NONTERMINALS_MAP[tok_names]
                # This production rule only one Left Node.
                if nonterm.children[0] == nonterm.children[1]:
                    new_node = build_new_nonterm(nonterm.name, 0, 0, "?",
                                                 nonterm.action,
                                                 nonterm.children, tok_slice)
                    assert isinstance(new_node.left, Node)
                    s = new_node.left.start
                    e = new_node.left.end
                    scope = new_node.left.scope
                    new_node = build_new_nonterm(new_node.name, s, e, scope,
                                                 new_node.action,
                                                 new_node.children, tok_slice)
                    print(f'L: {new_node.name} -> {new_node.left.name} '
                          f':: {tok_names}',)
                else:  # This production rule has a Left Node and a Right Node.
                    new_node = build_new_nonterm(nonterm.name, 0, 0, "?",
                                                 nonterm.action,
                                                 nonterm.children, tok_slice)
                    assert isinstance(new_node.left, Node)
                    assert isinstance(new_node.right, Node)
                    s = new_node.left.start
                    e = new_node.right.end
                    scope = new_node.left.scope
                    new_node = build_new_nonterm(new_node.name, s, e, scope,
                                                 new_node.action,
                                                 new_node.children, tok_slice)
                    print(f'LR: {new_node.name} -> {new_node.left.name} '
                          f'{new_node.right.name} :: {tok_names}',)

                lej_tokens[i] = new_node
                # id_assert actions occur mid-parse.
                if new_node.action == "id_assert":
                    lej_tokens = id_assert(lej_tokens, new_node)
                print("BEFORE:", i, j, extract_node_names(lej_tokens))
                lej_tokens[i+1:] = lej_tokens[i+j:]
                print("AFTER:", i, j, extract_node_names(lej_tokens))
                return parse(lej_tokens)
            else:
                i += 1
    if len(lej_tokens) > 1:
        # Panic, because the parser couldn't complete the parse.
        print("This collection of tokens cannot be parsed.")
        exit(1)
    return lej_tokens[0]
