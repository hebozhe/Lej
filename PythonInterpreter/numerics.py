'''
This module houses the functions that evaluate numeric values.
'''
from typing import Literal, TypeAlias
from node import Node

###############################################################################
# Base Types
###############################################################################


class Rat:
    '''
    summary: Stores a rational number value.
    '''
    num: int  # num can be positive or negative.
    den: int  # den must always be positive.


class Real:
    '''
    summary: Stores a real number value.
    '''
    num: int  # num can be positive or negative.
    den: int  # den must always be positive.
    exp: Rat


class RealPair:
    '''
    summary: Stores an unresolved sum, difference, product, quotient, modulus,
        or exponentiation of two reals.
    '''
    left_real: Real
    right_real: Real
    oper: Literal['+', '-', '*', '/', '%', '^']


Number: TypeAlias = int | Rat | Real | RealPair

INT_VARS: dict[str, int] = {}
RAT_VARS: dict[str, Rat] = {}


###############################################################################
# Arithmetic Evaluations
###############################################################################

def eval_int_subexpr(node: Node) -> int:
    '''
    summary: Evaluate an <INT-SUBEXPR> Node by converting its literal.

    params:
    node: Node of the <INT-SUBEXPR>.
        An <INT-SUBEXPR> is terminal.
        An <INT-SUBEXPR> literal is a collection of digits '0' through '9'.
    '''
    int_a: int = 0
    for char in node.literal:
        if char == '0':
            int_a = int_a * 10
        elif char == '1':
            int_a = (int_a * 10) + 1
        elif char == '2':
            int_a = (int_a * 10) + 2
        elif char == '3':
            int_a = (int_a * 10) + 3
        elif char == '4':
            int_a = (int_a * 10) + 4
        elif char == '5':
            int_a = (int_a * 10) + 5
        elif char == '6':
            int_a = (int_a * 10) + 6
        elif char == '7':
            int_a = (int_a * 10) + 7
        elif char == '8':
            int_a = (int_a * 10) + 8
        elif char == '9':
            int_a = (int_a * 10) + 9
    return int_a


def standardize_rat(rat: Rat) -> Rat:
    '''
    summary: Standardize the notational presentation of a rational.

        Rationals are standardized by forcing the denominator
            to be positive.

    params:
    rat: Rat to be standardized.

    return: Rat fitting that standard.
    '''
    if rat.den < 0:
        rat.num = 0 - rat.num
        rat.den = 0 - rat.den
    return rat


def get_gcd(int_a: int, int_b: int) -> int:
    '''
    summary: Calculate the greatest common denominator of two integers.

    params:
    int_a: int of the first factor.
    int_b: int of the second factor.

    return: int of the greatest common denominator (GCD).
    '''
    if int_a < 0:
        int_a = 0 - int_a
    if int_b < 0:
        int_b = 0 - int_b
    while int_b != 0:
        int_a, int_b = int_b, int_a % int_b
    # By here, int_b > int_a.
    return int_a


def simplify_rat(rat: Rat) -> Rat:
    '''
    summary: Simplify a rational to its lowest terms.

    params:
    rat: Rat to be simplified.

    return: Rat, simplified.
    '''
    gcd: int = get_gcd(int_a=rat.num, int_b=rat.den)
    rat.num = rat.num // gcd
    rat.den = rat.den // gcd
    return rat


def conv_int_to_rat(int_: int) -> Rat:
    '''
    summary: Convert an integer to a rational.
        All integers are rationals, so there's no risk of failure.

    params:
    int_: int to be converted.

    return: Rat of the integer.
    '''
    rat: Rat = Rat()
    rat.num = int_
    rat.den = 1
    return rat


def conv_rat_to_int(rat: Rat) -> int:
    '''
    summary: Convert a rational to an integer.
        Not all rationals are integers, so there is a risk of failure.

    params:
    rat: Rat to be converted.

    return: int of the rational, or else exit with an error.
    '''
    rat = standardize_rat(rat=rat)
    rat = simplify_rat(rat=rat)
    if rat.den == 1:
        return rat.num
    print(f'The rational number ({rat.num} / {rat.den}) cannot be converted to an integer.')
    exit(1)


