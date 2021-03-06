_delims = "(){}[]"
_white = " \n\t\v"
_string_delim = '"'
_escape_char = '\\'

class Tokenizer(object):
    def __init__(self):
        pass
    def initialize(self, code):
        self.code = code
        self.in_string = False
        self.in_comment = False
        self.tokens = []
        self.acc = []
        self.pos = 0
    def _prev_char(self):
        return self.code[self.pos - 1]
    def _next_char(self):
        return self.code[self.pos + 1]
    def _maybe_add_token(self):
        if self.acc:
            self.tokens.append("".join(self.acc))
        self.acc = []
    def handle_char(self):
        c = self.code[self.pos]
        if self.in_comment:
            if c == "\n":
                self.in_comment = False
        elif self.in_string:
            if c == _string_delim and self._prev_char() != _escape_char:
                self.acc.append(c)
                self._maybe_add_token()
                self.in_string = False
            else:
                self.acc.append(c)
        elif c == _string_delim:
            self._maybe_add_token()
            self.acc.append(c)
            self.in_string = True
        elif c in _delims:
            if self.in_string:
                self.acc.append(c)
            else:
                self._maybe_add_token()
                self.acc.append(c)
                self._maybe_add_token()
        elif c in _white:
            self._maybe_add_token()
        elif c == ";":
            self._maybe_add_token()
            self.in_comment = True
        else:
            self.acc.append(c)
            
        self.pos += 1
        
                
    def tokenize(self, code):
        self.initialize(code)
        while self.pos < len(self.code):
            self.handle_char()

        return self.tokens

if __name__ == "__main__":
    import sys

    code = sys.stdin.read()
    t = Tokenizer()
    print(t.tokenize(code))
        
