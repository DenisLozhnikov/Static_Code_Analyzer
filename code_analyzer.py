from file_handler import FileHandler
import sys
import re
import ast
from ast_parsing import AstParser
from messages import STYLE_MESSAGES, NAMED_MESSAGES


def get_name(line):
    """
    Return class or function name from given string
    :param line: string, one line of code
    :return: Class or function name
    """
    return re.search(r"(def|class) +(\w+).*$", line).group(2)


def get_construction_name(line):
    """
    Get construction name (def or class)
    :param line: string, one line of code
    :return: construction name
    """
    return re.search(r"(def|class)", line).group(1)


class Analyzer():
    def __init__(self, file_handler):
        """
        Parsers directory for py files if given
        :param file_handler: Object of FileHandler class
        """
        self.files = file_handler.get_filter_files('py')
        self.errors = []
        self.name_issues = {}

    def analyze_all(self):
        """
        Analyzes single file or all files in directory
        :return: formatted dic {Path: {Line: Code}}
        """
        issues = {}
        for file in self.files:  # py file
            self.name_issues = {}
            issues[file] = self.perform_checks(file)
            for pos, value in issues[file].items():  # {pos = line_number: value = [issues_list]}
                for error in value:  # issues in line №(pos)
                    if error in NAMED_MESSAGES:
                        message = STYLE_MESSAGES[error].replace("-", self.name_issues[pos][error])
                    else:
                        message = STYLE_MESSAGES[error]
                    print(f"{file}: Line {pos}: {error} {message}")

    def perform_checks(self, path):
        """
        checks specified file
        :param path: path to py file to check
        :return: dic {Line: [Codes]}
        """
        pyfile = open(path)
        file_errors = {}
        blank_counter = 0
        blank_issue = False
        for num, line in enumerate(pyfile):
            line = line.strip('\n')
            if not line or line.isspace():
                blank_counter += 1
                blank_issue = True if blank_counter > 2 else False
                continue
            file_errors.update(self.get_line_issues(num+1, line, blanks=blank_issue))

            blank_counter = 0
            blank_issue = False
        pyfile.close()
        ast_errors = self.perform_ast_checks(path)
        for line_error in ast_errors:
            if line_error in file_errors:
                file_errors[line_error].extend(ast_errors[line_error])
            else:
                file_errors[line_error] = ast_errors[line_error]
        return file_errors

    def perform_ast_checks(self, path):
        """
        Performs checks with ast module
        :param path: path to file
        :return: {Line: [Codes]}
        """
        with open(path) as file:
            tree = ast.parse(file.read())
            ast_parser = AstParser()
            ast_parser.visit(tree)
            for line_name in ast_parser.name_errors:
                if line_name in self.name_issues:
                    self.name_issues[line_name].update(ast_parser.name_errors[line_name])
                else:
                    self.name_issues[line_name] = ast_parser.name_errors[line_name]
        return ast_parser.errors


    def get_line_issues(self, num, line, blanks=False):
        """
        Get all issues in line
        :param num: line number
        :param line: line text
        :param blanks: true if more than two preceding blank lines
        :return: {num: [list of errors in line]}
        """
        self.errors = []
        if "class" in line or "def" in line:
            self.get_naming_issues(num, line)
        self.check_len(line)
        self.check_comments(line)
        self.check_indentation(line)
        self.check_unnec_symbs(line)
        if blanks:
            self.errors.append("S006")
        return {num: sorted(self.errors)}

    def get_naming_issues(self, num, line):
        """
        Issues related with function or class name
        :param num: line number
        :param line: line text
        :return: True if found at least one issue
        """
        self.name_issues[num] = {}
        s007 = self.check_spaces(line)
        if s007 is not None:
            self.name_issues[num]["S007"] = s007

        s008 = self.check_class_name(line)
        if s008 is not None:
            self.name_issues[num]["S008"] = s008

        s009 = self.check_def_name(line)
        if s009 is not None:
            self.name_issues[num]["S009"] = s009
        return self.name_issues is not None


    def check_len(self, line):  # S001
        if len(line) > 79:
            self.errors.append("S001")

    def check_comments(self, line):  # S004 S005
        if '#' in line:
            index = line.index('#')
            if (line[index - 1] != ' ' or line[index - 2] != ' ') and index > 1:
                self.errors.append("S004")
            if line.upper().find("TODO") != -1:
                self.errors.append("S005")

    def check_indentation(self, line):  # S002
        for index, char in enumerate(line):
            if char != ' ':
                if index % 4 != 0:
                    self.errors.append("S002")
                break

    def check_unnec_symbs(self, line):  # S003
        if '#' in line:
            line = line[:line.index('#')]
        for char in reversed(line):
            if char != ' ':
                if char == ';':
                    self.errors.append("S003")
                break

    def check_spaces(self, line):  # S007
        match = re.search(r"(class|def)  +.*$", line)
        if match:
            self.errors.append("S007")
            return match.group(1)
        return None

    def check_class_name(self, line):  # S008
        if get_construction_name(line) == "class":
            match = re.search(r"class +([A-Z][a-z0-9]*)+[(:]", line)
            if match is None:
                self.errors.append("S008")
                return get_name(line)
        return None

    def check_def_name(self, line):  # S009
        if get_construction_name(line) == "def":
            match = re.search(r"def +[a-z0-9_]+\(.*$", line)
            if match is None:
                self.errors.append("S009")
                return get_name(line)
        return None


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        analyzer = Analyzer(FileHandler(args[1]))
        analyzer.analyze_all()
    else:
        print("USAGE: python code_analyzer.py directory-or-file")
