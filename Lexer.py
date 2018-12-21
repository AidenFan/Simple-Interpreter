from utils import Token
from utils import Token_Type
from utils import TokenTab


class Lexer:
    def __init__(self, filename):
        self.words = ''
        self.state = 0
        # token set
        self.tokens = []
        self.cnt = 0
        self.file = open(filename, 'r')
        if self.file is None:
            print("Open Source File Error!")
        self.comment = False

    def start(self):
        # open the file
        content = self.file.read()
        self.file.close()
        content += '\n'
        # to upper
        content = str.upper(content)
        # init
        state = 0
        for i in range(len(content)):
            if content[i] == '\n':
                self.comment = False
            if not self.comment:
                state = self.next_state(state, content[i])
        self.tokens.append(Token(Token_Type.NONTOKEN.name, "", 0.0, None))

    def next_state(self, state, ch):
        if ch == ' ' or ch == '\t' or ch == '\n':
            self.search(state)
            return 0

        if state == 0:
            self.words += ch
            if ch.isalpha():
                return 1
            elif ch.isdigit():
                return 2
            elif ch == '*':
                return 4
            elif ch == '/':
                return 6
            elif ch == '-':
                return 7
            elif ch == '+' or ch == ',' or ch == ';' or ch == '(' or ch == ')':
                return 5
        elif state == 1:
            if ch.isdigit() or ch.isalpha():
                self.words += ch
                return 1
            else:
                self.search(state)
                return self.next_state(0, ch)
        elif state == 2:
            if ch.isdigit():
                self.words += ch
                return 2
            elif ch == '.':
                self.words += ch
                return 3
            else:
                self.search(state)
                return self.next_state(0, ch)
        elif state == 3:
            if ch.isdigit():
                self.words += ch
                return 3
            else:
                self.search(state)
                return self.next_state(0, ch)
        elif state == 4:
            if ch == '*':
                self.words += '*'
                return 5
            else:
                self.search(state)
                return self.next_state(0, ch)
        elif state == 5:
            self.search(state)
            return self.next_state(0, ch)
        elif state == 6:
            if ch == '/':
                self.words += ch
                return 5
            else:
                self.search(state)
                return self.next_state(0, ch)
        elif state == 7:
            if ch == '-':
                self.words += ch
                return 5
            else:
                self.search(state)
                return self.next_state(0, ch)

    def search(self, state):
        # print(state)
        # print(self.words)
        if state == 1:
            found = False
            for item in TokenTab:
                if self.words == item.lexeme:
                    self.tokens.append(item)
                    found = True
                    break
            if not found:
                print("Error with " + self.words + ": ID not found!")
        elif state == 2 or state == 3:
            self.tokens.append(Token(Token_Type.CONST_ID.name, "CONST_ID", self.words, None))   # 字符串转数字
        elif state == 4:
            self.tokens.append(Token(Token_Type.MUL.name, self.words, 0.0, None))
        elif state == 5:
            if self.words == "**":
                self.tokens.append(Token(Token_Type.POWER.name, self.words, 0.0, None))
            elif self.words == "//":
                self.tokens.append(Token(Token_Type.COMMENT.name, self.words, 0.0, None))
                self.comment = True
            elif self.words == "--":
                self.tokens.append(Token(Token_Type.COMMENT.name, self.words, 0.0, None))
                self.comment = True
            elif self.words == "+":
                self.tokens.append(Token(Token_Type.PLUS.name, self.words, 0.0, None))
            elif self.words == ",":
                self.tokens.append(Token(Token_Type.COMMA.name, self.words, 0.0, None))
            elif self.words == ";":
                self.tokens.append(Token(Token_Type.SEMICO.name, self.words, 0.0, None))
            elif self.words == "(":
                self.tokens.append(Token(Token_Type.L_BRACKET.name, self.words, 0.0, None))
            elif self.words == ")":
                self.tokens.append(Token(Token_Type.R_BRACKET.name, self.words, 0.0, None))
        elif state == 6:
            self.tokens.append(Token(Token_Type.DIV.name, self.words, 0.0, None))
        elif state == 7:
            self.tokens.append(Token(Token_Type.MINUS.name, self.words, 0.0, None))
        self.words = ""

    def gettoken(self):
        res = self.tokens[self.cnt]
        self.cnt = self.cnt + 1
        return res


if __name__ == '__main__':
    # 初始化词法分析器
    a = Lexer("test.txt")
    # 对文件进行词法分析
    a.start()

    token = Token(Token_Type.ERRTOKEN.name, "", 0.0, None)
    print("记号类别   字符串   常数值   函数指针")
    print("------------------------------------")
    # 每次返回一个token
    while True:
        token = a.gettoken()
        if token.type != Token_Type.NONTOKEN.name:
            token.show()
        else:
            break
    print("------------------------------------")
