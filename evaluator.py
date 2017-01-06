from tokenizer import Tokenizer
from parser import Parser, SchemeData, SchemeList

null = SchemeData("null", None)

class Scope(dict):
    def __init__(self, parent):
        dict.__init__(self)
        self.parent = parent
    def set(self, name, value):
        if name.type_ == "symbol":
            self[name.value] = value
        else:
            raise Exception("Scheme exception: invalid name %s." % name)
    def look_up(self, name):
        if name.type_ != "symbol":
            raise Exception("Scheme exception: invalid name %s." % name)
        try:
            return self[name.value]
        except KeyError:
            if self.parent != None:
                return self.parent.look_up(name)
            else:
                raise Exception("Scheme exception: symbol %s is undefined." % name)
    
class SchemeFunction(object):
    pass

    
class BuiltInFunction(SchemeData, SchemeFunction):
    def __init__(self, f):
        SchemeData.__init__(self, "closure", f)
        self.f = f
        
    def __call__(self, args, scope):
        return self.f(args, scope)

    def __repr__(self):
        return "closure: built-in-function"

    
class UserDefinedFunction(SchemeData, SchemeFunction):
    def __init__(self, form, arg_names):
        SchemeData.__init__(self, "closure", form)
        self.form = form
        self.arg_names = arg_names

    def __repr__(self):
        return "(lambda (%s) %s)" % (
            " ".join([repr(arg) for arg in self.arg_names]),
            self.form)
        

class Evaluator(object):
    def __init__(self):
        self.global_scope = Scope(None)
        null = SchemeData("null", None)
        
    def _is_atom(self, form):
        return form.type_ in ["string", "number", "boolean"]

    def add_builtin(self, name, func):
        self.global_scope[name] = func
    
    def eval(self, form, scope=None):

        if scope == None:
            scope = self.global_scope

        if self._is_atom(form):
            return form

        elif form.type_ == "symbol":
            return scope.look_up(form)
        
        elif form.type_ == "list":

            init = form[0].value

            if init == "if":
                if self.eval(form[1], scope).value: # #t
                    return self.eval(form[2], scope)
                
                else: # #f
                    if len(form) == 2:
                        return null
                    else:
                        return self.eval(form[3], scope)

            elif init == "quote":

                # don't evaluate the next part of the form
                return form[1]
            
            elif init == "define":
                func_name = form[1][0]
                arg_names = form[1][1:]
                func_forms = form[2:]

                func_form = SchemeList()
                func_form.append(SchemeData("symbol", "begin"))

                for item in func_forms:
                    func_form.append(item)

                func = UserDefinedFunction(func_form, arg_names)
                scope.set(func_name, func)

                # define has no return value

            elif init == "cond":
                
                for item in form[1]:
                    condition, subform = item

                    if self.eval(condition, scope):
                        return self.eval(subform, scope)

                return null
            
            elif init == "begin":
                
                retval = null

                for subform in form[1:]:
                    retval = self.eval(subform, scope)

                return retval
            
            elif init == "let":
                
                retval = null
                
                scope = Scope(scope)

                for defn in form[1]:
                    # evaluate the value expressions in the parent
                    # scope to allow things like (let ((n n)) ...)
                    scope.set(defn[0], self.eval(defn[1], scope.parent))

                for subform in form[2:]:
                    retval = self.eval(subform, scope)

                scope = scope.parent
                
                return retval

            elif init == "let*":

                retval = null
                
                scope = Scope(scope)

                for defn in form[1]:
                    scope.set(defn[0], self.eval(defn[1], scope))

                for subform in form[2:]:
                    retval = self.eval(subform, scope)

                scope = scope.parent
                
                return retval
            
            else:

                # function call
                
                retval = null

                scope = Scope(scope)

                fn = self.eval(form[0], scope)

                if not isinstance(fn, SchemeFunction):
                    raise Exception("Scheme exception: %s is not a function." % form[0])

                values = [self.eval(frm, scope)
                          for frm in form[1:]]

                if isinstance(fn, BuiltInFunction):
                    retval = fn(values, scope)
                    
                else: #not a built-in function
                    
                    if len(values) != len(fn.arg_names):
                        raise Exception("Scheme exception: function %s takes %s arguments; %s provided." %
                                        (form[0], len(fn.arg_names), len(values)))

                    for i in range(len(values)):
                        scope.set(fn.arg_names[i], values[i])

                    retval = self.eval(fn.form, scope)

                scope = scope.parent

                return retval
                    

if __name__ == "__main__":
    import sys, codecs

    t = Tokenizer()
    p = Parser()
    e = Evaluator()

    def show_scope_fn(args, scope):
        if args:
            indent = args[0]
        else:
            indent = ""
            
        for k in scope.keys():
            print(indent, k, ": ", scope[k])
        if scope.parent:
            show_scope_fn([indent + "    "], scope.parent)

        return null

    show_scope = BuiltInFunction(show_scope_fn)

    def display_fn(args, scope):
        arg_vals = [repr(arg) for arg in args]
        sys.stdout.write(" ".join(arg_vals))
        return null

    display = BuiltInFunction(display_fn)

    def newline_fn(args, scope):
        sys.stdout.write("\n")
        return null

    newline = BuiltInFunction(newline_fn)

    def eval_fn(args, scope):
        return e.eval(args[0], scope)

    eval = BuiltInFunction(eval_fn)

    e.add_builtin("show-scope", show_scope)
    e.add_builtin("display", display)
    e.add_builtin("newline", newline)
    e.add_builtin("eval", eval)

    try:
        code = codecs.open(sys.argv[1], "r", "utf-8").read()
    except:
        code = sys.stdin.read()
        
    tokens = t.tokenize(code)
    tree = p.parse(tokens)
    for form in tree:
        e.eval(form)

        