def eval_add(number_a: Number, number_b: Number) -> Number:
    '''
    summary: Evaluate the sum of two numbers.

    params:
    number_a: Number of the left operand of an <ADD-(EXPR|SUBEXPR)>.
    number_a: Number of the right operand of an <ADD-(EXPR|SUBEXPR)>.

    return: Number of the sum, simplified and standardized.
    '''
    # Evaluate "int + int" expression.
    if isinstance(number_a, int) and isinstance(number_b, int):
        return number_a + number_b
    # Evaluate "int + Rat" expression.
    if isinstance(number_a, int) and isinstance(number_b, Rat):
        rat_a: Rat = conv_int_to_rat(int_=number_a)
        rat_b: Rat = standardize_rat(rat=number_b)
        rat_c: Rat = Rat()
        rat_c.num = (rat_a.num * rat_b.den) + (rat_b.num * rat_a.den)
        rat_c.den = rat_a.den * rat_b.den
        return simplify_rat(rat=rat_c)
    # Evaluate "Rat + int" expression.
    if isinstance(number_a, Rat) and isinstance(number_b, int):
        rat_a: Rat = standardize_rat(rat=number_a)
        rat_b: Rat = conv_int_to_rat(int_=number_b)
        rat_c: Rat = Rat()
        rat_c.num = (rat_a.num * rat_b.den) + (rat_b.num * rat_a.den)
        rat_c.den = rat_a.den * rat_b.den
        return simplify_rat(rat=rat_c)
    # Evaluate "Rat + Rat" expression.
    if isinstance(number_a, Rat) and isinstance(number_b, Rat):
        rat_a: Rat = standardize_rat(rat=number_a)
        rat_b: Rat = standardize_rat(rat=number_b)
        rat_c: Rat = Rat()
        rat_c.num = (rat_a.num * rat_b.den) + (rat_b.num * rat_a.den)
        rat_c.den = rat_a.den * rat_b.den
        return simplify_rat(rat=rat_c)
    print(f'The formula of "{type(number_a)} + {type(number_b)}" has not been implemented.')
    exit(1)


def eval_sub(number_a: Number, number_b: Number) -> Number:
    '''
    summary: Evaluate the difference of two numbers.

    params:
    number_a: Number of the left operand of an <SUB-(EXPR|SUBEXPR)>.
    number_a: Number of the right operand of an <SUB-(EXPR|SUBEXPR)>.

    return: Number of the difference, simplified and standardized.
    '''
    # Evaluate "int - int" expression.
    if isinstance(number_a, int) and isinstance(number_b, int):
        return number_a - number_b
    # Evaluate "int - Rat" expression.
    if isinstance(number_a, int) and isinstance(number_b, Rat):
        rat_a: Rat = conv_int_to_rat(int_=number_a)
        rat_b: Rat = standardize_rat(rat=number_b)
        rat_c: Rat = Rat()
        rat_c.num = (rat_a.num * rat_b.den) - (rat_b.num * rat_a.den)
        rat_c.den = rat_a.den * rat_b.den
        return simplify_rat(rat=rat_c)
    # Evaluate "Rat - int" expression.
    if isinstance(number_a, Rat) and isinstance(number_b, int):
        rat_a: Rat = standardize_rat(rat=number_a)
        rat_b: Rat = conv_int_to_rat(int_=number_b)
        rat_c: Rat = Rat()
        rat_c.num = (rat_a.num * rat_b.den) - (rat_b.num * rat_a.den)
        rat_c.den = rat_a.den * rat_b.den
        return simplify_rat(rat=rat_c)
    # Evaluate "Rat - Rat" expression.
    if isinstance(number_a, Rat) and isinstance(number_b, Rat):
        rat_a: Rat = standardize_rat(rat=number_a)
        rat_b: Rat = standardize_rat(rat=number_b)
        rat_c: Rat = Rat()
        rat_c.num = (rat_a.num * rat_b.den) - (rat_b.num * rat_a.den)
        rat_c.den = rat_a.den * rat_b.den
        return simplify_rat(rat=rat_c)
    print(f'The formula of "{type(number_a)} - {type(number_b)}" has not been implemented.')
    exit(1)


def eval_mul(number_a: Number, number_b: Number) -> Number:
    '''
    summary: Evaluate the product of two numbers.

    params:
    number_a: Number of the left operand of an <MUL-(EXPR|SUBEXPR)>.
    number_a: Number of the right operand of an <MUL-(EXPR|SUBEXPR)>.

    return: Number of the product, simplified and standardized.
    '''
    # Evaluate "int * int" expression.
    if isinstance(number_a, int) and isinstance(number_b, int):
        return number_a * number_b
    # Evaluate "int * Rat" expression.
    if isinstance(number_a, int) and isinstance(number_b, Rat):
        rat_a: Rat = conv_int_to_rat(int_=number_a)
        rat_b: Rat = standardize_rat(rat=number_b)
        rat_c: Rat = Rat()
        rat_c.num = rat_a.num * rat_a.num
        rat_c.den = rat_a.den * rat_b.den
        return simplify_rat(rat=rat_c)
    # Evaluate "Rat * int" expression.
    if isinstance(number_a, Rat) and isinstance(number_b, int):
        rat_a: Rat = standardize_rat(rat=number_a)
        rat_b: Rat = conv_int_to_rat(int_=number_b)
        rat_c: Rat = Rat()
        rat_c.num = rat_a.num * rat_a.num
        rat_c.den = rat_a.den * rat_b.den
        return simplify_rat(rat=rat_c)
    # Evaluate "Rat * Rat" expression.
    if isinstance(number_a, Rat) and isinstance(number_b, Rat):
        rat_a: Rat = standardize_rat(rat=number_a)
        rat_b: Rat = standardize_rat(rat=number_b)
        rat_c: Rat = Rat()
        rat_c.num = rat_a.num * rat_a.num
        rat_c.den = rat_a.den * rat_b.den
        return simplify_rat(rat=rat_c)
    print(f'The formula of "{type(number_a)} * {type(number_b)}" has not been implemented.')
    exit(1)


