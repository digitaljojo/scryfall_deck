import textwrap
import os
import progressbar
import scrython
from random import randint
import math
import re


def produce_mana_type(cdr):  # Returns a string for mana dorks and lands
    col_id = ''
    counter = cdr.color_identity()
    for pip in counter:
        if pip == counter[0]:
            col_id = 'produces:' + pip
        else:
            col_id = col_id + ' or produces:' + pip

    #print(col_id)
    return col_id


def add_basic_lands(counter, deck):  # returns the deck with basic lands added
    for pip in counter:  # Read through how many pips of each color. Add that many lands of that color.
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


def b_wipes(cdr, deck):
    tr = tribe(cdr)
    slots = []
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    haul = scrython.cards.Search(q=f"(o:'exile all' or o:destroy all') id:{tr} f:commander")
    print("\nNow adding board wipes...")
    while len(slots) < 8:
        p = randint(1, math.ceil(haul.total_cards() / 175))
        tray = scrython.cards.Search(page=p,
                                     q=f"(o:'exile all' or o:destroy all') id:{tr} f:commander")
        y = randint(0, tray.data_length() - 1)
        card = tray.data(y)
        while card == cdr or card in deck or card in slots:
            y = randint(0, tray.data_length() - 1)
            card = tray.data(y)
            # print(card['name'])
        slots.append(card)
        #print(card['name'] + '\n')
        bar.update(len(slots))
    deck = deck + slots
    return deck


def card_draw(cdr, deck):
    tr = tribe(cdr)
    slots = []
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    haul = scrython.cards.Search(q=f"f:commander id:{tr} o:draw")
    print('\nNow adding card draw...')
    while len(slots) < 8:
        p = randint(1, math.ceil(haul.total_cards() / 175))
        tray = scrython.cards.Search(page=p,
                                     q=f"f:commander id:{tr} o:draw")
        y = randint(0, tray.data_length() - 1)
        card = tray.data(y)
        while card == cdr or card in deck or card in slots:
            y = randint(0, tray.data_length() - 1)
            card = tray.data(y)
            # print(card['name'])
        slots.append(card)
        #print(card['name'] + '\n')
        bar.update(len(slots))
    deck = deck + slots
    return deck


def deck_base(cdr, deck):
    tr = tribe(cdr)
    slots = []
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    haul = scrython.cards.Search(q=f"f:commander id:{tr} -o:draw -produces:{tr} -o:destroy -o:'opponent sacrifice'")
    print('\nNow adding your random cards:')
    while len(slots) < 29:
        p = randint(1, math.ceil(haul.total_cards() / 175))
        tray = scrython.cards.Search(page=p,
                                     q=f"f:commander id:{tr} -o:draw -produces:{tr} -o:destroy -o:'opponent sacrifice'")
        y = randint(0, tray.data_length() - 1)
        card = tray.data(y)
        while card == cdr or card in deck or card in slots:
            y = randint(0, tray.data_length() - 1)
            card = tray.data(y)
            # print(card['name'])
        slots.append(card)
        #print(card['name'] + '\n')
        bar.update(len(slots))
    deck = deck + slots
    return deck





def file_name():
    counter = 0
    while os.path.isfile(f"/home/jojo/PycharmProjects/scryfall_deck/decklist0{counter}.txt"):
        counter += 1
    named = f"/home/jojo/PycharmProjects/scryfall_deck/decklist0{counter}.txt"
    return named


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


def landfall(counter, deck):
    tot = 0
    for pip in counter:
        tot += counter[pip]
    lands = counter
    for pip in lands:
        lands[pip] = math.ceil(lands[pip] / tot * (89 - len(deck)))
    test = 0
    for pip in lands:
        test += lands[pip]
    '''if test >36:                                                                              
        lands = counter                                                                       
        for pip in lands:                                                                     
            lands[pip] = math.floor(lands[pip] / tot * (98 - len(deck)))  '''
    print(lands)
    return lands


def moar_land(cdr, deck):
    tr = tribe(cdr)
    pro = produce_mana_type(cdr)
    slots = []
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    haul = scrython.cards.Search(q=f"t:land ({pro}) f:commander id:{tr} -t:basic")
    print('\nFinal land addition...')
    while len(deck) + len(slots) < 99:
        p = randint(1, math.ceil(haul.total_cards() / 175))
        tray = scrython.cards.Search(page=p, q=f"t:land ({pro}) f:commander id:{tr} -t:basic")
        y = randint(0, tray.data_length() - 1)
        card = tray.data(y)
        while card == cdr or card in deck or card in slots:
            y = randint(0, tray.data_length() - 1)
            card = tray.data(y)
            # print(card['name'])
        slots.append(card)
        # print(card['name'] + '\n')
        bar.update(len(slots))
    deck = deck + slots

    return deck


