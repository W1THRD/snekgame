import easygui as ez
import os, sys
p = ez.indexbox("Welcome to snek!", "Snek v1.0", ["1P Mode", "2P Mode", "Custom Levels", "About", "Exit"])
if p == 0:
    exec(open('1p.pyw').read())
elif p == 1:
    exec(open('2p.pyw').read())
elif p == 2:
    ez.msgbox("This is still a work in progress. But, you can try out this randomly-generated level!")
    exec(open('clevel.pyw').read())
elif p == 3:
    ez.msgbox("Snek is a small snake game made by W1THRD, designed to be a unique snake game. \nMade with Python, PyGame Zero, and Easygui.", "Snek: About")
    os.execv(sys.executable, ['python'] + sys.argv)
