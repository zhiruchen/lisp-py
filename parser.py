"""
lisp parser
"""
# encoding: utf-8

Symbol = str
List = list
Number = (int, float)

def read_from_tokens(tokens):
    """read an expression from tokens"""
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF while reading!")

    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif ')' == token:
        raise SyntaxError("unexpected )")
    else:
        return atom(token)


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def tokenize(program):
    """xxx"""
    return program.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program):
    """parse"""
    return read_from_tokens(tokenize(program))
