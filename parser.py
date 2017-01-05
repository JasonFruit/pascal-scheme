_open_delims = "([{"
_close_delims = "}])"

class SchemeData(object):
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return "%s: %s" % (self.type_, self.value)

class Parser(object):
    def __init__(self):
        pass
    def initialize(self, tokens):
        self.tokens = tokens
        self.parse_tree = [[]]
        self.pos = 0
    def _start_new_list(self):
        new_list = []
        self.parse_tree.append(new_list)
    def _add_atom(self, atom):
        self.parse_tree[-1].append(atom)
    def _close_list(self):
        lst = self.parse_tree.pop()
        self.parse_tree[-1].append(lst)
    def _is_string(self, token):
        return token[0] == "\""
    def _is_number(self, token):
        try:
            _ = float(token)
            return True
        except ValueError:
            return False
    def handle_token(self):
        token = self.tokens[self.pos]
        if token in _open_delims:
            self._start_new_list()
        elif token in _close_delims:
            self._close_list()
        elif self._is_string(token):
            self._add_atom(SchemeData("string",
                                      token[1:-1]))
        elif self._is_number(token):
            self._add_atom(SchemeData("number",
                                      float(token)))
        else:
            self._add_atom(SchemeData("symbol",
                                      token))
        self.pos += 1
    def parse(self, tokens):
        self.initialize(tokens)
        while self.pos < len(tokens):
            self.handle_token()
        return self.parse_tree[-1]

if __name__ == "__main__":
    import sys
    from tokenizer import Tokenizer
    t = Tokenizer()
    code = sys.stdin.read()
    tokens = t.tokenize(code)
    p = Parser()
    tree = p.parse(tokens)
    print(tree)
