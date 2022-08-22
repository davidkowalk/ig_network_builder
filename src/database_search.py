#I am hella drunk while writing this, so dont expect too much

markers = "()&"
keys = ["and", "or", "not"]
forbidden = "#/\"'"

#############################
#           LEXER           #
#############################

class token:
    def __init__(self, type, content):
        self.type = type
        self.content = content

    def __str__(self):
        return f"Token({self.type}, \"{self.content}\")"

    def __repr__(self):
        return self.__str__()

def get_str(code, i):
    ret_str = ""
    while i < len(code) and not (code[i] in markers or code[i].isspace()):
        ret_str += code[i]
        i += 1

    return ret_str, i

def skip_whitespace(code, i):
    while code[i].isspace():
        i += 1

    return i

def tokenize(code):

    tokens = list()
    i = 0 # saves current position in string

    while i < len(code):

        if code[i] in markers:

            if code[i] == "(":
                tokens.append(token("lparen", code[i]))
            elif code[i] == ")":
                tokens.append(token("rparen", code[i]))
            elif code[i] == "&":
                tokens.append(token("and", code[i]))

            i += 1

        elif code[i].isspace():
            i = skip_whitespace(code, i)

        elif code[i] not in markers and not code[i] in forbidden:
            term, i = get_str(code, i)

            if term not in keys:
                tokens.append(token("word", term))
            else:
                if term == "and":
                    tokens.append(token("and", term))
                elif term == "or":
                    tokens.append(token("or", term))
                elif term == "not":
                    tokens.append(token("not", term))

        else:
            print(f"[Tokenize] Unexpected character: {code[i]} at {i}, skipping!")
            i += 1

    return tokens


#------------------------------------------------------------------------------------

##################
#     Parser     #
##################

WORD, AND, OR, LPAREN, RPAREN, NOT = ("word", "and", "or", "lparen", "rparen", "not")

class AST(object):

    def __init__(self):
        pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, child):
        self.child = child
        self.token = self.op = op

class Word(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.content

class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.current_token = self.tokens[self.i]

    def next_token(self):
        self.i += 1
        if self.i >= len(self.tokens):
            return

        self.current_token = self.tokens[self.i]

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.

        if self.current_token.type == token_type:
            self.next_token()
        else:
            self.error()

    def expr(self):
        """
        expr: term ((AND | OR) term)*
        """

        node = self.term()

        while self.current_token.type in (AND, OR):
            token = self.current_token

            if token.type == AND:
                self.eat(AND)
            elif token.type == OR:
                self.eat(OR)

            node = BinOp(left = node, op=token, right=self.term())

        return node

    def term(self):
        """
        term: WORD | LPAREN expr RPAREN | NOT expr
        """

        token = self.current_token

        if token.type == WORD:
            self.eat(WORD)
            return Word(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == NOT:
            op = token
            self.eat(NOT)
            node = UnaryOp(token, self.expr())
            return node

    def parse(self):
        return self.expr()

def build_tree(tokens):

    """
    Takes token stream and returns a node tree of commands
    """
    #raise ValueError(f"Unclosed Paranthesees at {i}")

    parser = Parser(tokens)
    tree = parser.parse()

    return tree

def get_tree(code):

    token_stream = tokenize(code)
    return build_tree(token_stream)

# ---------------------------------------------
from sys import argv as args
import json
#python3 database_search.py <json file> <search expression>

def match(net, user, top_node):

    if type(top_node) == Word:
        parent = top_node.value

        if parent not in net:
            print(f"No network data for \"{parent}\"")
            exit()

        return user in net[parent]["follows"]

    elif type(top_node) == BinOp:

        if top_node.op.type == "and":
            return match(net, user, top_node.left) and match(net, user, top_node.right)
        elif top_node.op.type == "or":
            return match(net, user, top_node.left) or match(net, user, top_node.right)
        else:
            raise Exception(f"Invalid Binary Operator \"{top_node.op}\"")

    elif type(top_node) == UnaryOp:

        if top_node.op.type == "not":
            return not match(net, user, top_node.child)
        else:
            raise Exception(f"Invalid Unary Operator \"{top_node.op}\"")

def help():
    print("""
    Search Syntax: python3 database_search.py <json file> <search expression>
    Returns all users matching the search expression

    Search expression:
    > (a or b) and not (c or d)
    Returns all accounts followed by a or b but excludes all accounts followed by c or d

    Data Syntax: python3 database_search.py <json file> -d
    Prints all accounts with data available.
    """)

def main():

    if args[1] == "-h":
        help()
        return


    with open(args[1], "r") as fp:
        net = json.load(fp)

    if args[2] == "-d":
        print("Data available for:")
        for user in net:
            print(user, end = ", ")

        print("")
        return

    expr = get_tree(args[2])
    print(args[2])

    #build list of all users
    users_in_net = list()
    for user in net:
        users_in_net.append(user)
        users_in_net += net[user]["follows"]

    users_in_net_clean = [ii for n,ii in enumerate(users_in_net) if ii not in users_in_net[:n]]
    #print(users_in_net_clean)

    matched = list()
    for user in users_in_net_clean:
        #print(f"Check {user}")
        if match(net, user, expr):
            matched.append(user)

    print(matched)


if __name__ == '__main__':
    main()