def mana_costs(deck):
    tot = 0
    counter: dict[str, int] = {"W": 0,
                               "U": 0,
                               "B": 0,
                               "R": 0,
                               "G": 0}  # WUBRG
    for i in deck:  # iterates through the deck
        # print(i.get('name'), i.get('mana_cost'))
        try:
            check = i['mana_cost']  # pulls the mana cost
        except TypeError:
            print(i)
            check = i.mana_cost()  # pulls the mana cost
        except KeyError:
            try:
                print(i)
                check = i['card_faces'][0]['mana_cost']
            except AttributeError:
                print(i)
                check = i['card_faces'][1]['mana_cost']
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


def mana_dork(cdr, colors, deck):
    tr = tribe(cdr)

    deck.append(scrython.cards.Named(exact='Sol Ring'))
    haul = scrython.cards.Search(q=f'f:commander ({colors}) -t:land id:{tr} m<=4')

    print('\nNow adding mana dorks:')
    # Pull a card. If not the commander and color id matches, add it to the deck.
    slots = []
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    while len(slots) < 13:
        p = randint(1, math.ceil(haul.total_cards() / 175))
        tray = scrython.cards.Search(page=p, q=f'f:commander ({colors}) -t:land id:{tr} m<=4')
        y = randint(0, tray.data_length() - 1)
        card = tray.data(y)
        while card == cdr or card in deck or card in slots:
            y = randint(0, tray.data_length() - 1)
            card = tray.data(y)
            # print(card['name'])
        slots.append(card)
        #print(card['name'])
        bar.update(len(slots))
    deck = deck + slots
    return deck


def oracle_txt(cdr):
    txt = "Card Text: "
    prefix = txt + ": "
    pref_width = 70
    wrapper = textwrap.TextWrapper(initial_indent=prefix, width=pref_width,
                                   subsequent_indent=' ' * len(prefix))
    try:
        message = cdr.oracle_text()
        print(wrapper.fill(message))
    except KeyError or TypeError as err:
        print(cdr.card_faces()[0]['name'])
        message = cdr.card_faces()[0]['oracle_text']
        print(wrapper.fill(message))
        print(cdr.card_faces()[1]['name'])
        message = cdr.card_faces()[1]['oracle_text']
        print(wrapper.fill(message))
    finally:
        print('You can use the following colors in your deck:')
        human_color(cdr)
        print('\n')


def page_picker():
    try:
        tray = scrython.cards.Search(q='is:commander game:paper -kw:companion -kw:background t:creature').total_cards()
        pages = randint(1, math.ceil(tray / 175))
    except scrython.ScryfallError:
        tray = scrython.cards.Search(q='is:commander game:paper -kw:companion -kw:background t:creature').total_cards()
        pages = randint(1, math.ceil(tray / 175))
    return pages


def rand_commander() -> object:  # print random card as Named obj
    num = scrython.cards.Search(page=page_picker(), q='is:commander game:paper -kw:companion -kw:background t:creature')
    picked = randint(0, num.data_length() - 1)
    num = num.data(picked, 'name')
    print(num)
    card = scrython.cards.Named(exact=num)
    return card


def removal(cdr, deck):
    tr = tribe(cdr)
    slots = []
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
    haul = scrython.cards.Search(q=f"(o:'destroy'  or o:'opponent sacrifices' or o:'exile target') id:{tr}")
    print('\nNow adding removal:')
    while len(slots) < 8:
        p = randint(1, math.ceil(haul.total_cards() / 175))
        tray = scrython.cards.Search(page=p,
                                     q=f"(o:'destroy'  or o:'opponent sacrifices' or o:'exile target') id:{tr}")
        y = randint(0, tray.data_length() - 1)
        card = tray.data(y)
        while card == cdr or card in deck or card in slots:
            y = randint(0, tray.data_length() - 1)
            card = tray.data(y)
            # print(card['name'])
        slots.append(card)
        #print(card['name'] + '\n')
        bar.update(len(slots))
    deck = deck + slots
    return deck


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


def tribe(cdr):
    tribe = cdr.color_identity()
    tr = ''
    for i in tribe:
        tr += i.lower()

    return tr
