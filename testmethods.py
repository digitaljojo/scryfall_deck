import math
import re
import progressbar
from random import randint
import scrython
import textwrap


def add_basic_lands(counter, deck):  # returns the deck with basic lands added
    for pip in counter: # Read through how many pips of each color. Add that many lands of that color.
        for card in range(counter[pip]):
            name = ''
            if counter[pip] > 0:
                match pip:  # Match the color to the basic land type.
                    case 'W':
                        name = 'Plains'
                    case 'U':
                        name = 'Island'
                    case 'B':
                        name = 'Swamp'
                    case 'R':
                        name = 'Mountain'
                    case 'G':
                        name = 'Forest'
                    case _:
                        print('Not sure how we got here. Hmm mm...')
                deck.append(scrython.cards.Named(exact=name))
    return deck


def auto_fill(deck, cdr):
    # Automatically performs the actions of the fill function for pure random deck goodness.
    typing = ['Creature', 'Enchantment', 'Artifact', 'Instant', 'Sorcery', 'Planeswalker', 'Land']
    # Loop through the types of cards and adds a set amount.
    for i in typing:
        timing = 0
        match i:
            case 'Creature':
                timing = 35
            case 'Enchantment':
                timing = 4
            case 'Artifact':
                timing = 4
            case 'Instant':
                timing = 6
            case 'Sorcery':
                timing = 6
            case 'Planeswalker':
                timing = 4
            case 'Land':
                timing = 5
            case _:
                print('Well, this is awkward...')

        for a in range(timing):
            plus = search_add(cdr, i.lower(), 10)
            deck.append(plus)


def fill(cdr):
    # Print out card types available to add.
    typing = ['Creature', 'Enchantment', 'Artifact', 'Instant', 'Sorcery', 'Planeswalker', 'Land']
    print('Card-types:')
    for i in range(len(typing)):
        if i == len(typing) - 1:
            print(f'{i}. {typing[i]}')
        elif i == len(typing) / 2 - 1:
            print(f'{i}. {typing[i]} \n')
        else:
            print(f'{i}. {typing[i]}', end=' <<*>> ')

    # Ask the user for card type, max CMC
    check = int(input('What type of cards do you want to add?   '))
    while check not in range(len(typing)) and not isinstance(check, int):
        check = int(input('What type of cards do you want to add?   '))

    mv = int(input('How high do you want the CMC to be? Input a number:   '))
    while not isinstance(mv, int):
        mv = int(input('How high do you want the CMC to be? Input a number:   '))

    deck = []
    # Determine how many of that card type to add to deck.
    amt = int(input('How many do you want to add?   '))
    while 63 - (len(deck) + amt) < 0 or not isinstance(amt, int):  # verifies you can add the cards to your deck
        amt = int(input('<<<<<<ERROR: Invalid value.>>>>>>\nHow many do you want to add?   '))

    finder = typing[check]
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    while len(deck) < amt:
        plus = search_add(cdr, finder, int(mv))
        while plus['name'] in cdr.name():
            print('\nGreat minds think alike \n')
            plus = search_add(cdr, finder, int(mv))
        deck.append(plus)
        bar.update(len(deck))

    return deck


def human_color(card):
    for pip in card.color_identity():
        match pip:
            case 'R':
                print('>>Red<<', end='')
            case 'B':
                print('>>Black<<', end='')
            case 'W':
                print('>>White<<', end='')
            case 'U':
                print('>>Blue<<', end='')
            case 'G':
                print('>>Green<<', end='')
            case _:
                print('>>None')


def identity(card, comm):
    chk = card['color_identity']  # Named object notation
    com = comm.color_identity()
    if len(chk) > len(com):
        return False
    else:
        for color in chk:
            if color not in com:
                return False
    return True


def landfall(counter, deck):
    tot = 0
    for pip in counter:
        tot += counter[pip]
    lands = counter
    for pip in lands:
        lands[pip] = math.ceil(lands[pip] / tot * (99 - len(deck)))
    print(lands)
    return lands


def mana_costs(deck):
    tot = 0
    counter: dict[str, int] = {"W": 0,
                               "U": 0,
                               "B": 0,
                               "R": 0,
                               "G": 0}  # WUBRG
    for i in deck:  # iterates through the deck
        # print(i.get('name'), i.get('mana_cost'))
        check = i.get('mana_cost')  # pulls the mana cost
        for pip in counter:
            if check:
                x = len(re.findall(pip, check))
                if x > 0:
                    counter[pip] += x
            else:
                pass
    for pip in counter:
        tot += counter[pip]
    print(f'Your deck has {tot} pips of mana.\nCalculating mana base~\n')
    return counter

def oracle_txt(cdr):
    txt = "Card Text: "
    prefix = txt + ": "
    pref_width = 70
    wrapper = textwrap.TextWrapper(initial_indent=prefix, width=pref_width,
                                   subsequent_indent=' ' * len(prefix))
    message = cdr.oracle_text()
    print(wrapper.fill(message))
    print('You can use the following colors in your deck:')
    human_color(cdr)
    print('\n')

def page_picker():
    tray = scrython.cards.Search(q='is:commander game:paper').total_cards()
    pages = randint(1, math.ceil(tray / 175))
    return pages


def rand_commander() -> object:  # print random card as Named obj
    num = scrython.cards.Search(page=page_picker(), q='is:commander game:paper -kw:companion -kw:background')
    picked = randint(0, num.data_length() - 1)
    num = num.data(picked, 'name')
    print(num)
    card = scrython.cards.Named(exact=num)
    return card


def search_add(cdr, typed, mv):  # returns a single card as dictionary
    # Determine the color identity for the deck.
    tribe = cdr.color_identity()
    tr = ''
    for i in tribe:
        tr += i.lower()

    # Determine how many cards are returned, and randomize which page you pick from.
    # For simplicity no commanders w background or companion.
    kw = '-kw:companion -kw:background'
    haul = scrython.cards.Search(q='color<=' + tr + ' f:commander t:' + typed.lower() + f' mv<={mv} {kw}')
    p = randint(1,math.ceil(haul.total_cards()/175))
    tray = scrython.cards.Search(page=p,q='color<=' + tr + ' f:commander t:' + typed.lower() + f' mv<={mv} {kw}')

    # Pull a card. If not the commander and color id matches, add it to the deck.
    y = randint(0, tray.data_length() - 1)
    card = tray.data(y)
    while card['name'] in cdr.name() or (not identity(card, cdr)):
        y = randint(0, tray.data_length() - 1)
        card = tray.data(y)
        # print(card['name'])
    return card


def search_com():  # returns a Named obj
    # User enters their search query.
    com = input("Who is your commander?\n====>")

    # Scrython tries to find the card. Creates a list of possible matches.
    card = scrython.cards.Search(q=f'{com} is:commander t:legendary t:creature')

    # Print a list of all the USABLE matches. If len = 1, say that's the commander.
    listed = []
    rnd = 0
    for choice in range(card.data_length()):
        print(f'<--{rnd}--> {card.data(choice, 'name')} ')
        listed.append(choice)
        rnd += 1

    # Prints list if multiple options. Otherwise, will print commander found.
    if len(listed) > 1:
        my = int(input("Please choose a commander from the previous list:\n"))
    else:
        my = 0

    card = card.data(listed[my])  # This variable turns card into a usable dictionary.
    print(f"Your commander is {card['name']} ")
    card = scrython.cards.Named(exact=card['name'])  # Search obj => Named obj
    return card


def dummycard():
    card = scrython.cards.Named(exact='Chatterfang, Squirrel General')
    return card
