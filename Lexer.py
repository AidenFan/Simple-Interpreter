from utils import Token
from utils import Token_Type
from utils import TokenTab


class Lexer:
    def __init__(self):
        self.words = ''
        self.token = Token(Token_Type.ERRTOKEN.name, "", 0.0, None)

    def lexer(self, fpath):
        file = open(fpath, 'r')
        content = file.read()
        content += '\n'
        content = str.upper(content)
        state = 0
        for i in range(len(content)):
            state = self.next_state(state, content[i])

    def next_state(self, state, ch):
        if ch == ' ' or ch == '\t' or ch == '\n':
            self.search(state, self.words).show()
            self.words = ''
            return 0
        self.words += ch
        # print("after join: %s" % self.words)
        if state == 0:
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
                return 1
        elif state == 2:
            if ch.isdigit():
                return 2
            elif ch == '.':
                return 3
        elif state == 6:
            if ch == '/':
                return 5
        elif state == 7:
            if ch == '-':
                return 5

    def search(self, state, words):
        if state == 1:
            for item in TokenTab:
                if words == item.lexeme:
                    return item
            print("ID not found!")
        elif state == 2 or state == 3:
            return Token(Token_Type.CONST_ID.name, "CONST_ID", words, None)   # 字符串转数字
        elif state == 4:
            return Token(Token_Type.MUL.name, words, 0.0, None)
        elif state == 5:
            return Token(Token_Type.POWER.name, words, 0.0, None)
        elif state == 6:
            return Token(Token_Type.DIV.name, words, 0.0, None)
        elif state == 7:
            return Token(Token_Type.MINUS.name, words, 0.0, None)


if __name__ == '__main__':
    a = Lexer()
    a.lexer('test.txt')
    # while True:
    #     sentence = input()
    #     if sentence == 'q':
    #         break
    #     sentence = str.upper(sentence)
    #     for i in range(len(sentence)):
    #         print(sentence[i])
    # token = Token(Token_Type.ERRTOKEN.name, "", 0.0, None)
    # print("记号类别     字符串     常数值     函数指针")
    # print("----------------------------------------")
    # while True:
    #     token = GetToken()
    #     if(token.type != Token_Type.NONTOKEN.name):
    #         token.show()
    #     else:
    #         break
    # print("----------------------------------------")
