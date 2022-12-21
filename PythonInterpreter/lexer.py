'''
This module tokenizes Lej code.
'''
from node import build_new_term, Node

###############################################################################
# Mapping Terminal Nodes
###############################################################################


TERMINALS_MAP: dict[str, Node] = {
    # Assignment keywords:
    'def': build_new_term('DEF', 0, 0, 'g', '', 'def'),
    'as': build_new_term('AS', 0, 0, 'g', '', 'as'),
    # Identifiers are found separately.
    # Logical literals:
    'T': build_new_term('VAL-SUBEXPR', 0, 0, 'g', 'build_true', 'T'),
    'U': build_new_term('VAL-SUBEXPR', 0, 0, 'g', 'build_unsure', 'U'),
    'F': build_new_term('VAL-SUBEXPR', 0, 0, 'g', 'build_false', 'F'),
    # Logical operators:
    'and': build_new_term('AND', 0, 0, 'g', '', 'and'),
    'or': build_new_term('OR', 0, 0, 'g', '', 'or'),
    'not': build_new_term('NOT', 0, 0, 'g', '', 'not'),
    # Delimiters:
    ';': build_new_term(';', 0, 0, 'g', '', ';'),
    '(': build_new_term('(', 0, 0, 'g', '', '('),
    ')': build_new_term(')', 0, 0, 'g', '', ')'),
    # Type keywords:
    'val': build_new_term('VAL', 0, 0, 'g', '', 'val'),
}


def build_new_id_node(start: int, end: int, scope: str, literal: str) -> Node:
    '''
    summary: Builds and returns a new terminal ID Node.
    '''
    return build_new_term('ID', start, end, scope, '', literal)


def can_be_new_id(s: str) -> bool:
    '''
    summary: Checks whether a given string can legally be an ID.
    '''
    if s in TERMINALS_MAP:
        return False
    if not ('a' <= s[0] <= 'z'):
        return False
    for c in s:
        if not (('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9')):
            return False
    return True


###############################################################################
# Tokenizer
###############################################################################

def tokenize(this_path: str) -> list[Node]:
    '''
    summary: Tokenize the strings read from this_path
        and return the list of terminal Node objects.
    '''
    token_arr: list[Node] = []
    with open(file=this_path, mode='r', encoding='UTF-8') as lej_file:
        lej_text = lej_file.read() + ' '
    whitespaces = [' ', '\n']
    i = 0
    cur_scope = 'g'
    for j in range(1, len(lej_text)):
        # Skip slice-leading whitespace characters.
        while lej_text[i] in whitespaces:
            i += 1
            if i == j:
                break
        # Append identifiers in current chunk.
        cur_chunk = lej_text[i:j]
        next_chunk = lej_text[i:j+1]
        print(cur_chunk)
        # Skip empty chunks.
        if cur_chunk == '':
            continue
        # Check for new terminal ID nodes.
        if can_be_new_id(cur_chunk):
            # Skip if the next chunk can be an identifier, too.
            if can_be_new_id(next_chunk):
                continue
            # Skip if the next chunk can be a primitive.
            if next_chunk in TERMINALS_MAP:
                continue
            id_node = build_new_id_node(i, j, cur_scope, cur_chunk)
            token_arr.append(id_node)
            i = j
            continue
        # Append primitive terminal Nodes.
        if cur_chunk in TERMINALS_MAP:
            # Skip if the next chunk can be an identifier.
            if can_be_new_id(next_chunk):
                continue
            tn = TERMINALS_MAP[cur_chunk]
            next_t_node = \
                build_new_term(tn.name, i, j, cur_scope, tn.action, cur_chunk)
            token_arr.append(next_t_node)
            i = j
            continue
        # Panic, because the character is foreign.
        print(f'This chunk could not be tokenized: {cur_chunk}')
        exit(1)
    return token_arr
