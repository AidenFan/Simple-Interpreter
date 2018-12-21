from utils import Token_Type
from utils import ExprNode
from utils import syntax_error
from Lexer import Lexer
from utils import set_param, get_param, change_param
import math
import matplotlib.pyplot as plt

Origin_x = 0.0
Origin_y = 0.0
Rot_ang = 0.0
Scale_x = 1
Scale_y = 1
Color = 'BLACK'


def set_origin(x, y):
    global Origin_x, Origin_y
    Origin_x = x
    Origin_y = y
    print("^^^^^^^^^^^Set Origin^^^^^^^^^^^^")
    print(str(Origin_x) + ' ' + str(Origin_y))


def set_scale(x, y):
    global Scale_x, Scale_y
    Scale_x = x
    Scale_y = y
    print("^^^^^^^^^^^Set Scale^^^^^^^^^^^^")
    print(str(Scale_x) + ' ' + str(Scale_y))


def set_rot(x):
    global Rot_ang
    Rot_ang = x
    print("^^^^^^^^^^^Set Rot^^^^^^^^^^^^")
    print(str(Rot_ang))


def set_color(x):
    global Color
    Color = x
    print("^^^^^^^^^^^Set Color^^^^^^^^^^^^")
    print(Color)


def get_expr_value(root):
    if root is None:
        return 0.0
    if root.type == Token_Type.PLUS.name:
        return float(get_expr_value(root.left)) + float(get_expr_value(root.right))
    elif root.type == Token_Type.MINUS.name:
        return float(get_expr_value(root.left)) - float(get_expr_value(root.right))
    elif root.type == Token_Type.MUL.name:
        return float(get_expr_value(root.left)) * float(get_expr_value(root.right))
    elif root.type == Token_Type.DIV.name:
        return float(get_expr_value(root.left)) / float(get_expr_value(root.right))
    elif root.type == Token_Type.FUNC.name:
        return float(root.func(get_expr_value(root.left)))
    elif root.type == Token_Type.CONST_ID.name:
        return float(root.value)
    elif root.type == Token_Type.T.name:
        return float(root.get_param())
    return 0.0


def cal_coord(x_ptr, y_ptr):
    global Origin_x, Origin_y, Scale_x, Scale_y
    x = get_expr_value(x_ptr)
    y = get_expr_value(y_ptr)
    # scale transformation
    x *= Scale_x
    y *= Scale_y
    # rotation
    temp = x * math.cos(Rot_ang) + y * math.sin(Rot_ang)
    y = y * math.cos(Rot_ang) - x * math.sin(Rot_ang)
    x = temp
    # translation
    x += Origin_x
    y += Origin_y
    return x, y


def draw_loop(start, end, step, x_ptr, y_ptr):
    global Color
    set_param(start)
    while get_param() <= end:
        x, y = cal_coord(x_ptr, y_ptr)
        # print(str(x) + ", " + str(y))
        if Color == 'RED':
            plt.plot(x, y, 'r.')
        elif Color == 'GREEN':
            plt.plot(x, y, 'g.')
        elif Color == 'BLUE':
            plt.plot(x, y, 'b.')
        else:
            plt.plot(x, y, 'k.')
        change_param(step)


def close_scanner():
    print("Close scanner")


def print_tree(root):
    if root is not None:
        root.show()
        print("left_child: ")
        print_tree(root.left)
        print("right_child: ")
        print_tree(root.right)


