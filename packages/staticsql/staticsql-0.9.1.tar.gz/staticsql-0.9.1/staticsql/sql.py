import os
import codecs
import re
import collections

lexer = (
    ("NEWLINE", r"(\r\n)"),
    ("WS", r"(\s+)"),

    ("CREATE", r"(create)\b"),
    ("TABLE", r"(table)\b"),
    ("CONSTRAINT", r"(constraint)\b"),
    ("PRIMARY", r"(primary|\[primary\])\b"),
    ("CLUSTERED", r"(clustered)\b"),
    ("ASC", r"(asc)\b"),
    ("DESC", r"(desc)\b"),
    ("WITH", r"(with)\b"),
    ("KEY", r"(key)\b"),
    ("NOT", r"(not)\b"),
    ("NULL", r"(null)\b"),
    ("MAX", r"(max)\b"),

    ("COMMENT", r"(/\*[^*]*\*/)"),

    ("PERIOD", r"(\.)"),
    ("COMMA", r"(,)"),
    ("LPAREN", r"(\()"),
    ("RPAREN", r"(\))"),
    ("STRING", r"('[^']+')"),
    ("DIGITS", r"(\-?\d+)"),
    ("QNAME", r"\[([^\]]+)\]"),
    ("NAME", r"([_a-zæøå][_a-zæøå0-9]*)"),
    ("JUNK", r"([^\s]+)"),
)

lexer = [(token_type, re.compile(regex, re.I)) for (token_type, regex) in lexer]

class Token(object):
    def __init__(self, typename, value, line_number, column_number):
        self.typename = typename
        self.value = value
        self.line_number = line_number
        self.column_number = column_number

    def __repr__(self):
        return f"<Token {self.typename} @ [L{self.line_number}:C{self.column_number}] '{self.value}'>"

def gettokens(sql):
    tokens = []
    pos = 0
    line_number = 1
    column_number = 1
    while pos < len(sql):
        for token_type, regex in lexer:
            m = regex.match(sql, pos)
            if m:
                a, b = m.span(1)
                pos = m.span(0)[1]
                if token_type in ("NEWLINE"):
                    line_number += 1
                    column_number = 1
                    break
                if not token_type in ("WS", "COMMENT"):
                    tokens.append(Token(token_type, sql[a:b], line_number, column_number))
                break
        else:
            raise Exception("No match", sql[pos:pos+10])
    return tokens

class ParseException(Exception):
    pass

class Parser(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.pos = 0
        self.tokens = []
        self.table = collections.OrderedDict({
            "schema": None,
            "name": None,
            "tags": [],
            "attributes": [],
        })
        

    def parse(self, sql):
        self.tokens = gettokens(sql)
        while not self.lookahead("CREATE"):
            self.skip()
        self.expect("CREATE")
        self.expect("TABLE")
        pos = self.pos
        try:
            self.table["schema"] = self.expect("NAME", "QNAME").value
            self.expect("PERIOD")
            self.table["name"]   = self.expect("NAME", "QNAME").value
        except ParseException:
            self.pos = pos
            self.table["schema"] = 'dbo'
            self.table["name"] = self.expect("NAME", "QNAME").value

        self.expect("LPAREN")

        while not self.lookahead("RPAREN"):
            if self.lookahead("CONSTRAINT", "PRIMARY"):
                skipped_tokens = list(self.skip_until("COMMA", "RPAREN"))
                at = skipped_tokens[0].line_number
                print(f"Line {at}: Skipped " + " ".join(token.value for token in skipped_tokens))

            else:
                self.table["attributes"].append(self.attribute())

            next_token = self.lookahead()
            if not next_token.typename in ("COMMA", "RPAREN"):
                raise ParseException(next_token, "Comma or right paren expected")
            if next_token.typename == "COMMA":
                self.expect("COMMA")
        self.expect("RPAREN")


    def attribute(self):
        attribute = {}
        attribute["name"] = self.expect("NAME", "QNAME").value
        attribute["data_type"] = self.data_type()
        while not self.lookahead("COMMA", "RPAREN"):
            pos = self.pos
            try:
                self.expect("NOT")
                self.expect("NULL")
                attribute["is_nullable"] = False
                continue
            except:
                self.pos = pos

            try:
                self.expect("NULL")
                attribute["is_nullable"] = True
                continue
            except:
                self.pos = pos

            self.skip_any()

        return attribute


    def data_type(self):
        typename = self.expect("NAME", "QNAME").value.upper()
        if not self.lookahead().typename == "LPAREN":
            return typename

        pos = self.pos
        try:
            self.expect("LPAREN")
            self.expect("MAX")
            self.expect("RPAREN")
            return f"{typename}(MAX)"
        except ParseException:
            self.pos = pos

        try:
            self.expect("LPAREN")
            length = self.expect("DIGITS").value
            self.expect("RPAREN")
            return f"{typename}({length})"
        except ParseException:
            self.pos = pos

        try:
            self.expect("LPAREN")
            length = self.expect("DIGITS").value
            self.expect("COMMA")
            precision = self.expect("DIGITS").value
            self.expect("RPAREN")
            return f"{typename}({length}, {precision})"
        except ParseException:
            self.pos = pos

    def lookahead(self, *type_names):
        if type_names:
            next_token = self.lookahead()
            if next_token.typename in type_names:
                return next_token
            else:
                return None
        return self.tokens[self.pos]

    def expect(self, *token_types):
        token = self.tokens[self.pos]
        if token.typename in token_types:
            self.pos += 1
            return token
        else:
            raise ParseException(token)

    def skip(self):
        token = self.lookahead()
        self.pos += 1
        return token


    def skip_any(self):
        if self.lookahead().typename == "LPAREN":
            return self.skip_paren()
        else:
            return [self.skip()]

    def skip_until(self, *typenames):
        tokens = []
        while not self.lookahead(*typenames):
            tokens.extend(self.skip_any())
        return tokens

    def skip_paren(self):
        tokens = []
        tokens.append(self.expect("LPAREN"))
        while self.lookahead().typename != "RPAREN":
            if self.lookahead().typename == "LPAREN":
                tokens.extend(self.skip_paren())
            else:
                tokens.append(self.skip())
        tokens.append(self.expect("RPAREN"))
        return tokens

def from_sql(sql, verbose=False):
    parser = Parser(verbose)
    parser.parse(sql)
    return parser.table
