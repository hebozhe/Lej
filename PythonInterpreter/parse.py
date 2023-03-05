'''
This module parses Lej code into an AST bottom-up,
according to the generation rules provided herein.
'''
from lex import tokenize
from node import Node, child, make_nonterminal, build_base_node


###############################################################################
# Nonterminal Rules
###############################################################################


def build_rules(parent_name: str, pools: list[list[str]]) \
        -> dict[tuple[str, ...], str]:
    '''
    summary: Use Cartesian products to construct rule-parent key-value pairs.

    params:
    parent_name: str of the name of the parent node.
    pools: list[list[str]] of the rules, in order.

    return: dict[str. str] of the rules.
    '''
    cart_prod: tuple[tuple[str, ...], ...] = (tuple(''),)
    for pool in pools:
        cart_prod = \
            tuple(x + (y,) for x in cart_prod for y in pool)
    return {cp: parent_name for cp in cart_prod}


NAMED_POOLS: dict[str, list[str]] = \
    {
        ':LR-ASSIGNABLE:':
        ['<ASGN-STMT>', '<REASGN-STMT>', '<LR-NODE>'],
        ':BROU-ASSIGNABLE:':
        ['<BROU-SUBEXPR>', '<BROU-ID>', '<NOT-SUBEXPR>', '<OR-EXPR>', '<AND-EXPR>', '<EQ-EXPR>', '<GT-EXPR>', '<LT-EXPR>'],
        ':BROU-EVALUABLE:':
        ['<BROU-SUBEXPR>', '<BROU-ID>', '<NOT-SUBEXPR>', '<OR-SUBEXPR>', '<AND-SUBEXPR>', '<EQ-SUBEXPR>', '<GT-SUBEXPR>', '<LT-SUBEXPR>'],
        ':INT-ASSIGNABLE:':
        ['<INT-SUBEXPR>', '<INT-ID>', '<ADD-EXPR>', '<SUB-EXPR>', '<NEG-SUBEXPR>', '<MUL-EXPR>', '<DIV-EXPR>', '<MOD-EXPR>', '<POW-EXPR>'],
        ':INT-EVALUABLE:':
        ['<INT-SUBEXPR>', '<INT-ID>', '<ADD-SUBEXPR>', '<SUB-SUBEXPR>', '<NEG-SUBEXPR>', '<MUL-SUBEXPR>', '<DIV-SUBEXPR>', '<MOD-SUBEXPR>', '<POW-SUBEXPR>'],
        ':RAT-ASSIGNABLE:':
        ['<RAT-ID>', '<ADD-EXPR>', '<SUB-EXPR>', '<NEG-SUBEXPR>', '<MUL-EXPR>', '<DIV-EXPR>', '<MOD-EXPR>', '<POW-EXPR>', '<DEC-SUBEXPR>'],
        ':RAT-EVALUABLE:':
        ['<RAT-ID>', '<ADD-SUBEXPR>', '<SUB-SUBEXPR>', '<NEG-SUBEXPR>', '<MUL-SUBEXPR>', '<DIV-SUBEXPR>', '<MOD-SUBEXPR>', '<POW-SUBEXPR>', '<DEC-SUBEXPR>'],
}


