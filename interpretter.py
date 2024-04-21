

# Parser; text -> [[command, line, start_char, end_char, is quotes], ...]
def parse(text):
    p = []
    for l, line in enumerate(text.splitlines()):
        lex = ""
        quotes = None
        start = 0
        n = 0
        for n, c in enumerate(line):
            if c in (quotes or " \t"):
                if lex != "":
                    p.append([lex, l, start, n, bool(quotes)])
                lex = ""
                quotes = None
                continue
            if lex == "":
                if c == "#":
                    break # Comment; Skip line
                start = n
                if c in ['"']:
                    quotes = c
                    continue
            lex += c
        if lex != "":
            p.append([lex, l, start, n, bool(quotes)])
    return p

def word2value(word):
    w = word[0]
    if not word[4]:
        try:
            w = int(w)
        except:
            try:
                w = float(w)
            except:
                pass
    return w

class Forth:
    def __init__(self, program=None, stackA=None, stackB=None, dictionary=None, pointer=0, step_number=0):
        self.__running = True
        self.pointer = pointer
        self.step_number = step_number
        self.program = [] if program is None else program
        self.stacks = {
            "A": [] if stackA is None else stackA,
            "B": [] if stackB is None else stackB,
        }
        self.dictionary = [] if dictionary is None else dictionary

    def pop(self, name, remove=True):
        stack = self.stacks[name]
        value = stack[-1]
        if remove:
            self.stacks[name]=stack[:-1]
        return value

    def push(self, name, value):
        self.stacks[name].append(value)

    def get(self, pointer):
        return word2value(self.program[pointer])

    def word(self, name, comment="Pre-definded"):
        def decorator(func):
            self.dictionary.append((name, func, comment))
        return decorator

    def stop(self):
        self.__running = False

    def step(self):
        if self.pointer >= len(self.program) or not self.__running:
            self.__running = False
            return False
        self.step_number += 1
        word = self.program[self.pointer]
        unknown = True
        for d in reversed(self.dictionary):
            if d[0] != word[0]:
                continue
            unknown = False
            if callable(d[1]):
                result = d[1](self)
                self.pointer = result if result is not None else self.pointer + 1
            else:
                self.push("A", self.pointer+1)
                self.pointer = d[1]
                return True
        if unknown:
            value = word2value(word)
            self.push("B", value)
            self.pointer += 1
        return True

    def show(self) -> str:
        ret_list = [["StackA (calls) ↓", "StackB (data) ↓"]]
        max_a = len(ret_list[0][0])
        max_b = len(ret_list[0][1])
        max_len = max(len(self.stacks["A"]), len(self.stacks["B"]))
        for i in range(max_len):
            row = []
            if i < len(self.stacks["A"]):
                row.append(str(self.stacks["A"][i]))
            else:
                row.append("")
            if i < len(self.stacks["B"]):
                typ = str(type(self.stacks["B"][i]))[8:-2]
                typ += " "*(6-len(typ))+": "
                row.append(typ+str(self.stacks["B"][i]))
            else:
                row.append("")
            max_a = max(max_a, len(row[0]))
            max_b = max(max_b, len(row[1]))
            ret_list.append(row)
        ret = ""
        for row in ret_list:
            if row[0] == "":
                ret += " "*max_a
            else:
                txt = row[0]
                txt += " "*(max_a-len(txt))
                ret += txt
            ret += " | "+row[1]
            ret += "\n"
        ret += "-"*(max_a+max_b+3)+"\n"
        ret_list = []
        max_name = 0
        for d in self.dictionary:
            row = [d[0]]
            max_name = max(max_name,len(d[0]))
            if len(d) > 2 and d[2] != "":
                row.append(d[2])
            else:
                row.append(d[1])
            ret_list.append(row)
        ret += "Dict\n"
        for row in ret_list:
            ret += row[0]+" "*(max_name-len(row[0])+1)+str(row[1])
            ret += "\n"
        return ret

















