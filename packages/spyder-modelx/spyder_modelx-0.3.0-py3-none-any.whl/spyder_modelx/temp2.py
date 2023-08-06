

from spyder_modelx.utility.formula import get_funcname

s = """

def foo(x,
        y):
    return 3

"""

print(get_funcname(s))
