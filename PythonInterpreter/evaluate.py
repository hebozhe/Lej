'''
The evaluator is where the Lej AST is walked and interpreted.
'''
from brouwerians import (eval_brou_tree,
                         Brou,
                         BROU_VARS)
from numerics import (conv_rat_to_int, conv_int_to_rat, eval_arit_tree,
                      Rat, Number,
                      INT_VARS, RAT_VARS)
from lex import tokenize
from parse import parse
from node import Node

###############################################################################
# Assignment and Reassignment Evaluations
###############################################################################


def eval_asgn_stmt(node: Node, reasgn: bool) -> int:
    '''
    summary: Evaluate an <ASGN-STMT> Node by placing a variable name
        into the appropriate _VAR dictionary.

    params:
    node: Node of the <ASGN-STMT>.
        An <ASGN-STMT> is nonterminal.
        An <ASGN-STMT> has a left child named <___-ID>.
        An <ASGN-STMT> has a right child named <___-(EXPR|SUBEXPR)>.
    reasgn: bool indicating whether the action is an assignment (False) or reassignment (True.)

    return: int indicating successful or unsuccessful completion.
        0 indicates a successful termination.
        1 indicates an erroneous termination.
    '''
    # print(node.left.name, node.right.name)
    var_name: str = f'{node.scope}:{node.left.left.literal}'
    # Assign or reassign Brouwerians.
    if node.left.name == '<BROU-ID>':
        if not reasgn and BROU_VARS.get(var_name, False):
            print(f'Brouwerian {node.left.left.literal} is already assigned.')
            exit(1)
        elif reasgn and not BROU_VARS.get(var_name, False):
            print(f'Brouwerian {node.left.left.literal} has not been assigned.')
            exit(1)
        brou_a: Brou = eval_brou_tree(tree=node.right)
        BROU_VARS[var_name] = brou_a
        return 0
    # Assign or reassign integers.
    if node.left.name == '<INT-ID>':
        if not reasgn and INT_VARS.get(var_name, False):
            print(f'Integer {node.left.left.literal} is already assigned.')
            exit(1)
        elif reasgn and not INT_VARS.get(var_name, False):
            print(f'Integer {node.left.left.literal} has not been assigned.')
            exit(1)
        number_a: Number = eval_arit_tree(tree=node.right)
        # Attempt to convert non-integer results.
        if isinstance(number_a, Rat):
            int_a: int = conv_rat_to_int(rat=number_a)
            INT_VARS[var_name] = int_a
        else:
            assert isinstance(number_a, int)
            INT_VARS[var_name] = number_a
        return 0
    # Assign or reassign rationals.
    if node.left.name == '<RAT-ID>':
        if not reasgn and RAT_VARS.get(var_name, False):
            print(f'Rational {node.left.left.literal} is already assigned.')
            exit(1)
        elif reasgn and not RAT_VARS.get(var_name, False):
            print(f'Rational {node.left.left.literal} has not been assigned.')
            exit(1)
        number_a: Number = eval_arit_tree(tree=node.right)
        if isinstance(number_a, int):
            rat_a: Rat = conv_int_to_rat(int_=number_a)
            RAT_VARS[var_name] = rat_a
        else:
            assert isinstance(number_a, Rat)
            RAT_VARS[var_name] = number_a
        return 0
    # TODO: Complete this part of the evaluator.
    print(f'The {node.name} with children',
          f'{node.left.name} and {node.right.name}',
          'could not be completed.')
    exit(1)


###############################################################################
# Walk Lej Tree
###############################################################################


def walk_tree(lej_tree: Node) -> int:
    '''
    summary: Walk a fully parsed tree, recursively, to execute the relevant code.

    params:
    tree: Node of a completely parsed Lej program tree.

    return: int indicating successful or unsuccessful completion.
        0 indicates a successful termination.
        1 indicates an erroneous termination.
    '''
    if lej_tree.name == '<LR-NODE>':
        return max(walk_tree(lej_tree=lej_tree.left),
                   walk_tree(lej_tree=lej_tree.right))
    if lej_tree.name == '<ASGN-STMT>':
        return eval_asgn_stmt(node=lej_tree, reasgn=False)
    if lej_tree.name == '<REASGN-STMT>':
        return eval_asgn_stmt(node=lej_tree, reasgn=True)
    print(f'The node {lej_tree.name} does not have an evaluation procedure in place.')
    exit(1)


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
        def brou isUnsureStill as (isUnsure or isAlsoUnsure) or U;

        def int firstInt as 12;
        change firstInt to 13 + firstInt;
        def rat firstRat as (firstInt / 2.2) % (5.8 / 8.8);
        def brou areEqual as (firstInt = 12) and ((firstRat > 3) or (firstRat < 3));
        '''
    sample_tokens: list[Node] = tokenize(lej_pgrm=sample_program)
    sample_tree: Node = parse(lej_tokens=sample_tokens)
    execution: int = walk_tree(lej_tree=sample_tree)
