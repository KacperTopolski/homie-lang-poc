from lex import lex
from parsing.parse import parse
from tree import ProgramNode
from tokens import Source
from typechecking.typechecker import typecheck
from ast_to_ll import to_ll
from compiler import compile
from parsing.combinators import Result, ResultStatus
from error_reporting import print_error, print_error_report
import sys

def nice_print(s: str):
    l = 0
    r = ""
    for c in s:
        if c in '<{[(':
            l += 1
        if len(r) == 0 or r[-1] == '\n':
            r += ' ' * l * 4
        if c != ',':
            r += c
        if c in '<>{[()]}':
            r += '\n'
        if c in '>}])':
            l -= 1
    print(r)

def run_file(file):
    with open(file, "r") as f:
        source = Source(file, f.read())

    tokens = lex(source)
    # print("TOKENS")
    # print(tokens)
    parsing_result = parse(tokens)
    # print("PARSING RES")
    # nice_print(str(parsing_result.parsed))

    if parsing_result.status == ResultStatus.Ok:
        program = parsing_result.parsed

        ctx, report = typecheck(program)

        if report.has_errors():
            print('typecheck fail')
            print_error_report(report)
        else:
            program = to_ll(program, ctx)

            # print(program.pretty_print(), file=sys.stderr)
            print(compile(program))
    else:
        print('parse fail')
        for error in parsing_result.errors:
            print_error(error)


if __name__ == "__main__":
    # nice_print('([],[])')
    run_file(sys.argv[1])
