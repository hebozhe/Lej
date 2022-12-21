'''
This is where Lej's lexer, parser, and evaluator all come together.
'''
import os
from lexer import tokenize
from parser_ import parse
from evaluator import walk_tree
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
    lej_tokens: list[Node] = tokenize(this_path=test_path)
    print(lej_tokens)
    lej_tree = parse(lej_tokens)
    # print(count_nodes(of_tree=lej_tree))
    walk_tree(lej_tree)
