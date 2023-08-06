# TacoTUI

Terminal text coloring and simple user interface widgets

![TacoTUI form widget demo](tacotui/demo/form.png)

This Python module is meant to be a simple, light-weight, cross-platform
method for manipulating the terminal and generating basic text-based user interfaces. 
If you just need easy control of terminal coloring, or a few simple widgets that are one step above using `input()`, this module is for you.

    - Cross platform. Works directly in the Windows 10 terminal, most Linux terminals, and OSX.
    - Provides easy access functions for setting terminal colors and position.
    - Widgets that provide a "linear" user experience. User works with one widget at a time.
    - Easy and fast to program. Instead of writing objects/classes, everything is defined using function calls.
    - Different color schemes for widgets.
    - Pure python, no dependencies.

While modules like curses, and its wrappers such as urwid or npyscreen, are
much more powerful and flexible, this has a low learning curve and works cross-platform with no additional setup.
It is meant for beginning Python programmers (aka engineers who use Python but don't have time to become computer scientists)
who want a quick method for generating a usable linear user interface.

This module works with Python 3.6 or higher on terminals that support ANSI escape codes.
This includes Mac terminal, Windows 10 terminal, and most Linux terminals. 


## Setting terminal colors

Use the `color` module to generate ANSI terminal commands for setting text and background color.
The attributes of `color` can be printed directly or used in Python f-strings to color individual words:

    from tacotui import color as c
    print(f'This sentence has {c.GREEN}green, {c.RED}red, {c.RESET}and {c.BLUE}blue {c.RESET} words.')
    print(f'TacoTUI can color {c.BGBLUE}background{c.RESET} and {c.BRIGHTYELLOW_BGBLUE}background and foreground{c.RESET}colors.')

Foreground colors: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, BRIGHTBLACK, BRIGHTRED, BRIGHTGREEN, BRIGHTYELLOW,
BRIGHTBLUE, BRIGHTMAGENTA, BRIGHTCYAN, BRIGHTWHITE.
Background colors can use the same names prepended with BG, for example BGRED for a red background.
Attributes UNDERLINE and BOLD can also be used. Foreground, background, and attribute can be combined with underscores
into a single attribute name, such as `c.RED_BGBLUE_UNDERLINE`.

Specific RGB colors can be specified by calling the `rgb()` or `rgbbg()` functions with the r, g, b values as integers between 0 and 255.


## Screen positioning

Use the `screen` module to perform screen operations such as clear or setting the cursor position.
The top-left corner of the screen is (1, 1).

    tacotui.clear()
    tacotui.hide_cursor(true)
    tacotui.setxy(10, 8)
    print('This text starts at x=10, y=8')


## Widgets

Use the `widgets` module to show predefined basic widgets, such as message boxes, list selections, and
file selection boxes. Note this is a linear user experience, only one widget can be used at a time. For
each widget, call `help(name)`  (for example `help(tacotui.widgets.message)`) for instructions on how to use it.

Widgets include:

    - `box` - Just draws a rectangle
    - `message` - Show a message, with or without buttons
    - `get_int` - Get integer value
    - `get_float` - Get floating point value
    - `get_char` - Get a single character
    - `get_date` - Get a datetime. Requires dateutil module
    - `list_select` - Choose an item from a list
    - `multi_select` - Choose multiple items from a list
    - `file_select` -  Choose an existing or new file, or a folder
    - `line_edit` -  Enter a string, with possible default value
    - `form` - Multiple entries in a form layout
    - `slider` - Slider widget for selecting from a range of values
    - `progress` - Progress bar widget

## Plots

You can even make ugly text-based plots like this one.

![text plot](tacotui/demo/plot.png)

Scatter plots and bar plots are drawn with these functions:

    - `textplot` - Draw scatter plot
    - `barplot` - Draw a horizontal bar plot


## Demo

Run the demos to see tacotui in action.

    import tacotui
    tacotui.demo.color()
    tacotui.demo.widgets()
    tacotui.demo.plot()

There's also an example number guessing game.

    tacotui.demo.game()

and a sample application of a form for ordering tacos.

    tacotui.demo.form()
