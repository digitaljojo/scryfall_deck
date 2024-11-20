#!usr/bin/env python3
"""
 MTG Commander Deck Generator Application | Jonathan Johnny
"""
import scrython

import testmethods as tm


def main():
    # Get your commander
    ans = input('Welcome to the Jajanken Deck Builder!\nDo you know your commander?   y/n:  ')
    good = ['y', 'n', 'yes', 'no', '']
    while ans.lower() not in good:
        ans = input('Do you know your commander?   y/n:  ')

    if ans in ['y', 'yes']:
        try:
            cdr = tm.search_com()
        except scrython.ScryfallError:
            print('You must hav made a typo.')
            cdr = tm.search_com()
    elif ans in ['n', 'no']:
        cdr = tm.rand_commander()
    else:
        print('We can play another time. Goodbye~!\n...\nNah, lemme find you a commander!')
        cdr = tm.rand_commander()
    tm.oracle_txt(cdr)

    # Generate a blank deck list.

    full_deck = []

    # Add cards to the deck until deck has 63 cards
    typing = ['Creature', 'Enchantment', 'Artifact', 'Instant', 'Sorcery', 'Planeswalker', 'Land']
    print('You will be adding 63 cards.\n')

    for c_type in typing:
        print(f'Now adding "{c_type}s"')
        dlen = len(full_deck)
        full_deck = full_deck + (tm.fill(cdr, c_type, dlen))
        print('\nCurrently, you have ' + str(len(full_deck)) + ' cards in your deck.')
        print('You have ' + str(63 - len(full_deck)) + ' card slots available!')

    # Mana addition.  Deck = Add basic lands(Count lands needed (Count pips in deck, deck), deck)
    full_deck = tm.add_basic_lands(tm.landfall(tm.mana_costs(full_deck), full_deck), full_deck)

    # Output the list
    print(f'Printing out your {len(full_deck)} card deck list!\n')
    with open('../decklist.txt', 'w') as decklist:
        decklist.write(f'{cdr.name()}: {cdr.type_line()}, {cdr.mana_cost()}\n')
        for i in full_deck:
            try:
                decklist.write(i.name() + '\n')
            except AttributeError:
                decklist.write(i['name'] +'\n')


main()
