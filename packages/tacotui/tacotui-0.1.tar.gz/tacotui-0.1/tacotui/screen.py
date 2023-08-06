''' Screen manipulation functions '''

import shutil

from .color import color, theme

scrwidth, scrheight = shutil.get_terminal_size()


class _Pos(object):
    ''' Class for generating cursor positioning ANSI command strings.
        Access by attribute, such as pos.XY10_5, pos.X10, pos.Y5.

        Also has attributes pos.PUSH and pos.POP to save and restore
        the cursor position.

        All results returned as printable ANSI strings.
    '''
    def __getattr__(self, name):
        if name.lower().startswith('xy'):
            x, y = name[2:].split('_')
            return f'\x1b[{y};{x}H'
        elif name.lower().startswith('y'):
            y = name[1:]
            return f'\x1b[{y}d'
        elif name.lower().startswith('x'):
            x = name[1:]
            return f'\x1b[{x}G'
        elif name.lower().startswith('push'):
            return '\x1b[s'
        elif name.lower().startswith('pop'):
            return '\x1b[u'
        else:
            raise AttributeError


pos = _Pos()


def sprint(s):
    ''' Print without newline and immediately update the display 

        Parameters
        ----------
        s: string
            The string to print
    '''
    print(s, end='', flush=True)


def clear():
    ''' Clear the screen and fill with the theme background color '''
    sprint(f'{theme.NORM}{color.CLS}')


def clearline():
    ''' Clear the current line and fill with the current background color '''
    sprint(color.CLRLINE)


def setxy(x, y):
    ''' Set the cursor position, (1, 1) is top left corner

        Paramters
        ---------
        x: int
            Horizontal cursor position
        y: int
            Vertical cursor position
    '''
    sprint(getattr(pos, f'XY{x}_{y}'))


def setcolor(c):
    ''' Set the current color

        Parameters
        ----------
        c: string
            Color name from the `tacotui.color` module
    '''
    sprint(getattr(color, c))


def resetcolor():
    ''' Reset colors to terminal default '''
    sprint(color.RESET)


def hide_cursor(hide=True):
    ''' Show or hide the cursor '''
    if hide:
        sprint('\x1b[?25l')
    else:
        sprint('\x1b[?25h')


def write(s, c=None):
    ''' Write a string in the given color

        Parameters
        ----------
        s: string
            The string to print
        c: string
            Color name from the `tacotui.color` module
    '''
    if c is not None:
        sprint('{}{}{}'.format(getattr(color, c), s, c.RESET))
    else:
        sprint(s)


def centertext(s, width=scrwidth):
    ''' Center the text, padded with spaces

        Parameters
        ----------
        s: string
            The text to center
        width:
            Total width of final padded string

        Returns
        -------
        s: string
            Centered string padded with spaces

        Note
        ----
        This currently won't work if `s` contains escape
        codes since Python's `format` doesn't know how to
        exclude those from the string length.
    '''
    return format(s, f'^{width}s')