GRAMMAR_MAP: dict[tuple[str, ...], str] = \
    build_rules(parent_name='<LR-NODE>',
                pools=[NAMED_POOLS[':LR-ASSIGNABLE:'], NAMED_POOLS[':LR-ASSIGNABLE:'],]) | \
    build_rules(parent_name='<ASGN-STMT>',
                pools=[['def'], ['<BROU-ID>'], ['as'], NAMED_POOLS[':BROU-ASSIGNABLE:'], [';'],]
                ) | \
    build_rules(parent_name='<REASGN-STMT>',
                pools=[['change'], ['<BROU-ID>'], ['to'], NAMED_POOLS[':BROU-ASSIGNABLE:'], [';'],]
                ) | \
    build_rules(parent_name='<ASGN-STMT>',
                pools=[['def'], ['<INT-ID>'], ['as'], NAMED_POOLS[':INT-ASSIGNABLE:'], [';'],]
                ) | \
    build_rules(parent_name='<REASGN-STMT>',
                pools=[['change'], ['<INT-ID>'], ['to'], NAMED_POOLS[':INT-ASSIGNABLE:'], [';'],]
                ) | \
    build_rules(parent_name='<ASGN-STMT>',
                pools=[['def'], ['<RAT-ID>'], ['as'], NAMED_POOLS[':RAT-ASSIGNABLE:'], [';'],]
                ) | \
    build_rules(parent_name='<REASGN-STMT>',
                pools=[['change'], ['<RAT-ID>'], ['to'], NAMED_POOLS[':RAT-ASSIGNABLE:'], [';'],]
                ) | \
    build_rules(parent_name='<BROU-ID>',
                pools=[['brou'], ['<ID>'],]
                ) | \
    build_rules(parent_name='<INT-ID>',
                pools=[['int'], ['<ID>'],]
                ) | \
    build_rules(parent_name='<RAT-ID>',
                pools=[['rat'], ['<ID>'],]
                ) | \
    build_rules(parent_name='<NOT-SUBEXPR>',
                pools=[['not'], NAMED_POOLS[':BROU-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<OR-EXPR>',
                pools=[NAMED_POOLS[':BROU-EVALUABLE:'], ['or'], NAMED_POOLS[':BROU-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<OR-SUBEXPR>',
                pools=[['('], NAMED_POOLS[':BROU-EVALUABLE:'], ['or'], NAMED_POOLS[':BROU-EVALUABLE:'], [')'],]
                ) | \
    build_rules(parent_name='<AND-EXPR>',
                pools=[NAMED_POOLS[':BROU-EVALUABLE:'], ['and'], NAMED_POOLS[':BROU-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<AND-SUBEXPR>',
                pools=[['('], NAMED_POOLS[':BROU-EVALUABLE:'], ['and'], NAMED_POOLS[':BROU-EVALUABLE:'], [')'],]
                ) | \
    build_rules(parent_name='<EQ-EXPR>',
                pools=[NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['='], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<EQ-SUBEXPR>',
                pools=[['('], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['='], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], [')'],]
                ) | \
    build_rules(parent_name='<GT-EXPR>',
                pools=[NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['>'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<GT-SUBEXPR>',
                pools=[['('], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['>'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], [')'],]
                ) | \
    build_rules(parent_name='<LT-EXPR>',
                pools=[NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['<'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<LT-SUBEXPR>',
                pools=[['('], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['<'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], [')'],]
                ) | \
    build_rules(parent_name='<ADD-EXPR>',
                pools=[NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['+'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<ADD-EXPR>',
                pools=[NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['<NEG-SUBEXPR>'],]
                ) | \
    build_rules(parent_name='<ADD-SUBEXPR>',
                pools=[['('], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['+'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], [')'],]
                ) | \
    build_rules(parent_name='<SUB-EXPR>',
                pools=[NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['-'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<SUB-SUBEXPR>',
                pools=[['('], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['-'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], [')'],]
                ) | \
    build_rules(parent_name='<NEG-SUBEXPR>',
                pools=[['-'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<MUL-EXPR>',
                pools=[NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['*'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<MUL-SUBEXPR>',
                pools=[['('], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['*'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], [')'],]
                ) | \
    build_rules(parent_name='<DIV-EXPR>',
                pools=[NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['/'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<DIV-SUBEXPR>',
                pools=[['('], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['/'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], [')'],]
                ) | \
    build_rules(parent_name='<MOD-EXPR>',
                pools=[NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['%'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<MOD-SUBEXPR>',
                pools=[['('], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['%'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], [')'],]
                ) | \
    build_rules(parent_name='<POW-EXPR>',
                pools=[NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['^'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'],]
                ) | \
    build_rules(parent_name='<POW-SUBEXPR>',
                pools=[['('], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], ['^'], NAMED_POOLS[':INT-EVALUABLE:'] + NAMED_POOLS[':RAT-EVALUABLE:'], [')'],]
                ) | \
    build_rules(parent_name='<DEC-SUBEXPR>',
                pools=[['<INT-SUBEXPR>'], ['.'], ['<INT-SUBEXPR>'],]
                )


def prioritize(grammar: dict[tuple[str, ...], str]) -> dict[str, dict[tuple[str, ...], str]]:
    '''
    summary: Organize a grammar by the priorities set, where top priority goes last.
    '''
    grammar = {k: v for k, v in grammar.items()}
    priorities: tuple[str, ...] = ('NODE', 'STMT', 'EXPR', 'SUBEXPR', 'ID')
    priority_dict: dict[str, dict[tuple[str, ...], str]] = {p: {} for p in priorities}
    while grammar:
        rule, name = grammar.popitem()
        name_priority: str = name.split('-')[1][:-1]
        priority_dict[name_priority][rule] = name
    return priority_dict


###############################################################################
# Grammar Completion Checks
###############################################################################


def assess_grammar(grammar: dict[tuple[str, ...], str]) -> list[str]:
    '''
    summary: For assistance only, find all of the undefined nodes in a grammar.

    params:
    grammar: dict[tuple[str, ...], str] of the grammar being checked.

    return: list[str] of those nodes whose have either not appeared in rules
        or have not appeared as resulting nodes from those rules.
    '''
    grammar_nodes: list[str] = \
        [n for rule in grammar for n in rule if n[0] == '<' and n[-1] == '>']
    terminals: list[str] = ['<ID>', '<BROU-SUBEXPR>', '<INT-SUBEXPR>', '']
    danglers: list[str] = \
        [gn for gn in grammar_nodes
         if gn not in terminals and gn not in grammar.values()]
    return [gn for i, gn in enumerate(danglers) if gn not in danglers[:i]]


###############################################################################
# Parser
###############################################################################


def typify_id_nodes(nodes: list[Node], typed_id: Node, from_pos: int) -> list[Node]:
    '''
    summary: Starting from the position after the initial typifying of an ID,
        visit all of the nodes that have the same ID name and typify them.

    params:
    nodes: list[Node] of the nodes with possible future matching <ID> nodes.
    typed_id: Node of the name <"TYPE"-ID>.
    from_pos: int indicating the start position from which to begin renaming.

    return: list[Node] of the updated nodes parameter.
    '''
    id_literal: str = typed_id.left.literal
    for dex, node in enumerate(nodes[from_pos:], start=from_pos):
        if not node.is_terminal:  # All <ID> nodes are terminals.
            continue
        if node.literal == id_literal:
            new_nonterm: Node = build_base_node(name=typed_id.name, start=node.start, end=node.end, scope=node.scope)
            new_nonterm = make_nonterminal(the_node=new_nonterm)
            new_nonterm.left = node
            nodes[dex] = new_nonterm
    return nodes


def parse_rec(lej_tokens: list[Node], grammar: dict[tuple[str, ...], str]) -> list[Node]:
    '''
    TODO: Write a docstring.
    '''
    grammar = {r: n for r, n in grammar.items() if any(n.name in r for n in lej_tokens)}
    if not grammar:
        return lej_tokens
    max_rule_len: int = max(len(k) for k in grammar)
    for context_len in range(max_rule_len, 0, -1):
        start: int = 0
        end: int = context_len
        while end < len(lej_tokens) + 1:
            context: list[Node] = lej_tokens[start:end]
            context_key: tuple[str, ...] = tuple(n.name for n in context)
            found_name: str = grammar.get(context_key, '')
            if not found_name:
                start += 1
                end += 1
                continue
            parent: Node = build_base_node(name=found_name, start=context[0].start, end=context[-1].end, scope=context[0].scope)
            parent = make_nonterminal(the_node=parent)
            parent = child(the_node=parent, context=context)
            if context_len == 2 and context[-1].name == '<ID>':
                lej_tokens = typify_id_nodes(nodes=lej_tokens, typed_id=parent, from_pos=end)
            return parse_rec(lej_tokens=lej_tokens[:start], grammar=grammar) + [parent] + parse_rec(lej_tokens=lej_tokens[end:], grammar=grammar)
    return lej_tokens


def parse(lej_tokens: list[Node]) -> Node:
    '''
    summary: From the bottom up, gather nodes and collect them into trees,
        starting from the shortest rules and ending with the longest rules.

    params:
    lej_tokens: list[Node] of a tokenized Lej program.

    return: Node of the fully parsed tree.
    '''
    priority_grammar: dict[str, dict[tuple[str, ...], str]] = prioritize(grammar=GRAMMAR_MAP)
    while priority_grammar:
        priority, grammar = priority_grammar.popitem()
        len_bef: int = 0
        len_aft: int = -1
        while len_aft < len_bef:
            len_bef = len(lej_tokens)
            lej_tokens = parse_rec(lej_tokens=lej_tokens, grammar=grammar)
            len_aft = len(lej_tokens)
        print(priority, '->', [n.name for n in lej_tokens])
    if len(lej_tokens) > 1:
        print('This Lej program could not be parsed.')
        # print(set(GRAMMAR_MAP.values()))
        exit(1)
    return lej_tokens[0]


if __name__ == '__main__':
    print(len([print(f'\n"{"".join(k)}" -> "{v}"') for k, v in GRAMMAR_MAP.items()]))
    print(assess_grammar(grammar=GRAMMAR_MAP))
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
        def brou isUnsureStill as (isUnsure or isAlsoUnsure) or U;

        def int firstInt as 12;
        change firstInt to 13 + firstInt;
        def rat firstRat as (firstInt / 2.2) % (5.8 / 8.8);
        `def brou areEqual as (firstInt = 12) and ((firstRat > 3) or (firstRat < 3));`
        '''
    print(parse(lej_tokens=tokenize(lej_pgrm=sample_program)))
