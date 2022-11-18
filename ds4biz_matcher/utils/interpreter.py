import ast


def eval_last(text,g=None,l=None):
    p=ast.parse(text)
    expr=p.body.pop(-1).value
    g,l=g or {},l or {}
    exec(compile(p,"<ast>","exec"),g,l)
    temp=compile(ast.Expression(expr),"<ast>","eval")
    return eval(temp,g,l)



