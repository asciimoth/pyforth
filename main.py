import interpretter as intp
from time import sleep

A = "A"
B = "B"

code = """
    # Returns pointer to function that puts 1 on sB
    { { 1 } -> -> [] <- <- } 1f ;
    # Returns pointer to function that puts 0 on sB
    { { 0 } -> -> [] <- <- } 0f ;
    # Breaks @ loop
    { -> -> -> -> ] ] ] ] } |@ ;
    {
        -> -> [] -> [] <- [] <-  <-
        -> [ <- <- ;:
        -> -> [] <- [ <- <-
        { -> -> -> ] ] ] } ? @
    } @ ;
    # 10 { [ 0 < } { [ out 1 [] - } @
"""

forth = intp.Forth()
forth.delay = 0.01

@forth.word("_", "Do nothing")
def nop_op(f):
    pass

@forth.word("+", "Sum")
def sub_op(f):
    f.push(B, f.pop(B) + f.pop(B))

@forth.word("-", "Sub")
def sub_op(f):
    f.push(B, f.pop(B) - f.pop(B))

@forth.word("*", "Mul")
def mul_op(f):
    f.push(B, f.pop(B) * f.pop(B))

@forth.word("/", "Div")
def div_op(f):
    f.push(B, f.pop(B) / f.pop(B))

@forth.word("=", "Equal")
def eq_op(f):
    f.push(B, f.pop(B) == f.pop(B))

@forth.word(">", "More")
def more_op(f):
    f.push(B, f.pop(B) > f.pop(B))

@forth.word("<", "Less")
def less_op(f):
    f.push(B, f.pop(B) < f.pop(B))

@forth.word("[", comment="Duplicate (copy) value on sB")
def dup_op(f):
    v = f.pop(B)
    f.push(B, v)
    f.push(B, v)

@forth.word("]", comment="Drop value on sB")
def drop_op(f):
    v = f.pop(B)

@forth.word("[]", comment="Swap two values on sB")
def swap_op(f):
    a, b = f.pop(B), f.pop(B)
    f.push(B, a)
    f.push(B, b)

@forth.word("->", comment="Move from sA to sB")
def a2b_op(f):
    f.push(B, f.pop(A))

@forth.word("<-", comment="Move from sB to sA")
def b2a_op(f):
    f.push(A, f.pop(B))

@forth.word("}", "Return; close block")
def block_close_op(f):
    if f.program[f.pointer][4]:
        f.push(B, "}")
        return
    return f.pop(A)

@forth.word("{", "Define block")
def block_open_op(f):
    if f.program[f.pointer][4]:
        f.push(B, "{")
        return
    f.push(A, f.pointer+1)
    blocks = 0
    pointer = f.pointer
    while True:
        pointer += 1
        if f.program[pointer][4]:
            continue
        if f.program[pointer][0] == "{":
            blocks += 1
        if f.program[pointer][0] == "}":
            blocks -= 1
            if blocks < 0:
                return pointer+1

@forth.word(";", "Define word (name from sB, pointer from sA)")
def block_close_op(f):
    name = f.pop(B)
    pointer = f.pop(A)
    f.dictionary.append((name, pointer))

@forth.word(":", "Add position to sA")
def label_op(f):
    f.push(A, f.pointer+1)

@forth.word(":;", "Goto sA")
def goto_op(f):
    return f.pop(A, remove=False)

@forth.word(";:", "Call sA")
def call_op(f):
    pointer = f.pop(A)
    f.push(A, f.pointer+1)
    return pointer

@forth.word(";;", "Ignore definition of next word")
def ignore_op(f):
    f.push(B, f.get(f.pointer+1))
    return f.pointer+2

@forth.word("?", "Conditional")
def cond_op(f):
    fal = f.pop(A)
    tru = f.pop(A)
    f.push(A, f.pointer+1)
    if f.pop(B):
        return tru
    return fal

@forth.word("out", "Print from sB")
def out_op(f):
    print(f.pop(B))

@forth.word("__stop", "Stop program")
def stop_op(f):
    print("stop")
    f.stop()

@forth.word("__delay", "Set step delay from sB")
def delay_op(f):
    f.delay = f.pop(B)


def main():
    forth.program = intp.parse(code)
    while forth.step():
        sleep(forth.delay)
    print(f"\n<<ended>> with {forth.step_number} steps")
    print(forth.show())


if __name__ == "__main__":
    main()

