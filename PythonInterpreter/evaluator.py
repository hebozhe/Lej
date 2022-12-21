'''
The evaluator is where the Lej AST is walked and interpreted.
'''
from typing import Any
from node import Node

###############################################################################
# Assignment Storage
###############################################################################

ASSIGN_MAP: dict[str, Any] = {'unsure_count': 0}

###############################################################################
# Handling val Assignments and Operations
###############################################################################


def build_true() -> list[int]:
    '''
    summary: Build and return the intruitionistically `True` value.
    '''
    return [2]


def build_false() -> list[int]:
    '''
    summary: Build and return the intuitionistically `False` value.
    '''
    return [0]


def build_unsure() -> list[int]:
    '''
    summary: Build and return the intuitionistically `Unsure` value.
        An `Unsure` value houses a unique Boolean truth-table column,
        which is devised based on the number of previous `Unsure` values.
    '''
    unsure_count = ASSIGN_MAP.get('unsure_count', None)
    assert isinstance(unsure_count, int)
    if unsure_count is not None:
        unsure_count += 1
        ASSIGN_MAP['unsure_count'] = unsure_count
        # TODO: Why the hell is this quadrupling instead of doubling?
        u_val_len = 2 << (unsure_count - 1)
        print(f'unsureCount is now {unsure_count},',
              f'and uValLen is now {u_val_len}.')
        u_val: list[int] = [1]
        t = 2
        f = 0
        for _ in range(u_val_len // 2):
            u_val.append(t)
        for _ in range(u_val_len // 2):
            u_val.append(f)
        return u_val
    print('unsure_count is missing.')
    exit(1)
    return []


def double_bools(of_val: list[int]) -> list[int]:
    '''
    summary: Double the length of `of_val` by appending a copy of
        `of_val[1:]` to the end of `of_val`.
    '''
    return of_val + of_val[1:]


def halve_bools(of_val: list[int]) -> list[int]:
    '''
    summary: If the right half of `of_val` is redundant with the left half,
        then return `of_val[:half_size+1]`, where `half_size` is half the
        length of `of_val[1:]`.
        If the right half is not redundant, then return `of_val` unchanged.

        Used for `U`-type vals.
    '''
    if len(of_val) < 4:
        return of_val
    bools_part = of_val[1:]
    half_size = len(bools_part)
    left_half = bools_part[:half_size]
    right_half = bools_part[half_size:]
    for i in range(half_size):
        if left_half[i] != right_half[i]:
            return of_val
    return of_val[:half_size+1]


def gilvenkoize(this_val: list[int]) -> list[int]:
    '''
    summary: If `this_val` only consists of `0`s aside from its first element,
        then return `[0]`, since Gilvenko's theorem applies. Otherwise,
        return `this_val` unchanged.
    '''
    for i in range(1, len(this_val)):
        if this_val[i] > 0:
            return this_val
    return [0]


def build_not(from_val: list[int]) -> list[int]:
    '''
    summary: Return the intuitionistic negation of `from_val`.
    '''
    for i, from_valx in enumerate(from_val):
        from_val[i] = 2 - from_valx
    return from_val


def build_or(val_a: list[int], val_b: list[int]) -> list[int]:
    '''
    summary: Return the intuitionistic disjunction of `val_a` and `val_b`.
    '''
    t = 2
    f = 0
    if val_a[0] == t or val_b[0] == t:
        return [2]
    if val_a[0] == f:
        return val_b
    if val_b[0] == f:
        return val_a
    # Assure that both val_a and val_b are of equal lengths.
    while len(val_a) < len(val_b):
        val_a = double_bools(val_a)
    while len(val_b) < len(val_a):
        val_b = double_bools(val_b)
    for i, (val_ax, val_bx) in enumerate(zip(val_a, val_b)):
        if val_ax < val_bx:
            val_a[i] = val_b[i]
    return gilvenkoize(halve_bools(val_a))


def build_and(val_a: list[int], val_b: list[int]) -> list[int]:
    '''
    summary: Return the intuitionistic conjunction of `val_a` and `val_b`.
    '''
    t = 2
    f = 0
    if val_a[0] == f or val_b[0] == f:
        return [0]
    if val_a[0] == t:
        return val_b
    if val_b[0] == t:
        return val_a
    # Assure that both val_a and val_b are of equal lengths.
    while len(val_a) < len(val_b):
        val_a = double_bools(val_a)
    while len(val_b) < len(val_a):
        val_b = double_bools(val_b)
    for i, (val_ax, val_bx) in enumerate(zip(val_a, val_b)):
        if val_ax > val_bx:
            val_a[i] = val_b[i]
    return gilvenkoize(halve_bools(val_a))


def evaluate_val_expr(val_expr: Node) -> list[int]:
    '''
    summary: Evaluate the VAL-EXPR Nodes and return their appropriate
        intuitionistic valuations.
    '''
    print(f'Evaluating {val_expr}')
    # For already assigned VAL-VARs.
    if val_expr.name == 'VAL-VAR':
        assert isinstance(val_expr.left, Node)
        val_id_key = val_expr.left.literal
        val_id_value: list[int] = ASSIGN_MAP.get(val_id_key, None)
        if val_id_value is None:
            print(val_id_key, 'is not a valid VAL ID.')
            exit(1)
        if not isinstance(val_id_value, list) \
                or not all(isinstance(i, int) and -1 < i < 3
                           for i in val_id_value):
            print(f'{val_id_key} is of the wrong type {val_id_value}.')
            exit(1)
        return val_id_value
    # For all terminals.
    if val_expr.action == 'build_true':
        return build_true()
    if val_expr.action == 'build_false':
        return build_false()
    if val_expr.action == 'build_unsure':
        return build_unsure()
    if val_expr.action == 'LEFT':  # This happens with VAL-ID Nodes.
        assert isinstance(val_expr.left, Node)
        return evaluate_val_expr(val_expr.left)
    # For all nonterminals.
    if val_expr.action == 'build_not':
        assert isinstance(val_expr.left, Node)
        left_side = evaluate_val_expr(val_expr.left)
        return build_not(left_side)
    if val_expr.action == 'build_or':
        assert isinstance(val_expr.left, Node)
        assert isinstance(val_expr.right, Node)
        left_side = evaluate_val_expr(val_expr.left)
        right_side = evaluate_val_expr(val_expr.right)
        return build_or(left_side, right_side)
    if val_expr.action == 'build_and':
        assert isinstance(val_expr.left, Node)
        assert isinstance(val_expr.right, Node)
        left_side = evaluate_val_expr(val_expr.left)
        right_side = evaluate_val_expr(val_expr.right)
        return build_and(left_side, right_side)
    print(f'{val_expr.name} to perform action {val_expr.action}',
          'cannot be correctly evaluated.')
    exit(1)
    return []


def assign_val(this_node: Node) -> None:
    '''
    summary: Assign the value of `this_node.right` to the VAL-VAR
        identified by `this_node.left.left.literal`.
    '''
    assert isinstance(this_node.left, Node)
    assert isinstance(this_node.left.left, Node)
    assert isinstance(this_node.right, Node)
    if this_node.left.name == 'VAL-VAR':
        assign_key: str = this_node.left.left.literal
        assign_value: list[int] = evaluate_val_expr(this_node.right)
        ASSIGN_MAP[assign_key] = evaluate_val_expr(this_node.right)
        print(f'{assign_key} successfully assigned to {assign_value}.')
        return
    print('Invalid type for assign_val.')
    exit(1)

###############################################################################
# Walking the AST
###############################################################################


def walk_tree(this_tree: Node) -> None:
    '''
    summary: Walk the tree and perform the corresponding actions
        on the nodes.
    '''
    if this_tree.action == 'BOTH':
        assert isinstance(this_tree.left, Node)
        assert isinstance(this_tree.right, Node)
        walk_tree(this_tree.left)
        walk_tree(this_tree.right)
        return
    if this_tree.action == 'LEFT':
        assert isinstance(this_tree.left, Node)
        walk_tree(this_tree.left)
        return
    if this_tree.action == 'RIGHT':
        assert isinstance(this_tree.right, Node)
        walk_tree(this_tree.right)
        return
    if this_tree.action == 'assign_val':
        assert isinstance(this_tree, Node)
        assign_val(this_tree)
        return
    print(f'{this_tree.name}\'s {this_tree.action}',
          'has not yet been implemented.')
    exit(1)
    return
