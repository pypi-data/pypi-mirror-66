''' Demonstrate the different widgets '''
import time
from random import randint
from tacotui import color, theme, screen, widgets


def demo():
    ''' Step through the different widgets '''
    screen.hide_cursor(True)
    screen.clear()
    # It's generally best to use colors from theme rather than colors directly. That prevents
    # ending up with Black on Black, for example.
    widgets.message(f'This is a message. The text can {color.YELLOW}have different colors.{color.RESET}') 
    widgets.getch()

    screen.clear()
    yesno = widgets.message('This message has buttons', buttons=['Yes', 'No'])
    screen.setxy(1, 1)
    print(f'You selected {theme.NAME}{yesno}{theme.NORM}.')
    widgets.getch()

    screen.clear()
    print(f'The {theme.NAME}get_int{theme.NORM} function prompts the user for an integer. It will\ncomplain until a valid integer is entered.')
    i = widgets.get_int('Enter a whole number: ', x=0, y=4)

    screen.setxy(1, 7)
    print(f'The {theme.NAME}get_float{theme.NORM} function prompts the user for a float value.\nIt will complain until a valid float is entered.')
    i = widgets.get_float('Enter a number between 1 and 100: ', fmin=1, fmax=100, x=0, y=10)

    screen.clear()
    print(f'This is a {theme.NAME}list_select{theme.NORM} widget. Use the up and down arrow keys\nand press enter to select an item.')
    index, item = widgets.list_select(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], h=6)
    screen.setxy(1, 4)
    print(f'You selected {theme.NAME}{item}{theme.NORM}.')
    widgets.getch()

    screen.clear()
    print(f'This is a {theme.NAME}multi_select{theme.NORM} widget. Use the up and down arrow keys\nand press enter select multiple items.')
    indexes, items = widgets.multi_select(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], h=8)
    items = ', '.join(items)
    screen.setxy(1, 4)
    print(f'You selected {theme.NAME}{items}{theme.NORM}.')
    widgets.getch()

    screen.clear()
    v = widgets.form(f'TacoTUI Order Form',
            ('First Name:', str),
            ('Last Name:', str),
            ('Number of tacos:', int),
            ('Filling:', ['Beef', 'Chicken', 'Bean', 'Calabacitas']),
            ('Chile:', ['Red', 'Green', 'Christmas']),
            ('', ['Smothered', 'On the side']),
            ('Temperature:', float),  # I need something to demonstrate floats...
            box=True,
            )
    screen.setxy(1, 1)
    screen.sprint('You entered:')
    screen.setxy(2, 2)
    screen.sprint(v)
    widgets.getch()

    screen.clear()
    widgets.slider('Slider widget', minval=0, maxval=100, showval=True)

    screen.clear()
    for i in range(11):
        widgets.progress(i*10, showpct=True, prompt='Progress...', w=70, color=f'{theme.MSG}')
        time.sleep(0.5)
    widgets.getch()

    screen.clear()
    print('file_select widget')
    fname = widgets.file_select(y=2, prompt='Select a file')
    screen.setxy(1, 1)
    print(f'File selected:  {fname}')
    widgets.getch()



if __name__ == '__main__':
    demo()
