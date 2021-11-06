#Static Code Analyzer for Python
##General info
This project can detect come common stylistic issues like wrong indentation, trailing semicolons, wrong class or def name etc. Graduate project for [JetBrains Academy](https://hyperskill.org)
##Recognizable stylistic issues
* ###S001 - Too long line
    Line with 80 and more characters
* ###S002 - Indentation is not a multiple of four
    Lines with not common indentation (only checks proper numbers of spaces)
* ###S003 - Unnecessary semicolon after a statement
    Note that semicolons are acceptable in comments
* ###S004 -  Less than two spaces before inline comments
* ###S005 - TODO found
    Checks only in comments only and case-insensitive
* ###S006 - More than two blank lines preceding a code line
    Applies to the first non-empty line
* ###S007 - Too many spaces after construction_name (def or class)
* ###S008 - Class name class_name should be written in CamelCase
* ###S009 - Function name function_name should be written in snake_case
##Input and output format
Program can analyze file or files within giver directory. For starting, need one parameter - path to file or directory:
`#python code_analyzer.py directory-or-file`

Output format looks like this:
`Path: Line: Code Message`

##Test cases
To analyze test python files you can run this as follows:
`python code_analyzer.py test_dir`