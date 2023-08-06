''' TacoTUI. Terminal text coloring and simple user interface widgets

    color: generate printable strings to change the terminal color:

        # After the next line, any printed text will have blue foreground
        print(tacotui.color.BLUE)

        # After the next line, any printed text will have red background
        print(tacotui.color.BGRED)

        # Attributes can be combined
        print(tacotui.color.YELLOW_BGBLACK_BOLD)

    pos: generate printable strings to control terminal cursor position:

        print(tacotui.pos.XY5_10)  # Move cursor to x=5, y=10

    functions:
        sprint - print without a newline and immediately update
        clear -  clear the screen
        clearline - clear from cursor to end of line
        setxy - set the cursor position
        setcolor - set the current color
        resetcolor - reset all colors to terminal default
        hide_cursor - hide or show the terminal cursor
        write - write a string in the given color
        centertext - return text centered within a given width

    widgets: functions in this module set up and display simple UI widgets:
        box - Just draws a rectangle
        message - Show a message, with or without buttons
        get_int - Get integer value
        get_float - Get floating point value
        get_char - Get a single character
        get_date - Get a datetime. Requires dateutil module
        list_select - Choose an item from a list
        multi_select - Choose multiple items from a list
        file_select -  Choose an existing or new file, or a folder
        line_edit -  Enter a string, with possible default value
        form - Multiple entries in a form layout
        slider - Slider widget for selecting from a range of values
        progress - Progress bar widget
        textplot - Draw scatter plot
        barplot - Draw a horizontal bar plot
'''
import atexit

try:
    from ctypes import windll
except ImportError:
    pass  # Not on windows, ANSI codes should work automatically
else:
    # On windows10, need to enable ANSI codes for some reason
    kernel = windll.kernel32
    kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)

from .color import color, theme
from .screen import *
from . import widgets
from . import demo
from .version import __version__

# Install exit handler to restore the terminal when the
# program exits
def _exit_handler():
    print(color.RESET)
    hide_cursor(False)


atexit.register(_exit_handler)