class Parser:
    def __init__(self, filename):
        self.lexer = Lexer(filename)
        self.token = None
        self.root = None

    def start(self):
        print("-----Enter Start-----")
        self.lexer.start()
        self.fetch_token()
        self.program()
        close_scanner()
        print("-----Exit Start-----")

    def fetch_token(self):
        print("-----Enter FetchToken-----")
        self.token = self.lexer.gettoken()
        # self.token.show()
        if self.token.type == Token_Type.ERRTOKEN.name:
            syntax_error(1)
        print("-----Exit FetchToken-----")

    def match_token(self, ob):
        print("-----Enter MatchToken-----")
        if self.token.type != ob:
            syntax_error(2, sb=self.token.type, ob=ob)
            print("-----Exit MatchToken-----")
            return False
        print("*****MatchToken " + ob + "*****")
        print("-----Exit MatchToken-----")
        return True

    def program(self):
        print("-----Enter Program-----")
        while self.token.type != Token_Type.NONTOKEN.name:
            self.statement()
            # end with ';'
            self.match_token(Token_Type.SEMICO.name)
            self.fetch_token()
        print("-----Exit Program-----")

    def statement(self):
        print("-----Enter Statement-----")
        if self.token.type == Token_Type.ORIGIN.name:
            self.origin_statement()
        elif self.token.type == Token_Type.SCALE.name:
            self.scale_statement()
        elif self.token.type == Token_Type.ROT.name:
            self.rot_statement()
        elif self.token.type == Token_Type.FOR.name:
            self.for_statement()
        elif self.token.type == Token_Type.COLOR.name:
            self.color_statement()
        else:
            syntax_error(3)
        print("-----Exit Statement-----")

    def origin_statement(self):
        print("-----Enter OriginStatement-----")
        self.match_token(Token_Type.ORIGIN.name)
        self.fetch_token()
        self.match_token(Token_Type.IS.name)
        self.fetch_token()
        self.match_token(Token_Type.L_BRACKET.name)
        self.fetch_token()
        tmp_ptr = self.expression()
        print("--------------------------------------------------")
        print_tree(tmp_ptr)
        print("--------------------------------------------------")

        x = get_expr_value(tmp_ptr)

        self.match_token(Token_Type.COMMA.name)
        self.fetch_token()
        tmp_ptr = self.expression()
        print("--------------------------------------------------")
        print_tree(tmp_ptr)
        print("--------------------------------------------------")

        y = get_expr_value(tmp_ptr)

        self.match_token(Token_Type.R_BRACKET.name)
        self.fetch_token()

        set_origin(x, y)

        print("-----Exit OriginStatement-----")

    def scale_statement(self):
        print("-----Enter ScaleStatement-----")
        self.match_token(Token_Type.SCALE.name)
        self.fetch_token()
        self.match_token(Token_Type.IS.name)
        self.fetch_token()
        self.match_token(Token_Type.L_BRACKET.name)
        self.fetch_token()
        tmp_ptr = self.expression()
        print("--------------------------------------------------")
        print_tree(tmp_ptr)
        print("--------------------------------------------------")

        x = get_expr_value(tmp_ptr)

        self.match_token(Token_Type.COMMA.name)
        self.fetch_token()
        tmp_ptr = self.expression()
        print("--------------------------------------------------")
        print_tree(tmp_ptr)
        print("--------------------------------------------------")

        y = get_expr_value(tmp_ptr)

        self.match_token(Token_Type.R_BRACKET.name)
        self.fetch_token()

        set_scale(x, y)

        print("-----Exit ScaleStatement-----")

    def rot_statement(self):
        print("-----Enter RotStatement-----")
        self.match_token(Token_Type.ROT.name)
        self.fetch_token()
        self.match_token(Token_Type.IS.name)
        self.fetch_token()
        tmp_ptr = self.expression()
        print("--------------------------------------------------")
        print_tree(tmp_ptr)
        print("--------------------------------------------------")

        x = get_expr_value(tmp_ptr)

        # self.fetch_token()

        set_rot(x)
        print("-----Exit RotStatement-----")

    def for_statement(self):
        print("-----Enter ForStatement-----")
        self.match_token(Token_Type.FOR.name)
        self.fetch_token()
        self.match_token(Token_Type.T.name)
        self.fetch_token()
        self.match_token(Token_Type.FROM.name)
        self.fetch_token()
        start_ptr = self.expression()
        print("--------------------------------------------------")
        print_tree(start_ptr)
        print("--------------------------------------------------")

        start = get_expr_value(start_ptr)

        self.match_token(Token_Type.TO.name)
        self.fetch_token()
        end_ptr = self.expression()
        print("--------------------------------------------------")
        print_tree(end_ptr)
        print("--------------------------------------------------")

        end = get_expr_value(end_ptr)

        self.match_token(Token_Type.STEP.name)
        self.fetch_token()
        step_ptr = self.expression()
        print("--------------------------------------------------")
        print_tree(step_ptr)
        print("--------------------------------------------------")

        step = get_expr_value(step_ptr)

        self.match_token(Token_Type.DRAW.name)
        self.fetch_token()
        self.match_token(Token_Type.L_BRACKET.name)
        self.fetch_token()
        x_ptr = self.expression()
        print("--------------------------------------------------")
        print_tree(x_ptr)
        print("--------------------------------------------------")
        self.match_token(Token_Type.COMMA.name)
        self.fetch_token()
        y_ptr = self.expression()
        print("--------------------------------------------------")
        print_tree(y_ptr)
        print("--------------------------------------------------")
        self.match_token(Token_Type.R_BRACKET.name)
        self.fetch_token()

        draw_loop(start, end, step, x_ptr, y_ptr)

        print("-----Exit ForStatement-----")

    def color_statement(self):
        print("-----Enter ColorStatement-----")
        self.match_token(Token_Type.COLOR.name)
        self.fetch_token()
        self.match_token(Token_Type.IS.name)
        self.fetch_token()
        self.match_token(Token_Type.SP_COLOR.name)

        set_color(self.token.lexeme)

        self.fetch_token()
        print("-----Exit ColorStatement-----")

    def expression(self):
        print("-----Enter Expression-----")
        left = self.term()
        while self.token.type == Token_Type.PLUS.name or self.token.type == Token_Type.MINUS.name:
            token_tmp = self.token.type
            self.match_token(token_tmp)
            right = self.term()
            left = ExprNode(token_tmp, lnode=left, rnode=right)
        print("-----Exit Expression-----")
        return left

    def term(self):
        print("-----Enter Term-----")
        left = self.factor()
        while self.token.type == Token_Type.MUL.name or self.token.type == Token_Type.DIV.name:
            token_tmp = self.token.type
            self.match_token(token_tmp)
            self.fetch_token()
            right = self.factor()
            left = ExprNode(token_tmp, lnode=left, rnode=right)
        print("-----Exit Term-----")
        return left

    def factor(self):
        print("-----Enter Factor-----")
        if self.token.type == Token_Type.PLUS.name or self.token.type == Token_Type.MINUS.name:
            token_tmp = self.token.type
            self.match_token(token_tmp)
            left = ExprNode(Token_Type.CONST_ID.name, 0)
            self.fetch_token()
            right = self.factor()
            res = ExprNode(token_tmp, lnode=left, rnode=right)
            print("-----Exit Factor-----")
            return res
        else:
            res = self.component()
            print("-----Exit Factor-----")
            return res

    def component(self):
        print("-----Enter Component-----")
        left = self.atom()
        self.fetch_token()
        while self.token.type == Token_Type.POWER.name:
            token_tmp = self.token.type
            self.match_token(token_tmp)
            self.fetch_token()
            right = self.component()
            left = ExprNode(token_tmp, lnode=left, rnode=right)
        print("-----Exit Component-----")
        return left

    def atom(self):
        print("-----Enter Atom-----")
        if self.token.type == Token_Type.CONST_ID.name:
            print("leaf: " + str(self.token.value))
            print("-----Exit Atom-----")
            return ExprNode(self.token.type, self.token.value)  # leaf
        elif self.token.type == Token_Type.T.name:
            print("leaf: " + self.token.type)
            print("-----Exit Atom-----")
            return ExprNode(self.token.type, self.token.value)  # leaf
        elif self.token.type == Token_Type.FUNC.name:
            token_tmp = self.token.type
            func_tmp = self.token.func
            self.fetch_token()
            self.match_token(Token_Type.L_BRACKET.name)
            self.fetch_token()
            left = self.expression()
            self.match_token(Token_Type.R_BRACKET.name)
            print("-----Exit Atom-----")
            return ExprNode(token_tmp, lnode=left, func=func_tmp)
        elif self.token.type == Token_Type.L_BRACKET:
            self.match_token(Token_Type.L_BRACKET.name)
            self.fetch_token()
            left = self.expression()
            self.match_token(Token_Type.R_BRACKET.name)
            print("-----Exit Atom-----")
            return left


if __name__ == '__main__':
    p = Parser("test.txt")
    p.start()
    plt.xlim(0)
    plt.ylim(0)
    plt.show()
