import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from time import sleep
from sys import exit
import interpretter as intp


A = "A"
B = "B"


# Add line numbers & paddings
def text2view(text):
    ret = ""
    lines = text.splitlines()
    for n, line in enumerate(lines):
        sp = len(str(len(lines)))-len(str(n))
        ret += f" {n}{' '*sp}⎸{line}\n"
    return ret

'''
text ="""
0.01 __tick
: ;: -> drop ;
: ::
    -> dup <- :@
    dup ^ -: ";" =
    ? 2 skipX 6 skipX
        1 + -> drop <- @
        dup ^  -: ;: = 
        ? 2 skipX 10 skipX
            1 + dup -> swap <- dup <- <- @
            1 + -> dup <- <- @
;
: while
    -> -> swap -> swap <- swap <- <-
    -> dup <- <- ` ? 2 skipX 13 skipX
    -> -> swap <- <- -> dup <- <- ` while 4 skipX
    -> -> drop drop
;
#100 :: dup 0 < ;: dup \\r "      " \\r . . . . 1 swap - ; while
: c dup 0 < ;
"""[1:]
'''

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

def command(arg=None, **kwargs):
    def decorator(f, name, comment=None):
        if name is None:
            name = str(f).split(" ")[1]
        #print(name, f)
        global dictionary
        if comment:
            dictionary.append((name, f, comment))
        else:
            dictionary.append((name, f))
        return f
    comment = None
    if "comment" in kwargs:
        comment = kwargs["comment"]
    if callable(arg):
        return decorator(arg, None, comment)
    return lambda f: decorator(f, arg, comment)

@command(comment="Do nothing")
def nop():
    pass

@command("+", comment="Sum two values on top of StackB")
def sum_op():
    putB(getB() + getB())

@command("-", comment="Sub two values on top of StackB")
def sub_op():
    putB(getB() - getB())

@command("*", comment="Mul two values on top of StackB")
def mul_op():
    putB(getB() * getB())

@command("/", comment="Div two values on top of StackB")
def mul_op():
    putB(getB() / getB())

@command("=", comment="Compare to values on top of StackB")
def mul_op():
    putB(getB() == getB())

@command(">", comment="Compare to values on top of StackB")
def mul_op():
    putB(getB() > getB())

@command("<", comment="Compare to values on top of StackB")
def mul_op():
    putB(getB() < getB())

@command("[", comment="Duplicate (copy) value on top of StackB")
def dup_op():
    v = getB()
    putB(v)
    putB(v)

@command("[]", comment="Swap value on top of StackB")
def swap_op():
    a, b = getB(), getB()
    putB(a)
    putB(b)

@command("]", comment="Drop one walue from top of StackB")
def drop_op():
    getB()

@command("<-", comment="Move value from top of StackB to top of StackA")
def b2a_op():
    global stackA
    stackA.append(getB())

@command("->", comment="Move value from top of StackA to top of StackB")
def a2b_op():
    global stackB
    stackB.append(getA())

@command("&", comment="Resolve word adress")
def ref_op():
    global stackB
    name = getB()
    for d in reversed(dictionary):
        if d[0] == name and not callable(d[1]):
            stackA.append(d[1])

@command("`", comment="call word with adress on top of StackA")
def deref_op():
    global stackA
    ref = getA()
    stackA.append(pointer+1)
    return ref

@command(":@", comment="Label, put itself position on StackA")
def label_op():
    global stackA
    stackA.append(pointer+1)

@command("@", comment="Goto label from top of StackA")
def label_goto_op():
    return getA()

@command(".", comment="Print value on top of StackB")
def print_op():
    print(getB(), end="", flush=True)

@command(",", comment="Show value on top of StackB")
def show_op():
    print(getB(remove=False), end="", flush=True)

@command("ret", comment="return")
def return_op():
    return getA()

@command(";", comment="return; also mark function end")
def return_op():
    return getA()

@command(":", comment="Define new word (name on next postion; allow rewrite word)")
def def_op():
    global dictionary
    dictionary.append((program[pointer+1][0], pointer+2))
    cur = pointer+1
    while program[cur][0] != ";" or program[cur][4]:
        cur += 1
    return cur+1

