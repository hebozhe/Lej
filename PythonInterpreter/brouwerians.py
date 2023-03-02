'''
This module houses the functions that evaluate Brouwerian values.
'''
from typing import Literal
from node import Node
from numerics import (eval_sub, eval_arit_tree, Rat, Number)

###############################################################################
# Base Types
###############################################################################


class Brou:
    '''
    summary: Stores a Brouwerian value.
    '''
    u_count: int  # T takes 0, F takes 0, and U takes a positive value.
    val: tuple[Literal[0, 1, 2], ...]


BROU_VARS: dict[str, Brou] = {}


###############################################################################
# Brouwerian Evaluations
###############################################################################


def eval_brou_subexpr(node: Node) -> Brou:
    '''
    summary: Evaluate a <BROU-SUBEXPR> Node by checking its literal.

    params:
    node: Node of the <BROU-SUBEXPR>.
        A <BROU-SUBEXPR> is terminal.
        A <BROU-SUBEXPR> literal is either 'T', 'U', or 'F'.
    '''
    if node.literal == 'T':
        brou_a: Brou = Brou()
        brou_a.u_count = 0
        brou_a.val = (2,)
        return brou_a
    if node.literal == 'U':
        brou_a: Brou = Brou()
        brou_a.u_count = node.u_count
        brou_a.val = (1,) + ((2,) * ((2 ** brou_a.u_count) // 2)) + ((0,) * ((2 ** brou_a.u_count) // 2))
        return brou_a
    if node.literal == 'F':
        brou_a: Brou = Brou()
        brou_a.u_count = 0
        brou_a.val = (0,)
        return brou_a
    print('A <BROU-SUBEXPR> could not be evaluated.')
    exit(1)


def double_brou_tail(brou: Brou) -> Brou:
    '''
    summary: Double the length of a Brouwerian's Boolean tail.

    params:
    brou: Brou to be doubled.

    return: Brou with the doubly long tail.
    '''
    brou_a: Brou = Brou()
    brou_a.u_count = 0
    brou_a.val = brou.val + brou.val[1:]
    return brou_a


def halve_brou_tail(brou: Brou) -> Brou:
    '''
    summary: Halve the length of a Brouwerian's Boolean tail
        if the first half and second half are identical.

    params:
    brou: Brou to be (potentially) halved.

    return: Brou with a (potentially) half-long tail.
    '''
    # Ex: (1, 2, 2, 2, 2); midpt = 3
    # Ex: (1, 2, 0, 2, 0, 2, 0, 2, 0); midpt = 5
    midpt: int = (len(brou.val) + 1) // 2
    while brou.val[1:midpt] == brou.val[midpt:]:
        brou.val = brou.val[:midpt]
        midpt: int = (len(brou.val) + 1) // 2
    return brou


def gilvenkoize(brou: Brou) -> Brou:
    '''
    summary: Determine whether a Brouwerian has a 0 Boolean tail.
        If it does, then the classical contradiction is also an intuitionistic
        contradiction, so a F Brouwerian value can be returned.

    params:
    brou: Brou to be checked for Gilvenko's tautology.

    return: Brou, either Gilvenko-ized or not.
    '''
    if len(brou.val) == 2 and brou.val[1] == 0:
        brou.u_count = 0
        brou.val = (0,)
        return brou
    return brou


def eval_and(brou_a: Brou, brou_b: Brou) -> Brou:
    '''
    summary: Evaluate two Brouwerians via logical conjunction.

    params:
    brou_a: Brou of the left horn of an <AND-(EXPR|SUBEXPR)>.
    brou_b: Brou of the right horn of an <AND-(EXPR|SUBEXPR)>.

    return: Brou of the conjunction, simplified and gilvenkoized.
    '''
    # Evaluate "F and T|U|F" and "T|U|F and F" expressions.
    if brou_a.val[0] == 0 or brou_b.val[0] == 0:
        brou_c: Brou = Brou()
        brou_c.u_count = 0
        brou_c.val = (0,)
        return brou_c
    # Evaluate "T and T|U|F" expressions.
    if brou_a.val[0] == 2:
        return brou_b
    # Evaluate "T|U|F and T" expressions.
    if brou_b.val[0] == 2:
        return brou_a
    # Evaluate "U and U" expressions.
    # Make sure the tails are equally long.
    while len(brou_a.val) < len(brou_b.val):
        brou_a = double_brou_tail(brou=brou_a)
    while len(brou_b.val) < len(brou_a.val):
        brou_b = double_brou_tail(brou=brou_b)
    # Choose the minimums for each tail Literal.
    brou_c: Brou = Brou()
    brou_c.val = (1,)
    for dex in range(1, len(brou_a.val)):
        if brou_a.val[dex] == 0 or brou_b.val[dex] == 0:
            brou_c.val = brou_c.val + (0,)
        else:
            brou_c.val = brou_c.val + (2,)
    brou_c = halve_brou_tail(brou=brou_c)
    brou_c = gilvenkoize(brou=brou_c)
    return brou_c


def eval_or(brou_a: Brou, brou_b: Brou) -> Brou:
    '''
    summary: Evaluate two Brouwerians via logical disjunction.

    params:
    brou_a: Brou of the left horn of an <OR-(EXPR|SUBEXPR)>.
    brou_b: Brou of the right horn of an <OR-(EXPR|SUBEXPR)>.

    return: Brou of the disjunction, simplified and gilvenkoized.
    '''
    # Evaluate "T or T|U|F" and "T|U|F or T" expressions.
    if brou_a.val[0] == 2 or brou_b.val[0] == 2:
        brou_c: Brou = Brou()
        brou_c.u_count = 0
        brou_c.val = (2,)
        return brou_c
    # Evaluate "F or T|U|F" expressions.
    if brou_a.val[0] == 0:
        return brou_b
    # Evaluate "T|U|F or F" expressions.
    if brou_b.val[0] == 0:
        return brou_a
    # Evaluate "U and U" expressions.
    # Make sure the tails are equally long.
    while len(brou_a.val) < len(brou_b.val):
        brou_a = double_brou_tail(brou=brou_a)
    while len(brou_b.val) < len(brou_a.val):
        brou_b = double_brou_tail(brou=brou_b)
    # Choose the maximums for each tail Literal.
    brou_c: Brou = Brou()
    brou_c.val = (1,)
    for dex in range(1, len(brou_a.val)):
        if brou_a.val[dex] == 2 or brou_b.val[dex] == 2:
            brou_c.val = brou_c.val + (2,)
        else:
            brou_c.val = brou_c.val + (0,)
    brou_c = halve_brou_tail(brou=brou_c)
    brou_c = gilvenkoize(brou=brou_c)
    return brou_c


def eval_not(brou_a: Brou) -> Brou:
    '''
    summary: Evaluate one Brouwerian via logical negation.

    params:
    brou_a: Brou of the left horn of a <NOT-(EXPR|SUBEXPR)>.

    return: Brou of the negation, simplified and gilvenkoized.
    '''
    brou_c: Brou = Brou()
    if brou_a.val[0] == 2:
        brou_c.u_count = 0
        brou_c.val = (0,)
        return brou_c
    if brou_a.val[0] == 0:
        brou_c.u_count = 0
        brou_c.val = (2,)
        return brou_c
    brou_c.val = (1,)
    for dex in range(1, len(brou_a.val)):
        brou_c.val = brou_c.val + ((2,) if brou_a.val[dex] == 0 else (0,))
    return brou_c


def eval_eq(number_a: Number, number_b: Number) -> Brou:
    '''
    summary: Evaluate two numbers for equality.

    params:
    number_a: Number of the left horn of a <EQ-(EXPR|SUBEXPR)>.
    number_b: Number of the right horn of a <EQ-(EXPR|SUBEXPR)>.

    return: Brou of the equality relation. 
    '''
    number_c: Number = eval_sub(number_a=number_a, number_b=number_b)
    brou: Brou = Brou()
    brou.u_count = 0
    if isinstance(number_c, int):
        brou.val = (2,) if number_c == 0 else (0,)
    if isinstance(number_c, Rat):
        brou.val = (2,) if number_c.num == 0 else (0,)
    return brou


def eval_gt(number_a: Number, number_b: Number) -> Brou:
    '''
    summary: Evaluate two numbers for inequality
        where the left horn is greater than the right horn.

    params:
    number_a: Number of the left horn of a <GT-(EXPR|SUBEXPR)>.
    number_b: Number of the right horn of a <GT-(EXPR|SUBEXPR)>.

    return: Brou of the equality relation. 
    '''
    number_c: Number = eval_sub(number_a=number_a, number_b=number_b)
    brou: Brou = Brou()
    brou.u_count = 0
    if isinstance(number_c, int):
        brou.val = (2,) if number_c > 0 else (0,)
    if isinstance(number_c, Rat):
        brou.val = (2,) if number_c.num > 0 else (0,)
    return brou


def eval_lt(number_a: Number, number_b: Number) -> Brou:
    '''
    summary: Evaluate two numbers for inequality
        where the left horn is less than the right horn.

    params:
    number_a: Number of the left horn of a <LT-(EXPR|SUBEXPR)>.
    number_b: Number of the right horn of a <LT-(EXPR|SUBEXPR)>.

    return: Brou of the equality relation. 
    '''
    number_c: Number = eval_sub(number_a=number_a, number_b=number_b)
    brou: Brou = Brou()
    brou.u_count = 0
    if isinstance(number_c, int):
        brou.val = (2,) if number_c < 0 else (0,)
    if isinstance(number_c, Rat):
        brou.val = (2,) if number_c.num < 0 else (0,)
    return brou


def eval_brou_tree(tree: Node) -> Brou:
    '''
    summary: Evaluate every <AND-EXPR>, <OR-EXPR>, <NOT-EXPR>,
        <INT-SUBEXPR>,
        as well as their matching <___-SUBEXPR>, to a Brouwerian.

    params:
    tree: Node of the tree whose root should evaluate to a Brouwerian.

    return: Brou of the evaluated expression.
    '''
    if tree.name == '<BROU-SUBEXPR>':
        return eval_brou_subexpr(node=tree)
    if tree.name == '<BROU-ID>':
        var_name: str = f'{tree.scope}:{tree.left.literal}'
        return BROU_VARS[var_name]
    if tree.name == '<AND-EXPR>' or tree.name == '<AND-SUBEXPR>':
        brou_a: Brou = eval_brou_tree(tree=tree.left)
        brou_b: Brou = eval_brou_tree(tree=tree.right)
        return eval_and(brou_a=brou_a, brou_b=brou_b)
    if tree.name == '<OR-EXPR>' or tree.name == '<OR-SUBEXPR>':
        brou_a: Brou = eval_brou_tree(tree=tree.left)
        brou_b: Brou = eval_brou_tree(tree=tree.right)
        return eval_or(brou_a=brou_a, brou_b=brou_b)
    if tree.name == '<NOT-EXPR>' or tree.name == '<NOT-SUBEXPR>':
        brou_a: Brou = eval_brou_tree(tree=tree.left)
        return eval_not(brou_a=brou_a)
    if tree.name == '<EQ-EXPR>' or tree.name == '<EQ-SUBEXPR>':
        number_a: Number = eval_arit_tree(tree=tree.left)
        number_b: Number = eval_arit_tree(tree=tree.right)
        return eval_eq(number_a=number_a, number_b=number_b)
    if tree.name == '<GT-EXPR>' or tree.name == '<GT-SUBEXPR>':
        number_a: Number = eval_arit_tree(tree=tree.left)
        number_b: Number = eval_arit_tree(tree=tree.right)
        return eval_gt(number_a=number_a, number_b=number_b)
    if tree.name == '<LT-EXPR>' or tree.name == '<LT-SUBEXPR>':
        number_a: Number = eval_arit_tree(tree=tree.left)
        number_b: Number = eval_arit_tree(tree=tree.right)
        return eval_lt(number_a=number_a, number_b=number_b)
    # TODO: Complete this part of the evaluator.
    print(f'This {tree.name} could not be evaluated.')
    exit(1)
