# Static Code Analyzer for Python
## General info
This project can detect some common stylistic issues like incorrect indentation, trailing semicolons, incorrect class or def name etc. Graduate project for [JetBrains Academy](https://hyperskill.org)
## Recognizable stylistic issues
* ### S001 - Too long line
    Line with 80 and more characters
* ### S002 - Indentation is not a multiple of four
    Lines with not common indentation (only checks proper numbers of spaces)
* ### S003 - Unnecessary semicolon after a statement
    Note that semicolons are acceptable in comments
* ### S004 -  Less than two spaces before inline comments
* ### S005 - TODO found
    Checks only in comments only and case-insensitive
* ### S006 - More than two blank lines preceding a code line
    Applies to the first non-empty line
* ### S007 - Too many spaces after construction_name (def or class)
* ### S008 - Class name class_name should be written in CamelCase
* ### S009 - Function name function_name should be written in snake_case
* ### S010 - Argument name arg_name should be written in snake_case
* ### S011 - Variable var_name should be written in snake_case
  Only in functions. The error message for an invalid variable name should be output only when this variable is assigned a value.
* ### S012 - The default argument value is mutable
## Input and output format
Program can analyze file or files within giver directory. To run the analyzer, you need to supply a directory path or a path to the file:
`#python code_analyzer.py directory-or-file`

Output format looks like this:
`Path: Line: Code Message`

## Test cases
To launch tests, run the command::
`python code_analyzer.py test_dir`