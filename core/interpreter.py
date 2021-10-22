from rply import LexerGenerator, ParserGenerator

lg = LexerGenerator()
lg.add('or', r'or')
lg.add('and', r'and')
lg.add('not', r'not')
lg.add('in', r'in')
lg.add('float', r'[-+]?[0-9]*\.?[0-9]+')
lg.add('num', r'\d+')
# lg.add('=', r'\=')
lg.add('==', r'\==')
lg.add('>=', r'\>=')
lg.add('<=', r'\<=')
lg.add('>', r'\>')
lg.add('<', r'\<')
lg.add('+', r'\+')
lg.add('-', r'\-')
lg.add('*', r'\*')
lg.add('/', r'\/')
lg.add('^', r'\^')
lg.add('(', r'\(')
lg.add(')', r'\)')
lg.add('colon', r'\"')
lg.add('str', r'\w*')

lg.ignore(r'\s+')

l = lg.build()

# for token in l.lex('"asd" in "cc21_asd"'): print(token)

dic = {}

pg = ParserGenerator(
    ['or', 'and', 'not', 'in', 'num', 'float', 'str', '>=', '<=', '>', '<', '==', '+', '-', '*', '/', '^', '(', ')', 'colon'],
    precedence=[
        ('left', ['or']),
        ('left', ['and']),
        ('left', ['not']),
        ('left', ['>', '<','>=', '<=', '==', 'in']),
        ('left', ['+', '-']),
        ('left', ['*', '/']), 
        ('right', ['^'])]
)

@pg.production('expression : num')
def exp_num(p):
    return int(p[0].value)

@pg.production('expression : float')
def exp_float(p):
    return p[0].value

@pg.production('expression : str')
def exp_str(p):
    return str(p[0].value)

@pg.production('expression : colon str colon')
def exp_colon(p):
    return p[1].value

@pg.production('expression : ( expression )')
def exp_br(p):
    return p[1]

@pg.production('expression : not expression')
def exp_not(p):
    return not p[1]

@pg.production('expression : expression or expression')
@pg.production('expression : expression and expression')
@pg.production('expression : expression >= expression')
@pg.production('expression : expression <= expression')
@pg.production('expression : expression > expression')
@pg.production('expression : expression < expression')
@pg.production('expression : expression == expression')
@pg.production('expression : expression in expression')
@pg.production('expression : expression + expression')
@pg.production('expression : expression - expression')
@pg.production('expression : expression * expression')
@pg.production('expression : expression / expression')
@pg.production('expression : expression ^ expression')
def expression_op(p):
    left = p[0]
    op = p[1]
    right = p[2]
    if op.gettokentype() == "or": return left or right
    elif op.gettokentype() == "and": return left and right
    elif op.gettokentype() == ">=": return left >= right
    elif op.gettokentype() == "<=": return left <= right
    elif op.gettokentype() == ">": return left > right
    elif op.gettokentype() == "<": return left < right
    elif op.gettokentype() == "==": return left == right
    elif op.gettokentype() == "in": return left in right
    elif op.gettokentype() == "+": return left + right
    elif op.gettokentype() == "-": return left - right
    elif op.gettokentype() == "*": return left * right
    elif op.gettokentype() == "/": return left / right
    elif op.gettokentype() == "^": return left ** right
    else: raise AssertionError('Oops, this should not be possible!')

@pg.error
def error_handler(token):
    raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())

p = pg.build()

def interpreter(expr):
    # 调用Interpreter解析表达式
    print('from interpreter: ', expr)
    return p.parse(l.lex(expr))
