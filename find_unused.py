import ast
import sys
from collections import defaultdict

class Method:
    def __init__(self, name):
        self.name = name
        self.defined_in_files = set()
        self.used_in_files = set()


def find_symbols(py_file):
    used_symbols = defaultdict(int)
    defined_funcs = []
    with open(py_file) as f:
        src = f.read()
        tree = ast.parse(src, py_file)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # print(ast.dump(node))
                defined_funcs.append(node.name)
            elif isinstance(node, ast.Attribute):
                used_symbols[node.attr] += 1
            elif isinstance(node, ast.Name):
                used_symbols[node.id] += 1
    return defined_funcs, used_symbols

def get_all_unused_methods(files):
    # find method names and where they are defined_in_files
    methods = {}
    # load all used symbols in the whole source tree into memory
    sources = []

    for py_file in files:
        defined_funcs, used_symbols = find_symbols(py_file)
        for name in defined_funcs:
            if name in methods:
                method = methods[name]
            else:
                method = Method(name)
                methods[name] = method
            method.defined_in_files.add(py_file)

        sources.append((py_file, used_symbols))

    # scan usage of each method
    for name, method in methods.items():
        for py_file, used_symbols in sources:
            if name in used_symbols:
                method.used_in_files.add(py_file)

    # print results (list by filename)
    unused_methods = defaultdict(list)
    for name, method in methods.items():
        if not method.used_in_files:
            for py_file in method.defined_in_files:
                unused_methods[py_file].append(name)

    return unused_methods

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        print(f"usage: {sys.argv[0]} files [files ... ]\n")
        print("Scan each file for unused functions")
        sys.exit(1)

    unused_methods = get_all_unused_methods(sys.argv[1:])

    print('-' * 80)

    for py_file in sorted(unused_methods.keys()):
        methods = unused_methods[py_file]
        print(py_file)
        for name in methods:
            print('\t', name)


if __name__ == '__main__':
    main()