def eval_div(number_a: Number, number_b: Number) -> Number:
    '''
    summary: Evaluate the quotient of two numbers.

    params:
    number_a: Number of the left operand of an <DIV-(EXPR|SUBEXPR)>.
    number_a: Number of the right operand of an <DIV-(EXPR|SUBEXPR)>.

    return: Number of the quotient, simplified and standardized.
    '''
    # Evaluate "int / int" expression.
    if isinstance(number_a, int) and isinstance(number_b, int):
        rat_a: Rat = conv_int_to_rat(int_=number_a)
        rat_b: Rat = conv_int_to_rat(int_=number_b)
        rat_c: Rat = Rat()
        rat_c.num = rat_a.num * rat_b.den
        rat_c.den = rat_b.num * rat_a.den
        rat_c = standardize_rat(rat=rat_c)
        return simplify_rat(rat=rat_c)
    # Evaluate "int / Rat" expression.
    if isinstance(number_a, int) and isinstance(number_b, Rat):
        rat_a: Rat = conv_int_to_rat(int_=number_a)
        rat_b: Rat = number_b
        rat_c: Rat = Rat()
        rat_c.num = rat_a.num * rat_b.den
        rat_c.den = rat_b.num * rat_a.den
        rat_c = standardize_rat(rat=rat_c)
        return simplify_rat(rat=rat_c)
    # Evaluate "Rat / int" expression.
    if isinstance(number_a, Rat) and isinstance(number_b, int):
        rat_a: Rat = number_a
        rat_b: Rat = conv_int_to_rat(int_=number_b)
        rat_c: Rat = Rat()
        rat_c.num = rat_a.num * rat_b.den
        rat_c.den = rat_b.num * rat_a.den
        rat_c = standardize_rat(rat=rat_c)
        return simplify_rat(rat=rat_c)
    # Evaluate "Rat / Rat" expression.
    if isinstance(number_a, Rat) and isinstance(number_b, Rat):
        rat_a: Rat = number_a
        rat_b: Rat = number_b
        rat_c: Rat = Rat()
        rat_c.num = rat_a.num * rat_b.den
        rat_c.den = rat_b.num * rat_a.den
        rat_c = standardize_rat(rat=rat_c)
        return simplify_rat(rat=rat_c)
    print(f'The formula of "{type(number_a)} / {type(number_b)}" has not been implemented.')
    exit(1)


def eval_dec(int_a: int, int_b: int) -> Rat:
    '''
    summary: Evaluate the decimalization of two integers.

    params:
    int_a: int of the left operand of an <DEC-(EXPR|SUBEXPR)>.
    int_b: int of the right operand of an <DEC-(EXPR|SUBEXPR)>.

    return: Rat of the decimal-formatted rational, simplified and standardized.
    '''
    # Evaluate "int.int" expression.
    den: int = 1
    while den < int_b:
        den = den * 10
    rat: Rat = Rat()
    rat.num = (int_a * den) + int_b
    rat.den = den
    rat = simplify_rat(rat=rat)
    return rat


