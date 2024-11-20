import calling_cards as c
import scrython


def main():
    # Get your commander
    ans = input('Welcome to the Jajanken Deck Builder!\nDo you know your commander?   y/n:  ')
    good = ['y', 'n', 'yes', 'no', '']
    while ans.lower() not in good:
        ans = input('Do you know your commander?   y/n:  ')
    # If yes, searches for commander. Returns a list.
    if ans in ['y', 'yes']:
        try:
            cdr = c.search_com()
        except scrython.ScryfallError:
            print('You must have made a typo.')
            cdr = c.search_com()
    elif ans in ['n', 'no']:
        cdr = c.rand_commander()
    else:
        print('We can play another time. Goodbye~!\n...\nNah, lemme find you a commander!')
        cdr = c.rand_commander()
    c.oracle_txt(cdr)

    # Generate a blank deck list.

    full_deck = []

    #  Determines identity. Fills the list.
    colors = c.produce_mana_type(cdr)
    full_deck = c.mana_dork(cdr, colors, full_deck)
    full_deck = c.deck_base(cdr, full_deck)
    full_deck = c.card_draw(cdr, full_deck)
    full_deck = c.b_wipes(cdr, full_deck)
    full_deck = c.removal(cdr, full_deck)

    # Determines required amount for proper mana distribution and fills the deck with land.
    counter = c.mana_costs(full_deck)
    lands = c.landfall(counter, full_deck)
    full_deck = c.add_basic_lands(lands, full_deck)
    full_deck = c.moar_land(cdr, full_deck)

    # Output the list
    print(f"\nPrinting out your {len(full_deck)+1} card deck list!")
    with open(c.file_name(), 'w') as decklist:
        try:
            decklist.write(f'{cdr.name()}: {cdr.type_line()}, {cdr.mana_cost()}\n')
        except:  # Takes into account the flip cards
            decklist.write(f'{cdr.name()}: {cdr.type_line()}, {cdr.card_faces()[0]['mana_cost']}\n')

        for i in full_deck:
            try:
                decklist.write(i.name() + '\n')
            except AttributeError:
                decklist.write(i['name'] + '\n')


main()
