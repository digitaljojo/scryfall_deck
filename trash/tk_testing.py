from tkinter import *
from tkinter import ttk

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5) / 10000.0)
    except ValueError:
        pass


root = Tk()
root.title('Commander Deck Builder')

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# card = StringVar()
feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky='W, E')

meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=3, sticky='W, E')

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=4, sticky=SW)

ttk.Label(mainframe, text='feet').grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text='is equivalent to ').grid(column=3, row=2, sticky=E)
ttk.Label(mainframe, text='meters').grid(column=3, row=3, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
feet_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()
'''


def commander():
    try:
        com = input("Who is your commander?\n====>")  # User enters their search query.
        card = scrython.cards.Search(fuzzy=com)  # Scrython tries to find the card. Creates a list of possible matches.

        # Print a list of all the USABLE matches. If len = 1, say that's the commander.
        listed = []
        round = 0
        for choice in range(card.data_length()):
            x = card.data(choice)

            check = x['type_line'].lower()  # converts type line to lower for easier check
            # Check to see if a legendary creature that's legal in the format.
            if commander_legal(x) and ('legendary' in check and 'creature' in check):
                print(f'<--{round}--> {card.data(choice, 'name')} ')
                listed.append(choice)
                round += 1

        if len(listed) > 1:
            my = int(input("Please choose a commander from the previous list:\n"))
        else:
            my = 0

        card = card.data(listed[my])  # This variable turns card into a usable dictionary.
        print(f"Your commander is {card['name']} ")
        card = scrython.cards.Named(exact=card['name'])
    except:
        print('Can\'t decide? Don\'t worry, I got you fam!')
        x = random_card()  # Named obj
        check = x.type_line().lower()

        my = 0
        while my < 1:
            if commander_legal(x) and ('legendary' in check and 'creature' in check):
                print(f'{x.name()} is the commander chosen for you.')
                break
        card = x  # This variable turns card into a Named obj.
        print(f"Your commander is {card.name()} ")
    finally:
        print(
            "You can only use cards of the following colors:")  # Next is using match case to print the colors more user friendly.
        human_color(card)
        print('\n')

    return card


def commander_legal(card):
    try:  # Search obj
        if card['commander'] == 'not_legal':
            return False
        else:
            return True
    except:  # Name obj
        if card.legalities()['commander'] == 'not_legal':
            return False
        else:
            return True

def adding(comm):
    deck: list[object] = []
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    while len(deck) < 10:
        card = random_card()
        if identity(card, comm) and commander_legal(card) and 'Land' not in card.type_line():
            deck.append(card)
            bar.update(len(deck))
    print('\n\n')
    return deck


def adding_others(comm):
    deck: list[object] = []
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    while len(deck) < 31:
        card = random_card()
        x = card.type_line()
        if identity(card, comm) and commander_legal(card) and 'Creature' not in x and 'Land' not in x:
            deck.append(card)
            bar.update(len(deck))
    print('\n\n')
    return deck




'''