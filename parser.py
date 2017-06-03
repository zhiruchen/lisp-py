# encoding: utf-8

"""
lisp parser
"""


import math
import operator as op

Symbol = str
List = list
Number = (int, float)
Env = dict

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
    """token to int/float/symbol"""
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


def standard_env():
    """标准环境"""
    env = Env()
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.div,
        '>': op.gt, '>=': op.ge, '<': op.lt, '<=': op.le, '=':op.eq,
        'abs': abs,
        'append': op.add,
        'apply': apply,
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol)
    })
    return env

global_env = standard_env()

def eval(x, env=global_env):
    """表达式求值"""
    if isinstance(x, Symbol):  # 变量引用
        return env[x]
    elif not isinstance(x, list):  # 常量
        return x
    elif x[0] == 'if':  # 条件表达式
        _, test, conseq, alt = x
        exp = conseq if eval(test, env) else alt
        return eval(exp, env)
    elif x[0] == 'define':  # 变量定义
        _, var, exp = x
        env[var] = eval(exp, env)
    else:                  # procedure call
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)

def repl(promt='lis.py> '):
    while True:
        val = eval(parse(raw_input(promt)))
        if val is not None:
            print schemestr(val)

def schemestr(exp):
    "convert Python obj into scheme str"
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    return str(exp)