@command("!:", comment="Undefine word")
def undef_op():
    global dictionary
    name = program[pointer+1][0]
    for n, w in enumerate(reversed(dictionary)):
        if w[0] == name:
            n = len(dictionary)-n-1
            dictionary = dictionary[:n]+dictionary[n+1:]
            break
    return pointer+2

@command(":i", comment="Ignore definition of next word")
def igdef_op():
    global stackB
    stackB.append(word2value(program[pointer+1]))
    return pointer+2

@command("^", comment="Reflexy")
def get_word_by_position_op():
    global stackB
    word = program[getB()][0]
    stackB.append(word)

#@command("~", comment="Self modificate")
#def selfmod_op():
#    global program
#    pos = getB()
#    repl = getB()
#    program[pos][0] = repl

@command("go", comment="Go to word defitnition without stackA mess")
def goto_op():
    global stackB
    name = program[pointer+1][0]
    #print(name)
    for d in reversed(dictionary):
        #print(d[0])
        if d[0] == name and not callable(d[1]):
            #print(d)
            return d[1]
    return pointer+2

@command("skip", comment="Skip next command")
def skip_op():
    return pointer+2

@command("skipX", comment="Skip X next commands")
def skipx_op():
    return pointer+1+getB()

@command("?", comment="Ternar statement. In '? 0 1 2' 0 will be executed if value on top of stackB if truly, else 2")
def if_op():
    if not getB():
        return pointer+3

@command("!?", comment="Ternar statement. In '? 0 1 2' 2 will be executed if value on top of stackB if truly, else 0")
def nif_op():
    if getB():
        return pointer+3

@command("\\n", comment="Line break")
def linebreak_op():
    global stackB
    stackB.append("\n")

@command("\\r", comment="Cursor return")
def retcursor_op():
    global stackB
    stackB.append("\r")

@command("__tick", comment="Set tick delay")
def tick_op():
    global tick_delay
    tick_delay = getB()

@command("__stop", comment="Stop execution")
def stop_op():
    global runing
    runing = False

@command("__stop", comment="Stop execution")
def stop_op():
    global runing
    runing = False

def step():
    global stackA
    global stackB
    global program
    global pointer
    global dictionary
    global step_number
    step_number += 1
    if pointer >= len(program):
        print("<<ended>>")
        return False
    word = program[pointer][0]
    #print(pointer, word)
    unknown = True
    for d in reversed(dictionary):
        if d[0] == word:
            unknown = False
            if callable(d[1]):
                result = d[1]()
                if result != None:
                    pointer = result
                else:
                    pointer += 1
                break
            else:
                stackA.append(pointer+1)
                pointer = d[1]
                return True
    if unknown:
        value = word2value(program[pointer])
        stackB.append(value)
        pointer += 1
    return True


print(text2view(text))


while step() and runing:
    sleep(tick_delay)


print("\nStackA:")
for e in stackA:
    # Trying to guess what stack value means
    try:
        if program[e-2][0] == ":":
            print(e, "word:", program[e-1][0])
            continue
    except:
        pass
    try:
        if program[e-1][0] in ["::", ";:"]:
            code = ""
            i = e
            try:
                while program[i][0] not in [";", ";:"]:
                    code+=program[i][0]+" "
                    i += 1
            except:
                pass
            print(e, "lambda:", code)
            continue
    except:
        pass
    try:
        name = program[e-1][0]
        find = False
        for d in reversed(dictionary):
            if d[0] == name:
                find = True
                continue
        if find:
            print(e, "ret2:", name, "on line", program[e-1][1])
            continue
    except:
        pass
    print(e)

print("\nStackB")
for e in stackB:
    print(e)

#print("\nProgram:")
#for n, e in enumerate(program):
#    print(f"{n} {e[0]}")

#print("\nDict")
#for e in dictionary:
#    if len(e) > 2:
#        print(f"({e[0]} {e[2]})")
#    else:
#        print(f"({e[0]} {e[1]})")


"""
TODO
- GUI
- Import forth code
- Import python code
- Random numbers generation
"""
