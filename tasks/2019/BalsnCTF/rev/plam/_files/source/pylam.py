import functools
import string


_cur_id = 0
def gen_id():
    global _cur_id
    _cur_id += 1
    return _cur_id


def puremethod(func):
    attr = f'_pureval_{func.__name__}'
    @functools.wraps(func)
    def inner(self):
        if hasattr(self, attr):
            return getattr(self, attr)
        val = func(self)
        setattr(self, attr, val)
        return val
    return inner


charset = set(string.ascii_lowercase)


class Variable(object):
    def __init__(self, name, showid=True):
        self.name = name
        self.id = gen_id()
        self.showid = showid

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        if self.showid:
            return f'{self.name}{self.id}'
        else:
            return f'{self.name}'

    def sub(self, var, value):
        if self == var:
            return value
        return self

    def eval(self):
        return self

    def simplify(self):
        return self

    def alpha_norm(self):
        return self

    @puremethod
    def freevar(self):
        return set([self])


class Abstraction(object):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def __repr__(self):
        expr = repr(self.expr)
        if not isinstance(self.expr, Variable):
            expr = expr[1:-1]
        return f'(λ{self.var}.{expr})'

    @puremethod
    def __hash__(self):
        return hash((self.var, self.expr))

    def __eq__(self, other):
        return self.var == other.var and self.expr == other.expr

    def __call__(self, arg):
        return self.expr.sub(self.var, arg)

    def eval(self):
        return self

    def simplify(self):
        return Abstraction(self.var, self.expr.simplify())

    def alpha_norm(self):
        var = min(charset - set([v.name for v in self.freevar()]))
        var = Variable(var, showid=False)
        return Abstraction(var, self(var).alpha_norm())

    def sub(self, var, value):
        if var not in self.freevar():
            return self
        expr = self.expr.sub(var, value)
        return Abstraction(self.var, expr)

    @puremethod
    def freevar(self):
        return self.expr.freevar() - set([self.var])


class Application(object):
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __repr__(self):
        func = repr(self.func)
        if isinstance(self.func, Application):
            func = func[1:-1]
        return f'({func} {self.arg})'

    @puremethod
    def __hash__(self):
        return hash((self.func, self.arg))

    def __eq__(self, other):
        return self.func == other.func and self.arg == other.arg

    def reducible(self):
        return isinstance(self.func, Abstraction)

    def apply(self):
        return self.func.eval()(self.arg)

    def eval(self):
        return self.apply().eval()

    def simplify(self):
        func = self.func.simplify()
        arg = self.arg.simplify()
        if isinstance(func, Abstraction):
            return func(arg).simplify()
        return Application(func, arg)

    def alpha_norm(self):
        return Application(self.func.alpha_norm(), self.arg.alpha_norm())

    def sub(self, var, value):
        if var not in self.freevar():
            return self
        func = self.func.sub(var, value)
        arg = self.arg.sub(var, value)
        return Application(func, arg)

    @puremethod
    def freevar(self):
        return self.func.freevar() | self.arg.freevar()
