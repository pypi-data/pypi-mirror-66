''' Demonstrates using tacotui widgets '''
import time
from tacotui import screen, widgets, theme


def demo():
    screen.clear()
    while True:
        screen.clear()
        order = widgets.form(f'TacoTUI Order Form',
                ('First Name:', str),
                ('Last Name:', str),
                ('Number of tacos:', int),
                ('Tortilla', ['Corn', 'Flour']),
                ('Filling:', ['Beef', 'Chicken', 'Carnitas', 'Bean', 'Calabacitas']),
                ('Chile:', ['Red', 'Green', 'Christmas']),
                ('', ['Smothered', 'On the side']),
                box=True,
                )

        screen.clear()
        toppings = widgets.multi_select(['Cheese', 'Lettuce', 'Tomato', 'Sour Cream', 'Avocado', 'Black Beans', 'Asparagus'], prompt='Choose your toppings')

        screen.clear()
        for i in range(10):
            widgets.progress(i*10, prompt='Cooking tacos...')
            time.sleep(0.5)

        screen.clear()
        again = widgets.message(f'Your {order[4].lower()} tacos with {len(toppings)} toppings are ready.\nDo you want to place another order?', buttons=['Yes', 'No'])
        if again == 'No':
            break

if __name__ == '__main__':
    demo()
