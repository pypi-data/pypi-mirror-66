''' Tacotui example of number guessing game '''
import time
from random import randint

from tacotui import color, theme, screen, widgets


def computerguess():
    ''' Computer guesses the number '''
    screen.clear()
    N = int(widgets.list_select(['10', '100', '1000', '10000'], prompt='Think of a number between 1 and:')[1])###, x=3, y=3)[1])

    screen.clear()
    widgets.message(f'Ok, press any key when you have your number between {theme.NAME}1 and {N}{theme.NORM}')
    widgets.getch()

    rng = range(1, N+1)
    guess = randint(1, N)  # Start with a random number to make it more fun.
    cnt = 1
    while True:
        screen.clear()
        ans = widgets.message(f'Is it {guess}?', buttons=['Higher', 'Lower', "That's It!"])
        if ans == 'Higher':
            rng = range(guess+1, rng[-1]+1)
        elif ans == 'Lower':
            rng = range(rng[0], guess+1)
        else:
            screen.clear()
            widgets.message(f'Woohoo! I guessed it in {cnt} tries.')
            break

        if len(rng) < 1:
            screen.clear()
            widgets.message(f"{theme.ERROR}Hey, you're cheating!{theme.NORM}")
            break
        guess = rng[0] + (rng[-1]-rng[0])//2
        cnt += 1
    widgets.getch()


def humanguess():
    ''' Human guesses the number '''
    screen.clear()
    N = int(widgets.list_select(['10', '100', '1000', '10000'], prompt="Ok, I'll think of a number between 1 and:")[1])
    number = randint(1, N)

    cnt = 1
    while True:
        screen.clear()
        guess = widgets.get_int('What is your guess? ')
        if guess < number:
            screen.clear()
            widgets.message(f'Higher than {guess}.')
            time.sleep(1.5)
        elif guess > number:
            screen.clear()
            widgets.message(f'Lower than {guess}.')
            time.sleep(1.5)
        else:
            widgets.message(f"That's it! You guessed it in {cnt} tries.")
            break
        cnt += 1
    widgets.getch()


def game():
    screen.hide_cursor()
    screen.clear()
    widgets.message('Number guessing game!')
    time.sleep(2)

    while True:
        screen.clear()
        _, choice = widgets.list_select(['Computer guesses the number', 'Human guesses the number', 'Done with guessing'], prompt='What kind of guessing game should we play?')

        if 'Computer' in choice:
            computerguess()
        elif 'Human' in choice:
            humanguess()
        else:
            screen.clear()
            widgets.message(f'{theme.NAME}Thanks for playing!{theme.NORM}')
            break

if __name__ == '__main__':
    game()
