import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# My desctop color pallette
base00 = "#111111"
base01 = "#1b1b1b"
base02 = "#262626"
base03 = "#777777"
base04 = "#919191"
base05 = "#ababab"
base06 = "#c6c6c6"
base07 = "#e2e2e2"
base08 = "#f04339"
base09 = "#df5923"
base0A = "#bb8801"
base0B = "#7f8b00"
base0C = "#00948b"
base0D = "#008dd1"
base0E = "#6a7fd2"
base0F = "#e3488e"

txt = """
   1  | a
   2  ‖ b
   3  ⁞ c
   4  ⎸ d
   5  | e
   6  | f 
   7  | g
   8  | h
   9  | i
   10 | j
"""[1:]+("".join(["   "+str(i)+(" "*(3-len(str(i))))+"| aa\n" for i in range(11, 120)]))

HIGHLIGHTED = None


def highligt(line, widget, highliter=">>", padding=" "):
    global HIGHLIGHTED
    if HIGHLIGHTED != None:
        widget.delete(f"{HIGHLIGHTED}.0", f"{HIGHLIGHTED}.{len(highliter)}")
        widget.insert(f"{HIGHLIGHTED}.0", padding*len(highliter))
        widget.tag_delete("highlighted")
    HIGHLIGHTED = line
    widget.delete(f"{HIGHLIGHTED}.0", f"{HIGHLIGHTED}.{len(highliter)}")
    widget.insert(f"{HIGHLIGHTED}.0", highliter)
    widget.tag_add("highlighted", f"{HIGHLIGHTED}.0", f"{HIGHLIGHTED}.8")
    widget.tag_config("highlighted", background=base07, foreground=base00)
    widget.mark_set("highlighted", f"{HIGHLIGHTED}.0")
    widget.see("highlighted")
    


window = tk.Tk()

text_box = ScrolledText(master=window, font=("Courier", 10), bg=base00, fg=base07)
text_box.pack(expand=1, fill=tk.BOTH)
text_box.insert(tk.END, txt)

highligt(1, text_box)

def tick():
    window.after(1000,tick)
    h = HIGHLIGHTED+1
    highligt(h, text_box)

window.after(1000,tick)

window.mainloop()
