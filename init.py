import sys
from parser import *
import math
from uuid import uuid4

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

builtins["cdr"] = BuiltInFunction(lambda args, scope: args[0][1:])

def add(args, scope):
    out = SchemeData("number",
                     sum([arg.value for arg in args]))
    return out

builtins["+"] = BuiltInFunction(add)
    
def subtract(args, scope):
    if len(args) == 1:
        out = SchemeData("number",
                         0 - args[0].value)
    else:
        out = SchemeData("number",
                         args[0].value - sum([arg.value
                                              for arg in args[1:]]))
    return out

builtins["-"] = BuiltInFunction(subtract)

def multiply(args, scope):
    out = 1.0
    for arg in args:
        out = out * arg.value
    return SchemeData("number", out)

builtins["*"] = BuiltInFunction(multiply)

def divide(args, scope):
    out = args[0].value
    for arg in args[1:]:
        out = out / arg.value
    return SchemeData("number", out)

builtins["/"] = BuiltInFunction(divide)

def list_fn(args, scope):
    out = SchemeList()
    for arg in args:
        out.append(arg)
    return out

builtins["list"] = BuiltInFunction(list_fn)

def equalp(args, scope):
    init = args[0]
    for arg in args[1:]:
        if arg.value != init.value:
            return SchemeData("boolean",
                              False)
    return SchemeData("boolean",
                      True)

builtins["equal?"] = BuiltInFunction(equalp)

builtins["="] = BuiltInFunction(equalp)

def integerp(args, scope):
    return SchemeData("boolean",
                      args[0].value == math.floor(args[0].value))

builtins["integer?"] = BuiltInFunction(integerp)

builtins["length"] = BuiltInFunction(
    lambda args, scope: SchemeData("number", len(args[0])))

def gensym(args, scope):
    return SchemeData("symbol",
                      str(uuid4()))

builtins["gensym"] = BuiltInFunction(gensym)

def type_fn(typ):
    def f(args, scope):
        return SchemeData("boolean",
                          args[0].type_ == typ)
    return f

builtins["symbol?"] = BuiltInFunction(type_fn("symbol"))
builtins["string?"] = BuiltInFunction(type_fn("string"))
builtins["number?"] = BuiltInFunction(type_fn("number"))
builtins["list?"] = BuiltInFunction(type_fn("list"))
builtins["closure?"] = BuiltInFunction(type_fn("closure"))
builtins["boolean?"] = BuiltInFunction(type_fn("boolean"))
builtins["null?"] = BuiltInFunction(type_fn("null"))
builtins["not"] = BuiltInFunction(lambda args, scope:
                                  SchemeData("boolean",
                                             not args[0].value))
