'''
This is where Lej's lexer, parser, and evaluator all come together.
'''
import os
from lex import tokenize
from parse import parse
from evaluate import walk_tree
from node import Node

PATH_HERE: str = '/'.join(os.path.abspath(__file__).split('/')[:-2])
print(PATH_HERE)


def count_nodes(of_tree: Node | None) -> int:
    '''
    TODO: Write a docstring.
    '''
    if of_tree is None:
        return 0
    return 1 + count_nodes(of_tree.left) + count_nodes(of_tree.right)


if __name__ == '__main__':
    test_path: str = f'{PATH_HERE}/Examples/valAssignments.lej'
    with open(test_path, mode='r', encoding='UTF-8') as test_file:
        test_prgrm: str = test_file.read()
    test_tokens: list[Node] = tokenize(lej_pgrm=test_prgrm)
    print(test_tokens)
    lej_tree = parse(lej_tokens=test_tokens)
    # print(count_nodes(of_tree=lej_tree))
    walk_tree(lej_tree)
