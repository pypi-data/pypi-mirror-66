''' Simple TUI widgets. All widgets are drawn using the colors defined in
    the current theme module. For example a message widget is drawn using the
    theme.MSG color for text and theme.BORDER color for the border.

    Color of string prompts can be overriden by adding color commands to the
    prompt text, for example:

        prompt=f'This is a {color.RED}red message!{color.RESET}.'
        
    Or use colors defined in the theme to prevent issues with default terminal
    configurations set by the OS or user.
    
        prompt=f'This is a {theme.NAME}message colored by the theme!{theme.NORM}.'
'''
import os
import time

from .getch import getch
from . import screen
from .color import color, theme


def _iterable(obj):
    ''' Check if obj is iterable '''
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def box(x, y, w, h):
    ''' Draw a box

        Parameters
        ----------
        x: int
            Left side of the box
        y: int
            Top side of the box
        w: int
            Width of the box
        h: int
            Height of the box
    '''
    screen.setxy(x, y)
    screen.sprint(theme.BORDER)
    screen.sprint('┌' + '─'*(w-2) + '┐')
    for i in range(y+1, y+h):
        screen.setxy(x, i)
        screen.sprint('│')
        screen.setxy(x+w-1, i)
        screen.sprint('│')
    screen.setxy(x, y+h)
    screen.sprint('└' + '─'*(w-2) + '┘')
    screen.sprint(theme.NORM)


