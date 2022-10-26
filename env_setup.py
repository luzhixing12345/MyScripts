
import platform
import select
import datetime
import json
import os
# --------------------------------------------------------
# basic configuration
# --------------------------------------------------------
VERSION = "0.0.1"                                          # MyScript version
UPDATE_TIME = datetime.datetime.now().strftime('%Y-%m-%d') # latest update time
SCRIPT_NAME = 'Myscript.py'                                # final py name generated by build.py
SCRIPTS_POSITION = './scripts'                             # json scripts content files root folder position

CMD_PROMPT = '[MyScript]'                                  # show in command line prompt
CMD_PROMPT_COLOR = 'cyan'                                  # prompt color
CURSOR_BLINKING_SYMBOL = '|'                               # cursor symbol
CURSOR_BLINKING_TIMER = 10                                 # count timer, show CURSOR_BLINKING_SYMBOL when settimeout
CURSOR_BLINKING_SLEEPTIME = 0.1                            # sleep time

# keyboard map
ESC = chr(27)
SPACE = chr(32)
BACKSPACE = chr(127)
TAB = chr(9)
TAB_SPACE = 4

# --------------------------------------------------------
# Keyboard input handler
# https://docs.python.org/zh-cn/3.7/library/termios.html
# --------------------------------------------------------

class _GetchWindows:

    def __call__(self):
        return msvcrt.getch()
    
    def handleinput(self,ch):
        if ch == ESC:
            exit(0)
        elif ch == SPACE:
            return ' '
        elif ch == TAB:
            return ' ' * TAB_SPACE
        else:
            return ch

class _GetchUnix:
    
    def __init__(self) -> None:
        
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(self.fd)
    
    def getchar(self):
        
        # try:
        
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            ch = sys.stdin.read(1)
            return self.handleinput(ch)
        else:
            return 'WAIT'
    
    def handleinput(self,ch):
        if ch == ESC:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            exit(0)
        elif ch == SPACE:
            return ' '
        elif ch == TAB:
            return ' ' * TAB_SPACE
        else:
            return ch

if platform.system() == 'Windows':
    import msvcrt
    keyboard = _GetchWindows()
elif platform.system() == 'Linux':
    import sys, tty, termios
    keyboard = _GetchUnix()
else:
    raise "unsupported OS"
# --------------------------------------------------------
# OS & package manager information
# --------------------------------------------------------

