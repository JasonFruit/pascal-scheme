import sys
from parser import *

builtins = {}

def show_scope(args, scope):
    if args:
        indent = args[0]
    else:
        indent = ""

    for k in scope.keys():
        print(indent, k, ": ", scope[k])
    if scope.parent:
        show_scope([indent + "    "], scope.parent)

    return null

builtins["show-scope"] = BuiltInFunction(show_scope)

def display(args, scope):
    arg_vals = [repr(arg) for arg in args]
    sys.stdout.write(" ".join(arg_vals))
    return null

builtins["display"] = BuiltInFunction(display)

def newline(args, scope):
    sys.stdout.write("\n")
    return null

builtins["newline"] = BuiltInFunction(newline)

def cons(args, scope):
    item, lst = args
    out = SchemeList()
    out.append(item)
    for thing in lst:
        out.append(thing)
    return out

builtins["cons"] = BuiltInFunction(cons)

builtins["car"] = BuiltInFunction(lambda args, scope: args[0][0])

def add(args, scope):
    out = SchemeData("number",
                     sum([arg.value for arg in args]))
    return out

builtins["+"] = BuiltInFunction(add)
    