def message(s, buttons=None, **kwargs):
    ''' Show a message box with optional buttons

        Parameters
        ----------
        s: string
            Message to display
        buttons: list
            List of button names

        Keyword Arguments
        -----------------
        x, y: int
            Coordinates of message box

        Returns
        -------
        btn: string
            Text of the selected button, or None if no
            buttons are defined.
    '''
    lines = s.splitlines()
    if len(lines) > 0:
        boxwidth = max([len(l) for l in lines]) + 4
        boxheight = len(lines) + 1
    else:
        boxwidth = 20
        boxheight = 0

    if buttons is not None:
        boxheight += 2
        bwidths = ([len(b)+2 for b in buttons])
        boxwidth = max(sum(bwidths)+4, boxwidth)

    x = kwargs.get('x', (screen.scrwidth - boxwidth)//2)
    y = kwargs.get('y', (screen.scrheight - boxheight)//2)

    if buttons is not None:
        buttony = y + boxheight - 1
        bwidth = (boxwidth-2) // len(buttons)
        btext = [screen.centertext(b, bwidth) for b in buttons]

    box(x, y, boxwidth, boxheight)
    screen.sprint(theme.MSG)
    for i, line in enumerate(lines):
        screen.setxy(x+2, i+y+1)
        screen.sprint(line)
    screen.sprint(theme.NORM)

    result = None
    selbutton = 0
    while buttons is not None:
        for i, b in enumerate(btext):
            screen.setxy(x+1+i*bwidth, buttony)
            if i == selbutton:
                screen.sprint(f'{theme.HLIGHT}{b}')
            else:
                screen.sprint(f'{theme.BUTTON}{b}')

        key = getch()
        if key in ['right', 'k', 'l'] and selbutton < len(buttons)-1:
            selbutton += 1
        elif key in ['left', 'h', 'j'] and selbutton > 0:
            selbutton -= 1
        elif key == 'enter':
            result = buttons[selbutton]
            break

    screen.sprint(theme.NORM)
    return result


def get_int(prompt, **kwargs):
    ''' Get an integer value.

        Parameters
        ----------
        prompt: string
            Prompt to show the user

        Keyword Arguments
        -----------------
        x, y: int
            Location to display prompt. An error message
            will display on the next line if a non-integer
            value is entered.

        Returns
        -------
        value: int
            Integer value entered by the user
    '''
    x = kwargs.get('x', (screen.scrwidth-len(prompt))//2)
    y = kwargs.get('y', screen.scrheight//2)
    while True:
        screen.setxy(x, y)
        screen.sprint(f'{theme.NORM}{prompt}')
        try:
            ch = input()
            val = int(ch)
        except ValueError:
            screen.setxy(x+1, y+1)
            screen.sprint(f'{theme.ERROR}Please enter an integer value.{theme.NORM}')
            time.sleep(2)
            screen.setxy(x+1, y+1)
            screen.sprint(f'{color.CLRLINE}')
        else:
            break
    return val


def get_char(options=None, **kwargs):
    ''' Input a character.

        Keyword Arguments
        -----------------
        options: list, optional
            List of acceptable characters
        x, y: int
            Location for showing error message if
            the entered character is not in options.

        Returns
        -------
        value: string
            Single-character string entered by the user
    '''
    x = kwargs.get('x', screen.scrwidth//2)
    y = kwargs.get('y', screen.scrheight//2)
    screen.setxy(x, y)
    ch = getch()
    while options is not None and ch not in options:
        screen.setxy(x+1, y+1)
        screen.sprint(f'{theme.ERROR}Please press ' + ', '.join(options))
        ch = getch()
    return ch


def get_float(prompt, **kwargs):
    ''' Get a float value.

        Parameters
        ----------
        prompt: string
            Prompt to show the user

        Keyword Arguments
        -----------------
        x, y: int
            Position for the prompt. If invalid or out-of-range
            value is entered, error message is shown on the
            next line.
        fmin: float
            Minimum acceptable float value
        fmax: float
            Maximum acceptable float value

        Returns
        -------
        value: float
            Floating point value entered by the user
    '''
    x = kwargs.get('x', (screen.scrwidth-len(prompt))//2)
    y = kwargs.get('y', screen.scrheight//2)
    fmin = kwargs.get('fmin', -1E99)
    fmax = kwargs.get('fmax', 1E99)

    while True:
        screen.setxy(x, y)
        screen.sprint(f'{color.CLRLINE}{theme.NORM}{prompt}')
        try:
            ch = input()
            val = float(ch)
        except ValueError:
            screen.setxy(x+1, y+1)
            screen.sprint(f'{theme.ERROR}Please enter a numeric value.{theme.NORM}')
            time.sleep(2)
            screen.setxy(x+1, y+1)
            screen.sprint(f'{color.CLRLINE}')
        else:
            if val < fmin or val > fmax:
                screen.setxy(x+1, y+1)
                screen.sprint(f'{theme.ERROR}Value must be between '
                              f'{theme.NAME}{fmin}{theme.ERROR} and '
                              f'{theme.NAME}{fmax}.{theme.ERROR}')
                time.sleep(2)
                screen.setxy(x+1, y+1)
                screen.sprint(f'{color.CLRLINE}')
            else:
                break
    screen.sprint(theme.NORM)
    return val


def get_date(prompt, **kwargs):
    ''' Get a date-time (requires dateutil package)

        Parameters
        ----------
        prompt: string
            Prompt to show the user
        x, y: int
            Position of prompt. If invalid date is entered,
            error message will show on next line.

        Returns
        -------
        value: datetime
            Date value entered by the user
    '''
    from dateutil.parser import parse  # not standard lib!
    x = kwargs.get('x', (screen.scrwidth-len(prompt))//2)
    y = kwargs.get('y', screen.scrheight//2)
    while True:
        screen.setxy(x, y)
        screen.sprint(f'{color.CLRLINE}{prompt}')
        try:
            s = input()
            d = parse(s)
        except ValueError:
            screen.setxy(x+1, y+1)
            screen.sprint(f'{theme.ERROR}Please enter a valid date.{theme.NORM}')
            time.sleep(2)
            screen.setxy(x+1, y+1)
            screen.sprint(f'{color.CLRLINE}')
        else:
            break
    return d


def list_select(options, prompt='', **kwargs):
    ''' Select an item from a list

        Parameters
        ----------
        options: list
            List of items for the list box
        prompt: string
            Text to show just above the box

        Keyword Arguments
        -----------------
        x, y: int
            Position of the box. If not provided, will be centered
            on the screen.
        w, h: int
            Width and height of box. If not provided, will
            be determined based on the size of the options
            list.

        Returns
        -------
        index: int
            Index of list item selected by the user
        value: string
            String of list item selected by the user
    '''
    w = kwargs.get('w', max([len(p) for p in options]) + 4)
    x = kwargs.get('x', (screen.scrwidth - w)//2)
    if 'y' not in kwargs:
        if 'h' not in kwargs:
            h = min(len(options), screen.scrheight-1) + 1
            y = (screen.scrheight - h)//2
        else:
            h = kwargs.get('h')
            y = (screen.scrheight - h - 3)//2
    else:
        y = kwargs.get('y')
        h = kwargs.get('h', min(len(options)+1, screen.scrheight-y))

    visiblelines = min(h-1, len(options))
    poptions = [format(p[:w-4], f'{w-4}s') for p in options]  # All same width for printing

    if prompt:
        plines = prompt.splitlines()
        pwidth = max([len(p) for p in plines])
        plines = [screen.centertext(p, pwidth) for p in plines]
        prompty = y - len(plines)
        for i, line in enumerate(plines):
            screen.setxy(screen.scrwidth//2 - pwidth//2, prompty+i)
            screen.sprint(line)

    box(x, y, w, h)
    cursor = 0
    topitem = 0
    while True:
        for i in range(visiblelines):
            screen.setxy(x+1, y+i+1)
            if i+topitem == cursor:
                screen.sprint(f'{theme.HLIGHT}{poptions[i+topitem]}{theme.NORM}')
            else:
                screen.sprint(f'{poptions[i+topitem]}')

        key = getch()
        if key in ['up', 'k'] and cursor > 0:
            if cursor == topitem:
                topitem -= 1
            cursor -= 1

        elif key in ['down', 'j'] and cursor < len(options)-1:
            if cursor-topitem == visiblelines-1 and topitem < len(options)-visiblelines+1:
                topitem += 1
            cursor += 1

        elif key == 'enter':
            break
    screen.sprint(theme.NORM)
    return cursor, options[cursor]


def multi_select(options, prompt='', **kwargs):
    ''' Select multiple items from a list.

        Parameters
        ----------
        options: list
            List of options to show in the box
        prompt: string
            Text to show just above the box

        Keyword Arguments
        -----------------
        x, y: int
            Position of the box. If not provided, will be centered
            on the screen.
        w, h: int
            Width and height of box. If not provided, will
            be determined based on the size of the options
            list.

        Returns
        -------
        index: list of int
            List of all indexes selected by the user
        values: list of string
            List of all strings values selected by the user
    '''
    w = kwargs.get('w', max([len(p) for p in options]) + 4)
    x = kwargs.get('x', (screen.scrwidth - w)//2)
    if 'y' not in kwargs:
        if 'h' not in kwargs:
            h = min(len(options), screen.scrheight-1)+3
            y = (screen.scrheight - h)//2
        else:
            h = kwargs.get('h')
            y = (screen.scrheight - h - 3)//2
    else:
        y = kwargs.get('y')
        h = kwargs.get('h', min(len(options), screen.scrheight-y))

    visiblelines = min(h-3, len(options))
    poptions = [format(p[:w-4], f'{w-4}s') for p in options]  # All same width for printing

    if prompt:
        plines = prompt.splitlines()
        pwidth = max([len(p) for p in plines])
        plines = [screen.centertext(p, pwidth) for p in plines]
        prompty = y - len(plines)
        for i, line in enumerate(plines):
            screen.setxy(screen.scrwidth//2 - pwidth//2, prompty+i)
            screen.sprint(line)

    donestr = format('DONE', f'^{w-4}s')
    selitems = []
    cursor = 0
    topitem = 0
    box(x, y, w, h)
    while True:
        for i in range(visiblelines):
            screen.setxy(x+1, y+i+1)
            if i+topitem == cursor and cursor in selitems:
                screen.sprint(f'{theme.HSELECT}{poptions[i+topitem]}{theme.NORM}')
            elif i+topitem == cursor:
                screen.sprint(f'{theme.HLIGHT}{poptions[i+topitem]}{theme.NORM}')
            elif i+topitem in selitems:
                screen.sprint(f'{theme.SELECT}{poptions[i+topitem]}{theme.NORM}')
            else:
                screen.sprint(f'{theme.NORM}{poptions[i+topitem]}')

        screen.setxy(x+1, y+h-1)
        if cursor == 'done':
            screen.sprint(f'{theme.HLIGHT}{donestr}{theme.NORM}')
        else:
            screen.sprint(f'{theme.NORM}{donestr}')

        key = getch()
        if key in ['up', 'k'] and cursor is not None and cursor != 'done' and cursor > 0:
            if cursor == topitem:
                topitem -= 1
            cursor -= 1

        elif (key in ['down', 'j']
              and cursor is not None
              and cursor != 'done'
              and cursor < len(options)-1):

            if cursor-topitem == visiblelines-1 and topitem < len(options)-visiblelines+1:
                topitem += 1
            cursor += 1

        elif key in ['left', 'right', 'h', 'l']:
            if cursor != 'done':
                cursorsaved = cursor
                cursor = 'done'
            else:
                cursor = cursorsaved

        elif key == 'enter':
            if cursor == 'done':
                break
            elif cursor in selitems:
                selitems.remove(cursor)
            else:
                selitems.append(cursor)
    return selitems, [options[i] for i in selitems]


def file_select(path='.', mode='existing', **kwargs):
    ''' Select a file or folder.

        Parameters
        ----------
        path: string
            Starting folder location
        mode: string
            File selection mode. Either 'existing',
            'new', or 'folder'.

        Keyword Arguments
        -----------------
        x, y: int
            Top-left position of the file selection box. Defaults
            to 0, 0.
        w, h: int
            Width and height of file selection box. Defaults to
            fill the full screen.
        showhidden: bool
            Show hidden files (starting with dot)
        filt: iterable
            List of file extensions to show, example ['py', 'pyc', 'pyo']

        Returns
        -------
        fname: string
            File or folder name as entered by the user
    '''
    path = os.path.abspath(path)
    name = ''   # Name of new file
    prompt = kwargs.get('prompt', None)
    showhidden = kwargs.get('showhidden', False)
    filt = kwargs.get('filt', [])

    x = kwargs.get('x', 1)
    y = kwargs.get('y', 1)
    boxtop = y+1 + (prompt is not None)

    width = kwargs.get('w', screen.scrwidth-x)
    height = kwargs.get('h', screen.scrheight-y)

    maxlines = height-3-(prompt is not None)
    panelwidth = width//2

    while True:  # New folder selected at the top of this loop
        screen.clear()
        try:
            folderlist = ['..'] + [o for o in os.listdir(path) if os.path.isdir(os.path.join(path, o))]
            filelist = [o for o in os.listdir(path) if not os.path.isdir(os.path.join(path, o))]
        except PermissionError:
            folderlist = ['..']
            filelist = []

        if not showhidden:
            folderlist = [f for f in folderlist if f in ['.', '..'] or not f.startswith('.')]
            filelist = [f for f in filelist if not f.startswith('.')]

        if len(filt) > 0:
            filteredlist = []
            for f in filt:
                filteredlist.extend([fname for fname in filelist if fname.lower().endswith(f.lower())])
            filelist = filteredlist

        visiblefolders = min(maxlines, len(folderlist))
        visiblefiles = min(maxlines, len(filelist))

        selitem = 'folders'  # 'files', 'ok', 'name', 'path'
        foldercursor = 0
        filecursor = None
        topfile = 0
        topfolder = 0

        box(x, boxtop, panelwidth, maxlines+1)
        box(x+panelwidth+1, boxtop, panelwidth, maxlines+1)
        if prompt:
            screen.setxy(x+1, y)
            screen.sprint(prompt)

        # Printable names, all same width
        foldernames = [format(p[:panelwidth-3], f'{panelwidth-3}s') for p in folderlist]
        filenames = [format(p[:panelwidth-3], f'{panelwidth-3}s') for p in filelist]

        while True:  # Cursor moves at the beginning of this loop
            screen.setxy(x+1, boxtop-1)
            if selitem == 'path':
                screen.sprint(f'{theme.HLIGHT}{path}{theme.NORM}')
            else:
                screen.sprint(f'{theme.NAME}{path}{theme.NORM}')

            screen.setxy(x+width-8, y+height)
            if selitem == 'ok':
                screen.sprint(f'{theme.HLIGHT}  Ok  {theme.NORM}')
            else:
                screen.sprint(f'{theme.BUTTON}  Ok  ')

            if mode == 'new':
                screen.setxy(x+2, y+height-1)
                screen.sprint(f'File Name:')
                if selitem == 'name':
                    screen.sprint(f' {theme.HLIGHT}{name} {theme.NORM}')
                else:
                    screen.sprint(f' {theme.NAME}{name}{theme.NORM}')
                namex = len(name) + 15
                screen.sprint('─'*(panelwidth-namex))

            for i in range(visiblefolders):  # Folders
                screen.setxy(x+2, boxtop+i+1)
                if selitem == 'folders' and i+topfolder == foldercursor:
                    screen.sprint(f'{theme.HLIGHT}{foldernames[i+topfolder]}{theme.NORM}')
                else:
                    screen.sprint(f'{theme.NORM}{foldernames[i+topfolder]}')

            for i in range(visiblefiles):  # Files
                screen.setxy(x+panelwidth+2, boxtop+i+1)
                if selitem == 'files' and i+topfile == filecursor:
                    screen.sprint(f'{theme.HLIGHT}{filenames[i+topfile]}{theme.NORM}')
                elif i+topfile == filecursor:
                    screen.sprint(f'{theme.NAME}{filenames[i+topfile]}{theme.NORM}')
                else:
                    screen.sprint(f'{theme.NORM}{filenames[i+topfile]}')

            key = getch()
            if selitem == 'folders':
                if key in ['up', 'k'] and foldercursor == 0:
                    selitem = 'path'
                elif key in ['up', 'k'] and foldercursor > 0:
                    if foldercursor == topfolder:
                        topfolder -= 1
                    foldercursor -= 1
                elif (key in ['down', 'j'] and foldercursor < len(folderlist) - 1):
                    if (foldercursor - topfolder == visiblefolders-1
                       and topfolder < len(folderlist)-visiblefolders+1):
                        topfolder += 1
                    foldercursor += 1
                elif key in ['left', 'right', 'h', 'l']:
                    if mode == 'existing':
                        selitem = 'files'
                        filecursor = 0
                    elif mode == 'folder':
                        selitem = 'ok'
                    elif mode == 'new':
                        selitem = 'name'
                elif mode == 'new' and key in ['down', 'j'] and foldercursor == len(folderlist)-1:
                    selitem = 'name'
                elif key == 'enter':
                    break

            elif selitem == 'files':
                if key in ['up', 'k'] and filecursor > 0:
                    if filecursor == topfile:
                        topfile -= 1
                    filecursor -= 1
                elif key in ['down', 'j'] and filecursor is not None and filecursor < len(filelist) - 1:
                    if (filecursor - topfile == visiblefiles-1
                       and topfile < len(filelist)-visiblefiles+1):
                        topfile += 1
                    filecursor += 1
                elif key in ['left', 'h']:
                    selitem = 'folders'
                elif key in ['right', 'l', 'enter']:
                    selitem = 'ok'

            elif selitem == 'path':
                if key in ['down', 'j']:
                    selitem = 'folders'
                elif key in ['right', 'l']:
                    selitem = 'files'
                elif key == 'enter':
                    screen.setxy(x+1, boxtop-1)
                    screen.hide_cursor(False)
                    screen.sprint(f'{theme.HLIGHT}{path}{theme.NAME}')
                    newpath = line_edit(path, x=x+1, y=boxtop-1)
                    screen.sprint(f'{theme.NORM}')
                    screen.hide_cursor(True)
                    break

            elif selitem == 'name':
                if key in ['up', 'left']:
                    selitem = 'folders'
                elif key in ['right', 'down']:
                    selitem = 'ok'
                else:
                    initname = name + key if len(key) == 1 else name
                    newname = line_edit(initname, prompt='Enter New Filename', x=x+1, y=y+height)
                    if newname != '':
                        name = newname   # Keep existing name if <enter> pressed on old name
                    screen.setxy(x+1, y+height)
                    screen.sprint(f'{theme.NORM}{color.CLRLINE}')
                    screen.hide_cursor(True)
                    selitem = 'ok'
                    continue

            elif selitem == 'ok':
                if key == 'enter':
                    if mode == 'new' and name == '':
                        screen.setxy(x+1, y+height)
                        screen.sprint(f'{theme.ERROR}Filename cannot be blank{theme.NORM}')
                    else:
                        break
                elif key in ['right', 'l'] and mode == 'folder':
                    selitem = 'files'
                    if filecursor is None:
                        filecursor = 0
                elif ((key in ['left', 'h'] and mode in ['folder', 'new'])
                      or (key in ['right', 'l'] and mode == 'new')):
                    selitem = 'folders'
                elif key in ['left', 'h'] and mode == 'existing':
                    selitem = 'files'

        if selitem == 'ok':
            break
        elif selitem == 'path':
            selitem = 'folders'
            newpath = os.path.normpath(newpath)
            if os.path.exists(newpath):
                path = newpath
        elif selitem == 'folders':
            path = os.path.normpath(os.path.join(path, folderlist[foldercursor]))

    if mode == 'folder':
        val = os.path.normpath(path)
    elif mode == 'existing':
        val = os.path.normpath(os.path.join(path, filelist[filecursor]))
    else:
        val = os.path.normpath(os.path.join(path, name))
    return val


def line_edit(s='', prompt='', **kwargs):
    ''' Enter a line of text, with possible initial value

        Parameters
        ----------
        s: string
            Default value for line edit
        prompt: string
            Text to show in front of entry area

        Keyword Arguments
        -----------------
        x, y: int
            Position of line edit

        Returns
        -------
        value: string
            Line entered by the user
    '''
    screen.hide_cursor(False)
    x = kwargs.get('x', 1)
    y = kwargs.get('y', 1)
    screen.setxy(x, y)
    if prompt != '' and not prompt.endswith(' '):
        prompt += ' '
    startx = x + len(prompt)
    screen.sprint(prompt)
    screen.sprint(f'{theme.NAME}{s}{theme.NORM}')
    while True:
        ch = getch()
        if len(ch) == 1:
            s += str(ch)
            screen.setxy(startx, y)
            screen.sprint(f'{theme.NAME}{s}{theme.NORM}{color.CLRLINE}')
        elif ch == 'backspace':
            s = s[:-1]
            screen.setxy(startx, y)
            screen.sprint(f'{color.CLRLINE}{theme.NAME}{s}{theme.NORM}{color.CLRLINE}')
        elif ch == 'enter':
            break
    screen.hide_cursor()
    return s


def form(title='', *items, **kwargs):
    ''' Make a form for entry of multiple items.

    Parameters
    ----------
    title: string
        Show a title on the form
    items: tuples
        Each row in the form is defined by a tuple of (prompt, datatype, [default])
        prompt: string value to show in this line
        datatype: either int, float, str, or a list of
        option values (selectable by arrow keys in the form)
        default (optional): initial value to show.

    Keyword Arguments
    -----------------
    x, y: int
        Top left position of the form
    w: int
        Width of the form

    Returns
    -------
    values: list
        List of all items entered in the form, in the same order
        they were defined, cast to the appropriate type.

    Notes
    -----
    int and float datatypes will be validated. User cannot select DONE
    until they enter valid numbers (or leave them blank). floats in
    scientific notation are allowed.
    '''
    selitem = 0
    prompts = [i[0] for i in items]
    col2x = max([len(p) for p in prompts]) + 3
    prompts = [format(p, '>{}'.format(col2x-3)) for p in prompts]  # Right-justify
    types = [i[1] for i in items]
    itemvalues = [str(i[2]) if len(i) > 2 else '' for i in items]  # Get default values
    # Make sure iterable items have a default
    itemvalues = [types[i][0] if (_iterable(types[i]) and itemvalues[i] == '')
                  else itemvalues[i] for i in range(len(items))]

    w = kwargs.get('w', len(prompts[0]) + 20)
    h = len(items) + 4
    x = kwargs.get('x', (screen.scrwidth-w)//2)
    y = kwargs.get('y', (screen.scrheight-h)//2)

    if kwargs.get('box', False):
        box(x-1, y-1, w+2, h+2)

    screen.setxy(x, y)
    screen.sprint(format(title, f'^{w}'))
    while True:
        valid = []
        for i in range(len(items)):
            if types[i] in [int, float] and itemvalues[i] != '':
                try:
                    types[i](itemvalues[i])
                except ValueError:
                    valid.append(False)  # Incomplete numeric value entered
                else:
                    valid.append(True)
            else:
                valid.append(True)

            if i == selitem:
                fmt = theme.MSG
            elif valid[i]:
                fmt = theme.NAME
            else:
                fmt = theme.ERROR
            screen.setxy(x, y+i+2)
            screen.sprint(prompts[i])
            screen.setxy(x+col2x, y+i+2)
            if _iterable(types[i]):
                s = format(f'\u25C4 {itemvalues[i]} \u25BA', f'<{w-col2x}')
                screen.sprint(f'{fmt}{s}{theme.NORM}')
            else:
                s = format(itemvalues[i], f'<{w-col2x}')
                screen.sprint(f'{fmt}{s}{theme.NORM}')

        screen.setxy(x+col2x, y+i+4)
        if selitem == len(items):
            screen.sprint(f'{theme.SELECT}DONE{theme.NORM}')
            screen.hide_cursor(True)
        else:
            screen.sprint(f'{theme.NORM}DONE')
            screen.hide_cursor(_iterable(types[selitem]))

        if selitem < len(itemvalues):
            screen.setxy(x+col2x + len(str(itemvalues[selitem])), y+selitem+2)

        ch = getch()
        if ch == 'enter' and selitem == len(itemvalues):
            if not all(valid):  # DONE
                selitem = valid.index(False)
            else:
                break

        elif ch == 'up' and selitem > 0:
            selitem -= 1

        elif ch in ['enter', 'down'] and selitem < len(itemvalues):
            selitem += 1

        elif (selitem < len(itemvalues)
              and _iterable(types[selitem])
              and ch in ['left', 'right', 'h', 'l']):

            idx = types[selitem].index(itemvalues[selitem])
            if ch in ['left', 'h'] and idx > 0:
                itemvalues[selitem] = types[selitem][idx-1]
            elif ch in ['right', 'l'] and idx < len(types[selitem])-1:
                itemvalues[selitem] = types[selitem][idx+1]

        elif ch == 'backspace':
            itemvalues[selitem] = itemvalues[selitem][:-1]

        elif selitem < len(itemvalues) and len(ch) == 1:
            if types[selitem] == str:
                itemvalues[selitem] += str(ch)
            elif types[selitem] == int:
                if ch.isnumeric() or (ch in ['+', '-'] and itemvalues[selitem] == ''):
                    itemvalues[selitem] += ch
            elif types[selitem] == float:
                if (ch.isnumeric() or
                   (ch == '.' and '.' not in itemvalues[selitem]) or
                   (ch in ['+', '-'] and itemvalues[selitem] == '') or
                   (ch in ['+', '-'] and 'e' in itemvalues[selitem].lower()) or
                   (ch in ['E', 'e'] and 'e' not in itemvalues[selitem].lower())):
                    itemvalues[selitem] += ch

    ret = []
    for i in range(len(items)):
        if _iterable(types[i]):
            ret.append(itemvalues[i])
        else:
            try:
                ret.append(types[i](itemvalues[i]))
            except ValueError:
                # Empty number is allowed, return None
                ret.append(None)
    return ret


def slider(prompt='', **kwargs):
    ''' Make a slider widget

        Parameters
        ----------
        prompt: string
            Text to show above the widget
        x, y: int
            Top-left position of the widget
        w: int
            Width in characters of the slider
        minval, maxval: float
            Miniumum and Maximum value represented by the slider
        showval: bool
            Whether to print the represented value to the right of the slider
        char: string
            Character to represent slider indicator
        color: string
            Color of slider indicator
        barcolor: string
            Color of slider bar

        Returns
        -------
        value: float
            Slider value when user presses enter
    '''
    w = kwargs.get('w', screen.scrwidth//2)
    x = kwargs.get('x', (screen.scrwidth-max(w, len(prompt)))//2)
    y = kwargs.get('y', screen.scrheight//2)
    bc = kwargs.get('barcolor', f'{theme.NORM}')
    c = kwargs.get('color', f'{theme.MSG}')
    minval = kwargs.get('minval', 0)
    maxval = kwargs.get('maxval', w)
    showval = kwargs.get('showval', False)
    char = kwargs.get('char', '\u2500')
    if prompt:
        screen.setxy(x, y-1)
        screen.sprint(prompt)
    val = kwargs.get('value', (maxval+minval)/2)
    i = int((val-minval)/(maxval-minval))
    bar = char * w
    while True:
        s = f'{bc}{bar[:i]}{c}\u2588{bc}{bar[i:]}'
        screen.setxy(x, y)
        screen.sprint(s)
        val = (i/w) * (maxval-minval) + minval
        if showval:
            screen.setxy(x+w+2, y)
            screen.sprint(f'{val:.2f}')

        ch = getch()
        if ch in ['left', 'h'] and i > 0:
            i -= 1
        elif ch in ['right', 'l'] and i < w:
            i += 1
        elif ch == 'enter':
            break
    return val


def progress(pct, prompt='', **kwargs):
    ''' Progress bar

        Parameters
        ----------
        pct: float
            Percent value to show (0-100 range)
        prompt: string
            Text to show above progress bar

        Keyword Arguments
        -----------------
        x, y: int
            Position of top left corner
        w: int
            Width of the progress bar
        c: string
            Color of indicator
        ch: string
            Character for indicator
        showpct: bool
            Print the percent value to the right of the indicator
    '''
    w = kwargs.get('w', int(screen.scrwidth*.8))
    x = kwargs.get('x', (screen.scrwidth-max(w, len(prompt)))//2)
    y = kwargs.get('y', screen.scrheight//2)
    c = kwargs.get('color', f'{theme.MSG}')
    ch = kwargs.get('char', '\u2588')
    showpct = kwargs.get('showpct', False)
    screen.setxy(x, y-1)
    screen.sprint(f'{theme.NORM}{prompt}')
    box(x, y, w, 2)
    screen.setxy(x+1, y+1)
    screen.sprint(c + ch*int((w-2)*pct/100))
    if showpct:
        screen.setxy(x+w+1, y+1)
        screen.sprint(f'{pct}%')


def textplot(*xypairs, **kwargs):
    ''' Plot x, y data as scatter plot

        Parameters
        ----------
        xypairs: tuples of lists
            Each xypair is a tuple of (x, y) data,
            where x and y are lists of values to plot.
        x, y: int
            Top-left position of plot
        w: int
            Plot width in characters
        h: int
            Plot height in characters
        title: string
            Title to print above the plot
        margin: int
            Size of left-side margin
        colors: list of string
            List of color codes to cycle for the plot points
        markers: list of string
            List of characters to cylce for the plot points
    '''
    colorlist = kwargs.get('colors',
                           [color.RED, color.BLUE, color.GREEN,
                            color.YELLOW, color.MAGENTA])
    markerlist = kwargs.get('markers',
                            ['\u25CF', '\u25B2', '\u25A0', '\u25CA', '\u00D7'])
    margin = kwargs.get('margin', 7)
    title = kwargs.get('title', '')

    w = kwargs.get('w', screen.scrwidth-2)
    h = kwargs.get('h', screen.scrheight-3)
    x = kwargs.get('x', 1)
    y = kwargs.get('y', 2)

    xmin = 1E99
    xmax = -1E99
    ymin = 1E99
    ymax = -1E99
    for xvals, yvals in xypairs:
        xmin = min(xmin, min(xvals))
        xmax = max(xmax, max(xvals))
        ymin = min(ymin, min(yvals))
        ymax = max(ymax, max(yvals))

    if title:
        screen.setxy(x+margin, y)
        screen.sprint(format(title, f'^{w-margin}'))

    box(x+margin+1, y+1, w-margin-1, h-2)  # Leave space for labels
    screen.setxy(x, y+h-1)
    screen.sprint(format(ymin, f'>{margin}.4g'))
    screen.setxy(x, y + (y+h-1)//2)
    screen.sprint(format((ymax+ymin)/2, f'>{margin}.4g'))
    screen.setxy(x, y+1)
    screen.sprint(format(ymax, f'>{margin}.4g'))

    screen.setxy(x+margin+1, y+h)
    screen.sprint(format(xmin, '.4g'))
    screen.setxy(x+margin+(w-margin)//2, y+h)
    screen.sprint(format((xmax+xmin)/2, '.4g'))
    screen.setxy(x+w, y+h)
    screen.sprint(format(xmax, f'<{margin}.4g'))

    for i, (xvals, yvals) in enumerate(xypairs):
        c = colorlist[i % len(colorlist)]
        char = markerlist[i % len(markerlist)]
        xnorm = [x + margin + 1 + int((x1-xmin)/(xmax-xmin) * (w-margin-2)) for x1 in xvals]
        ynorm = [y + h - 1 - int((y1-ymin)/(ymax-ymin) * (h-2)) for y1 in yvals]

        for xval, yval in zip(xnorm, ynorm):
            screen.setxy(xval, yval)
            screen.sprint(f'{c}{char}')


def barplot(*xypairs, **kwargs):
    ''' Make a horizontal bar plot

        Parameters
        ----------
        xypairs: tuples
            Tuples of (xlabel, yvalue)

        Keyword Arguments
        -----------------
        x, y: int
            Top-left position of bar plot
        w: int
            Total width of bar plot
        char: string
            Character to use for bar segment
        showvals: bool
            Print the numeric value at the end of each bar
        colors: list
            List of colors to cycle
    '''
    w = kwargs.get('w', screen.scrwidth-5)
    x = kwargs.get('x', 1)
    y = kwargs.get('y', 2)
    showvals = kwargs.get('showvals', False)
    char = kwargs.get('char', '\u2588')
    colorlist = kwargs.get('colors', [theme.NAME])

    margin = max([len(xval) for xval, _ in xypairs]) + 1
    ymax = max([yval for _, yval in xypairs])
    linelens = [int(yval/ymax * (w-margin)) for _, yval in xypairs]
    for i in range(len(xypairs)):
        c = colorlist[i % len(colorlist)]
        screen.setxy(x, y+i)
        screen.sprint(theme.NORM + format(xypairs[i][0], f'>{margin}'))
        screen.sprint(' ')
        screen.sprint(c + char * linelens[i])
        if showvals:
            screen.sprint(' ' + format(xypairs[i][1], '.2g'))

