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
    summary: Evaluate an <(ASGN|REASGN)-STMT> Node
        by placing a variable name into the appropriate "_VAR" dictionary.

    params:
    node: Node of the <ASGN-STMT> or <REASGN-STMT>.
        An <(ASGN|REASGN)-STMT> is nonterminal.
        An <(ASGN|REASGN)-STMT> has a left child named <TYPE-ID>.
        An <(ASGN|REASGN)-STMT> has a right child named <TYPE-(EXPR|SUBEXPR)>.
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
        print(f'ASSIGNED {brou_a.val} to {var_name}.')
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
            print(f'ASSIGNED {int_a} to {var_name}.')
        else:
            assert isinstance(number_a, int)
            INT_VARS[var_name] = number_a
            print(f'ASSIGNED {number_a} to {var_name}.')
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
            print(f'ASSIGNED {rat_a.num} / {rat_a.num} to {var_name}.')
        else:
            assert isinstance(number_a, Rat)
            RAT_VARS[var_name] = number_a
            print(f'ASSIGNED {number_a.num} / {number_a.den} to {var_name}.')
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
        def int int3 as 3;
        def int int5 as 5;
        def int int7 as 7;
        def int int9 as 9;

        `Integer Addition`
        def int intSum1 as 3 + 5;
        def int intSum2 as 7 + 9;

        `Integer Subtraction`
        def int intDiff1 as intSum1 - 3; `Expect 5.`
        def int intDiff2 as intSum2 - 5; `Expect 11.`

        `Integer Multiplication`
        def int intProd1 as intDiff1 * intDiff2; `Expect 55.`
        def int intProd2 as (intSum1 * 9) * 2; `Expect 144.`

        `Integer Division`
        def int intQuot1 as 9 / 3; `Expect 3.`
        def rat intQuot2 as intProd1 / intSum1; `Expect 55/8.`

        `Integer Modulus`
        def int intMod1 as 9 % 5; `Expect 4.`
        def int intMod2 as intSum2 % (intDiff2 % 3); `Expect 0.`

        `Rational Addition`
        def rat ratSum1 as (intSum1 / intSum2) + (3 / 9); `Expect 5/6.`
        def rat ratSum2 as ratSum1 + (ratSum1 + 5); `Expect 20/3.`

        `Rational Subtraction`
        def rat ratDiff1 as (1 / 3) - (intSum1 / intSum2); `Expect -1/6.`
        def rat ratDiff2 as (-5 / -10) - (intProd2 - (1 / 2)); `Expect -143/1.`

        `Rational Multiplication`
        def rat ratProd1 as ratDiff1 * ratDiff2; `Expect 143/6.`
        def rat ratProd2 as ratProd1 * 12; `Expect 286/1.`
        
        `Rational Division`
        def rat ratQuot1 as ratDiff1 / ratSum1; `Expect -1/5.`
        def rat ratQuot2 as (ratSum2 / ratSum1) / intProd1; `Expect 8/55.`
        def int intQuot3 as ratSum2 / ratSum2; `Expect 1.`

        `Rational Modulus`
        def rat ratMod1 as ratSum2 % ratSum1; `Expect 0/1.`
        def rat ratMod2 as intProd2 % ratDiff1; `Expect 0/1.`
        def rat ratMod3 as intQuot2 % 3; `Expect... 7/8.`

        `Rational Decimalization`
        def rat ratDec1 as 15.15; `Expect 303/20.`
        def rat ratDec2 as 3.1415926; `Expect 15707963/5000000.`
        '''
    sample_tokens: list[Node] = tokenize(lej_pgrm=sample_program)
    sample_tree: Node = parse(lej_tokens=sample_tokens)
    execution: int = walk_tree(lej_tree=sample_tree)
