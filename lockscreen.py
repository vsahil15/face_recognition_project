from tkinter import *

root = Tk()

root.attributes("-fullscreen", True)

def exit_app(event=None):
    root.destroy()

# Emergency exit key
root.bind("<Control-Shift-Q>", exit_app)

Label(
    root,
    text="SYSTEM LOCKED",
    font=("Arial", 40)
).pack(pady=100)

Label(
    root,
    text="Press Ctrl+Shift+Q to exit (testing mode)",
    font=("Arial", 15)
).pack()

root.mainloop()