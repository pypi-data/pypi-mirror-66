''' Module for defining terminal colors. All color attributes are returned
    as strings, which when printed, set the terminal properties.
'''


class _Color(object):
    ''' Class for generating ANSI color code strings.
        Access by attributes, such as color.RED, color.BGBLUE,
        or color.YELLOW_BGBLUE. All results returned as
        printable ANSI strings.

        Foreground color names can be prepended with BG:
        color.BGBLUE for a blue background

        Bold and underline:
        color.RED_UNDERLINE, color.BLUE_BOLD

        Combine multiple parameters with underscores:
        color.RED_BGYELLOW_BOLD
    '''
    # Named color codes
    ctable = {'black': '30',
              'brightred': '91',
              'brightgreen': '92',
              'brightyellow': '93',
              'brightblue': '94',
              'brightmagenta': '95',
              'brightcyan': '96',
              'brightwhite': '97',
              'brightblack': '90',
              'red': '31',
              'green': '32',
              'yellow': '33',
              'blue': '34',
              'magenta': '35',
              'cyan': '36',
              'white': '37',
              }

    # pre-define a few base colors for
    # faster access and introspection
    RED = '\x1b[31m'
    GREEN = '\x1b[32m'
    YELLOW = '\x1b[33m'
    BLUE = '\x1b[34m'
    MAGENTA = '\x1b[35m'
    CYAN = '\x1b[36m'
    WHITE = '\x1b[37m'
    BLACK = '\x1b[30m'
    BRIGHTRED = '\x1b[91m'
    BRIGHTGREEN = '\x1b[92m'
    BRIGHTYELLOW = '\x1b[93m'
    BRIGHTBLUE = '\x1b[94m'
    BRIGHTMAGENTA = '\x1b[95m'
    BRIGHTCYAN = '\x1b[96m'
    BRIGHTWHITE = '\x1b[97m'
    BRIGHTBLACK = '\x1b[90m'

    # Command Codes
    RESET = '\x1b[0m'      # Reset coloring to terminal default
    CLS = '\x1b[2J\x1b[H'  # Clear screen
    CLRLINE = '\x1b[K'     # Clear line

    def __getattr__(self, name):
        ''' Get attribute. Allows accessing color combos
            such as color.WHITE_BGBLUE_BOLD
        '''
        vals = [v.lower() for v in name.split('_')]
        fmtlist = []
        for v in vals:
            if v == 'bold':
                fmtlist.append('1')
            elif v == 'under' or v == 'underline' or v == 'uline':
                fmtlist.append('4')
            elif v.startswith('bg'):
                # Background colors are 10+ foreground colors
                fmtlist.append(str(int(self.ctable.get(v[2:], v[2:]))+10))
            else:
                fmtlist.append(self.ctable.get(v, v))
        return '\x1b[{}m'.format(';'.join(fmtlist))

    def rgb(self, r, g, b):
        ''' Get terminal color code from RGB (0-255) '''
        return f'\x1b[38;2;{r};{g};{b}m'

    def bgrgb(self, r, g, b):
        ''' Get background color code from RGB (0-255) '''
        return f'\x1b[48;2;{r};{g};{b}m'


color = _Color()


class Theme(object):
    ''' Color theme manager. Attributes (terminal color codes)
        that define a theme:

        NORM: Normal text
        BORDER: Borders for boxes, messages,etc.
        HLIGHT: Text that is highlighted by the cursor
        SELECT: Item that is selected/enabled but not highlighted
        HSELECT: Item that is selected/enabled and highlighted
        NAME: Name or title text
        MSG: Message text
        BUTTON: Button text
        ERROR: Color for error messages
    '''
    def __init__(self):
        self.settheme()

    def settheme(self, name=None):
        ''' Set the theme by name. Available themes are
            'default', 'blue' and 'sand'. '''
        if name == 'blue':
            self.NORM = color.WHITE_BGBLUE
            self.BORDER = color.WHITE
            self.HLIGHT = color.WHITE_BGGREEN
            self.SELECT = color.BRIGHTWHITE_BGBRIGHTBLUE
            self.NAME = color.BRIGHTBLUE
            self.MSG = color.WHITE
            self.BUTTON = color.WHITE_BGBLUE
            self.ERROR = color.RED
            self.HSELECT = color.BRIGHTYELLOW_BGBRIGHTBLUE

        elif name == 'sand':
            self.NORM = color.RED_BGWHITE
            self.BORDER = color.BLACK
            self.HLIGHT = color.BRIGHTYELLOW_BGCYAN
            self.SELECT = color.WHITE_BGCYAN
            self.NAME = color.BRIGHTGREEN
            self.MSG = color.BRIGHTRED
            self.BUTTON = color.RED_BGWHITE
            self.ERROR = color.BRIGHTRED
            self.HSELECT = color.RED_BGCYAN

        else:  # Default theme to look decent on white or black background terminals
            self.NORM = color.RESET
            self.BORDER = color.RESET
            self.HLIGHT = color.WHITE_BGBLUE
            self.SELECT = color.BLACK_BGWHITE
            self.NAME = color.BRIGHTGREEN
            self.MSG = color.BRIGHTMAGENTA
            self.BUTTON = color.RESET
            self.ERROR = color.RED
            self.HSELECT = color.YELLOW_BGBLUE


theme = Theme()
