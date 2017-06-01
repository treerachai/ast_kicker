#!/usr/bin/env python3
import ast
import collections


file_data = (
    ('./test_data/__init__.py', 'test_module'),
    ('./test_data/test_class.py', 'test_module.test_class'),
    ('./test_data/test_function.py', 'test_module.test_function'),
    ('./test_data/test_method.py', 'test_module.test_method'),
    ('./test_data/test_variable.py', 'test_module.test_variable'),
)


class Namespace(object):
    names = None
    node = None
    children = None
    parent = None

    def __init__(self, node, parent):
        self.node = node
        self.names = set()
        self.children = set()
        self.parent = parent

class NamespaceCollection(object):
    def __init__(self):
        self.namespaces = {}
        global_namespace = Namespace(None, None)
        self.namespaces['.'] = global_namespace
        self.stack = [global_namespace, ]

    @property
    def current(self):
        return self.stack[-1]

    def inward(self, node):
        print('INWARD', node)
        parent = self.current
        namespace = Namespace(node, parent)
        parent.children.add(namespace)
        self.stack.append(namespace)
        assert self.current.node == node
        return namespace

    def outward(self, node):
        print('OUTWARD', node)
        assert self.current.node == node
        self.stack.pop()

class NodeVisitor(ast.NodeVisitor):
    level = 0
    node_stack = None
    namespaces = None

    def __init__(self, root):
        super(NodeVisitor, self).__init__()
        self.root = root
        self.namespaces = NamespaceCollection()
        self.node_stack = [None, ]

    def pre_visit(self, node):
        self.level += 1
        self.node_stack.append(node)
        print(self.level, node)

    def post_visit(self, node):
        self.node_stack.pop()
        self.level -= 1

    def visit_arg(self, node):
        print(self.level, 'arg', node.arg)
        self.namespaces.current.names.add(node.arg)
        super(NodeVisitor, self).generic_visit(node)

    # def visit_Assign(self, node):
    #     print(self.level, 'Assign', dir(node))
    #     super(NodeVisitor, self).generic_visit(node)

    def visit_ClassDef(self, node):
        self.pre_visit(node)
        self.namespaces.inward(node)
        print(self.level, 'C', node.name)
        super(NodeVisitor, self).generic_visit(node)
        self.namespaces.outward(node)
        self.post_visit(node)

    def visit_FunctionDef(self, node):
        self.pre_visit(node)
        self.namespaces.inward(node)
        print(self.level, 'F', node.name)
        super(NodeVisitor, self).generic_visit(node)
        self.namespaces.outward(node)
        self.post_visit(node)

    def visit_Module(self, node):
        node.name = self.root
        self.pre_visit(node)
        self.namespaces.inward(node)
        print(self.level, 'M', node.name)
        super(NodeVisitor, self).generic_visit(node)
        self.namespaces.outward(node)
        self.post_visit(node)

    def visit_Name(self, node):
        print(self.level, 'Name', node.id)
        super(NodeVisitor, self).generic_visit(node)

    # def visit_Store(self, node):
    #     print(self.level, 'Store', dir(node))
    #     super(NodeVisitor, self).generic_visit(node)

    def generic_visit(self, node):
        self.pre_visit(node)
        super(NodeVisitor, self).generic_visit(node)
        self.post_visit(node)

for file_name, file_module in file_data:
    file_content = open(file_name, 'r').read()
    tree = ast.parse(file_content)
    visitor = NodeVisitor(file_module)
    visitor.visit(tree)
