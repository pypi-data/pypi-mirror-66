''' Cross-platform getch function to get single keystroke from keyboard '''
import time
import sys


class _Getch:
    ''' Gets a single character from standard input  Does not
        echo to the screen.
    '''
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self, timeout=None):
        char = self.impl(timeout=timeout)
        key = self.impl.decode(char)
        return key


class _GetchUnix:
    def __init__(self):
        import tty
        import sys

    def __call__(self, timeout=None):
        import tty
        import termios
        from select import select

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        ch = None
        try:
            tty.setraw(sys.stdin.fileno())
            i, o, e = select([sys.stdin.fileno()], [], [], timeout)
            if i:
                ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def decode(self, char):
        ''' Decode key into human-readable character or key name '''
        if char is None:
            return None
        elif char == '\x03':
            raise KeyboardInterrupt
        elif char == '\x04':
            raise EOFError
        elif ord(char) == 127:
            key = 'backspace'
        elif char in ['\n', '\r']:
            key = 'enter'
        elif char == '\t':
            key = 'tab'
        elif char == '\x1b':
            # Escape char, need two more bytes
            char += sys.stdin.read(2)
            key = {'[A': 'up',
                   '[B': 'down',
                   '[C': 'right',
                   '[D': 'left',
                   '[F': 'end',
                   '[H': 'home',
                   '[3': 'delete',
                   '[2': 'insert',
                   '[5': 'pgup',
                   '[6': 'pgdn',
                   }.get(char[1:], None)
        else:
            key = str(char)
        return key


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self, timeout=None):
        import msvcrt
        starttime = time.time()
        while True:
            if msvcrt.kbhit():
                return msvcrt.getch()

            if timeout is not None and time.time() - starttime > timeout:
                return None

    def decode(self, char):
        ''' Decode key into human-readable character or key name '''
        if char is None:
            return None
        elif char == b'\x03':
            raise KeyboardInterrupt
        elif char == b'\x04':
            raise EOFError
        elif char == b'\x08':
            key = 'backspace'
        elif char in [b'\n', b'\r']:
            key = 'enter'
        elif char == b'\t':
            key = 'tab'
        elif char in [b'\xe0', b'\x00']:  # 00 for numpad, e0 for arrows
            # Escape char, need two more bytes
            char2 = self()
            key = {b'H': 'up',
                   b'P': 'down',
                   b'M': 'right',
                   b'K': 'left',
                   b'G': 'upleft',
                   b'I': 'upright',
                   b'O': 'downleft',
                   b'Q': 'downright',
                   b'S': 'delete',
                   }.get(char2, char)
        else:
            key = char.decode()
        return key


getch = _Getch()


if __name__ == '__main__':
    # Timeout test
    while True:
        print('Press a key ', end='')
        ch = getch(timeout=3)
        if ch is None:
            print('TIMEOUT')
        else:
            print(ch)

