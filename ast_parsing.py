import ast
import re
from messages import STYLE_MESSAGES, NAMED_MESSAGES


class AstParser(ast.NodeVisitor):
    def __init__(self):
        self.errors = {}
        self.name_errors = {}

    def ast_check_args_name(self, node):  # errors -{line: [codes]}; names - {line:{code: value}}
        """
        Checks arguments' names in functions
        :param node: ast.Funtiondef object
        """
        for arg in node.args.args:
            match = re.match(r"[a-z0-9_]+$", arg.arg)
            if match is None:
                self.errors[node.lineno].append("S010")
                self.name_errors[node.lineno]["S010"] = arg.arg

    def ast_check_vars_name(self, nodes):
        """
        Checks variables' name in fucntions
        :param nodes: ast.Functiondef.body
        """
        names = []
        for node in nodes:
            if isinstance(node, ast.Assign):
                for name in node.targets:
                    if isinstance(name, ast.Attribute):
                        match = re.match(r"[a-z0-9_]+$", name.value.id)
                    else:
                        match = re.match(r"[a-z0-9_]+$", name.id)
                    if match is None and name.id not in names:
                        names.append(name.id)
                        self.errors[node.lineno] = []
                        self.errors[node.lineno].append("S011")
                        self.name_errors[node.lineno] = {}
                        self.name_errors[node.lineno]["S011"] = name.id

    def ast_check_default_args(self, node):
        """
        Checks if default argument is mutable
        :param node: ast.Funtiondef object
        """
        for default in node.args.defaults:
            if isinstance(default, ast.List) or isinstance(default, ast.Dict):
                self.errors[node.lineno].append("S012")

    def visit_FunctionDef(self, node):
        self.errors[node.lineno] = []
        self.name_errors[node.lineno] = {}
        self.ast_check_args_name(node)
        self.ast_check_default_args(node)

        self.ast_check_vars_name(node.body)
        self.generic_visit(node)