def eval_mod(number_a: Number, number_b: Number) -> Number:
    '''
    summary: Evaluate the modulo of two numbers.

    params:
    number_a: Number of the left operand of an <MOD-(EXPR|SUBEXPR)>.
    number_a: Number of the right operand of an <MOD-(EXPR|SUBEXPR)>.

    return: Number of the modulo, simplified and standardized.
    '''
    # Evaluate "int / int" expression.
    if isinstance(number_a, int) and isinstance(number_b, int):
        return number_a - (number_a // number_b)
    # Evaluate "int / Rat" expression.
    if isinstance(number_a, int) and isinstance(number_b, Rat):
        rat_a: Rat = conv_int_to_rat(int_=number_a)
        rat_b: Rat = number_b
        number_c: Number = eval_div(number_a=rat_a, number_b=rat_b)
        if isinstance(number_c, Rat):
            rat_c: Rat = standardize_rat(rat=number_c)
            quo_c: int = rat_c.num // rat_c.den
            prod_c: Number = eval_mul(number_a=rat_c, number_b=quo_c)
            rem_c: Number = eval_sub(number_a=rat_a, number_b=prod_c)
            return rem_c
    # Evaluate "Rat / int" expression.
    if isinstance(number_a, Rat) and isinstance(number_b, int):
        rat_a: Rat = number_a
        rat_b: Rat = conv_int_to_rat(int_=number_b)
        number_c: Number = eval_div(number_a=rat_a, number_b=rat_b)
        if isinstance(number_c, Rat):
            rat_c: Rat = standardize_rat(rat=number_c)
            quo_c: int = rat_c.num // rat_c.den
            prod_c: Number = eval_mul(number_a=rat_c, number_b=quo_c)
            rem_c: Number = eval_sub(number_a=rat_a, number_b=prod_c)
            return rem_c
    # Evaluate "Rat / Rat" expression.
    if isinstance(number_a, Rat) and isinstance(number_b, Rat):
        rat_a: Rat = number_a
        rat_b: Rat = number_b
        number_c: Number = eval_div(number_a=rat_a, number_b=rat_b)
        if isinstance(number_c, Rat):
            rat_c: Rat = standardize_rat(rat=number_c)
            quo_c: int = rat_c.num // rat_c.den
            prod_c: Number = eval_mul(number_a=rat_c, number_b=quo_c)
            rem_c: Number = eval_sub(number_a=rat_a, number_b=prod_c)
            return rem_c
    print(f'The formula of "{type(number_a)} / {type(number_b)}" has not been implemented.')
    exit(1)


def eval_arit_tree(tree: Node) -> Number:
    '''
    summary: Evaluate every <ADD-EXPR>, <SUB-EXPR>, <MUL-EXPR>, <DIV-EXPR>,
        <EXP-EXPR>, <DEC-EXPR>, <INT-SUBEXPR>,
        as well as their matching <___-SUBEXPR>, to an integer, rational, or real.

    params:
    tree: Node of the tree whose root should evaluate to an integer, rational, or real.

    return: Number of the evaluated expression.
    '''
    if tree.name == '<INT-SUBEXPR>':
        return eval_int_subexpr(node=tree)
    if tree.name == '<INT-ID>':
        var_name: str = f'{tree.scope}:{tree.left.literal}'
        return INT_VARS[var_name]
    if tree.name == '<RAT-ID>':
        var_name: str = f'{tree.scope}:{tree.left.literal}'
        return RAT_VARS[var_name]
    if tree.name == '<ADD-EXPR>' or tree.name == '<ADD-SUBEXPR>':
        number_a: Number = eval_arit_tree(tree=tree.left)
        number_b: Number = eval_arit_tree(tree=tree.right)
        return eval_add(number_a=number_a, number_b=number_b)
    if tree.name == '<SUB-EXPR>' or tree.name == '<SUB-SUBEXPR>':
        number_a: Number = eval_arit_tree(tree=tree.left)
        number_b: Number = eval_arit_tree(tree=tree.right)
        return eval_sub(number_a=number_a, number_b=number_b)
    if tree.name == '<MUL-EXPR>' or tree.name == '<MUL-SUBEXPR>':
        number_a: Number = eval_arit_tree(tree=tree.left)
        number_b: Number = eval_arit_tree(tree=tree.right)
        return eval_mul(number_a=number_a, number_b=number_b)
    if tree.name == '<DIV-EXPR>' or tree.name == '<DIV-SUBEXPR>':
        number_a: Number = eval_arit_tree(tree=tree.left)
        number_b: Number = eval_arit_tree(tree=tree.right)
        return eval_div(number_a=number_a, number_b=number_b)
    if tree.name == '<DEC-EXPR>' or tree.name == '<DEC-SUBEXPR>':
        number_a: Number = eval_arit_tree(tree=tree.left)
        number_b: Number = eval_arit_tree(tree=tree.right)
        return eval_div(number_a=number_a, number_b=number_b)
    if tree.name == '<MOD-EXPR>' or tree.name == '<MOD-SUBEXPR>':
        number_a: Number = eval_arit_tree(tree=tree.left)
        number_b: Number = eval_arit_tree(tree=tree.right)
        return eval_mod(number_a=number_a, number_b=number_b)
    print(f'This {tree.name} could not be evaluated.')
    exit(1)
