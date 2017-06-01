#!/usr/bin/env python3.5
import ast
import collections


file_data = (
    ('./test_data/__init__.py', 'test_module'),
    ('./test_data/test_class.py', 'test_module.test_class'),
    ('./test_data/test_function.py', 'test_module.test_function'),
    ('./test_data/test_method.py', 'test_module.test_method'),
    ('./test_data/test_variable.py', 'test_module.test_variable'),
)

KickedClass = collections.namedtuple('KickedClass', 'name parent')
KickedFunction = collections.namedtuple('KickedFunction', 'name parent')
KickedModule = collections.namedtuple('KickedModule', 'name parent')


class ClassVisitor(ast.NodeVisitor):
    def __init__(self, root_module):
        super().__init__()
        self.stack = []
        self.dot_stack = [None,]
        self.root = root_module.split('.')

    @property
    def level(self):
        return len(self.stack)

    def print(self, s, *args):
        print('  ' * self.level + str(s), *args)

    def generic_visit(self, node):
        #self.print(node)
        self.stack.append(node)
        super().generic_visit(node)
        self.stack.pop()

    def visit_ClassDef(self, node):
        kicked = KickedClass(node.name, self.dot_stack[-1])
        self.print(kicked)
        self.dot_stack.append(kicked)
        self.generic_visit(node)
        self.dot_stack.pop()

    def visit_FunctionDef(self, node):
        kicked = KickedFunction(node.name, self.dot_stack[-1])
        self.print(kicked)
        self.dot_stack.append(kicked)
        self.generic_visit(node)
        self.dot_stack.pop()
        
    def visit_Module(self, node):
        for value in self.root:
            kicked = KickedModule(value, self.dot_stack[-1])
            self.print(kicked)
            self.dot_stack.append(kicked)
        self.generic_visit(node)
        for value in self.root:
            self.dot_stack.pop()

for file_name, file_module in file_data:
    file_content = open(file_name, 'r').read()
    tree = ast.parse(file_content)
    visitor = ClassVisitor(file_module)
    visitor.visit(tree)
