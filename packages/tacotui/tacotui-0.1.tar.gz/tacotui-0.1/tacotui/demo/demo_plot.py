from tacotui import screen, color, widgets

def demo():
    screen.clear()
    screen.hide_cursor(True)

    widgets.barplot(('Cheese', 10), ('Lettuce', 3), ('Tomato', 5), ('Beans', 6), x=3, y=3, w=screen.scrwidth//2)

    widgets.barplot(('Beef', 8), ('Chicken', 5), ('Carnitas', 6), ('Calabacitas', 4),
                    w=screen.scrwidth//2, x=3, y=9, colors=[color.BLUE, color.YELLOW])
    widgets.getch()

    screen.clear()
    x = list(range(-10,11))
    y = [xval**3 for xval in x]
    widgets.textplot((x, y), title='y = x**3', w=screen.scrwidth//2, h=screen.scrheight//2)
    widgets.getch()


if __name__ == '__main__':
    demo()
