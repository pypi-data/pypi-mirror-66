import re
from typing import Pattern, List

patterns: List[Pattern[str]] = [
    re.compile(pattern=r'ObjectId\((.*)\)'),
    re.compile(pattern=r'ISODate\((.*)\)'),
    re.compile(pattern=r'NumberLong\((.*)\)'),
    re.compile(pattern=r'NumberInt\((.*)\)'),
    re.compile(pattern=r'NumberDecimal\("(.*)"\)'),
]


def apply_rule(pattern: Pattern[str], string: str) -> str:
    return pattern.sub(repl=r'\1', string=string)


def clean_line(line: str) -> str:
    for pattern in patterns:
        line = apply_rule(pattern=pattern, string=line)

    return line


def clean(string: str) -> str:
    clean_string = ''

    for line in string.splitlines():
        clean_string += clean_line(line=line)

    return clean_string
