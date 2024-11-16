#!usr/bin/env python3
"""
 MTG Commander Deck Generator Application | Jonathan Johnny
"""
import testmethods as tm


def main():
    # Get your commander
    ans = input('Welcome to the Jajanken Deck Builder!\nDo you know your commander?   y/n:  ')
    good = ['y', 'n', 'yes', 'no', '']
    while ans.lower() not in good:
        ans = input('Do you know your commander?   y/n:  ')

    if ans in ['y', 'yes']:
        cdr = tm.search_com()
    elif ans in ['n', 'no']:
        cdr = tm.rand_commander()
    else:
        print('We can play another time. Goodbye~!\n...\nNah, lemme find you a commander!')
        cdr = tm.rand_commander()
    tm.oracle_txt(cdr)

    # Generate a blank deck list.
    mlem = 63
    full_deck = []
    # Add cards to the deck until deck has 99 cards
    while len(full_deck) < mlem:
        full_deck = full_deck + tm.fill(cdr)

        # Verifies if any cards were added.
        print('\nCurrently, you have ' + str(len(full_deck)) + ' cards in your deck.')

        # Verifies no duplicates in the deck bc of dual type cards
        unique_list = []
        for o in full_deck:
            if o not in unique_list:
                unique_list.append(o)

        if len(full_deck) > len(unique_list):
            full_deck = unique_list
            print('Duplicates removed! \nYou have ' + str(mlem - len(full_deck)) + ' card slots available!')
        else:
            print('\n You have ' + str(mlem - len(full_deck)) + ' card slots available!')

    # Mana addition.  Deck = Add basic lands(Count lands needed (Count pips in deck, deck), deck)
    full_deck = tm.add_basic_lands(tm.landfall(tm.mana_costs(full_deck), full_deck), full_deck)

    # Output the list
    print(f'Printing out your {len(full_deck)} card deck list!\n')
    with open('decklist.txt', 'w') as decklist:
        decklist.write(f'{cdr.name()}: {cdr.type_line()}, {cdr.mana_cost()}\n')
        for i in full_deck:
            try:
                decklist.write(i.name() + ': ' + i.type_line() + ':  ' + '\n')
            except AttributeError:
                decklist.write(i['name'] + ': ' + i['type_line'] + ':  ' + '\n')


main()
