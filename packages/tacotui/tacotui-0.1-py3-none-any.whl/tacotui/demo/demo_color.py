''' Demonstrate setting text color, position, and widgets '''
import time
from random import randint
from tacotui import color, screen, widgets

colors = ['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE',
          'MAGENTA', 'CYAN', 'WHITE', 'BRIGHTBLACK',
          'BRIGHTRED', 'BRIGHTGREEN', 'BRIGHTYELLOW']

def demo1():
    ''' Show all predefined colors '''
    screen.clear()
    for i, c in enumerate(colors):
        screen.setxy(1, i+1)
        print(f'{getattr(color, c)}{c}{color.RESET}')

        screen.setxy(20, i+1)
        print(f'{color.WHITE}{getattr(color, "BG"+c)}{"BG"+c}{color.RESET}')

        screen.setxy(40, i+1)
        print(f'{getattr(color, c+"_BOLD")}{c+"_BOLD"}{color.RESET}')
        
        screen.setxy(60, i+1)
        print(f'{getattr(color, c+"_UNDER")}{c+"_UNDER"}{color.RESET}')

    widgets.getch()

def demo2():
    ''' Demonstrate RGB coloring functions '''
    screen.clear()
    for i in range(screen.scrheight):
        r = int(i*(255/screen.scrheight))
        g = int(i*(255/screen.scrheight))
        b = int(i*(255/screen.scrheight))
        print(f'{color.rgb(r,50,50)}RGB({r},50,50)    {color.rgb(50,g,50)}RGB(50,{g},50)    {color.rgb(50,50,b)}RGB(50,50,{b})   {color.rgb(r,g,b)}RGB({r},{g},{b})')
    widgets.getch()


def demo3():
    ''' Demonstrate positioning on screen '''
    screen.clear()
    print('Positioning...')
    # Printing pos.XY attribute for positioning
    print(f'{screen.pos.XY5_3}screen.pos.XY5_3')

    # Positioning using screen.setxy
    for i in range(10):
        x = randint(1, screen.scrwidth-8)
        y = randint(1, screen.scrheight-8)
        screen.setxy(x, y)
        print(f'({x}, {y})')
    widgets.getch()


def demo():
    demo1()
    demo2()
    demo3()


if __name__ == '__main__':
    demo()

