from random import shuffle

ranks = ('2','3','4','5','6','7','8','9','J','Q','K','A')
suits = ('Spades', 'Diamonds', 'Clubs', 'Hearts')
VALUES = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'J':10, 'Q':10, 'K':10, 'A':11}
playing = True


class Card():

    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck():

    def __init__(self): 
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The Deck has: " + deck_comp

    def shuffle_deck(self):
        shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand():

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += VALUES[card.rank]

        if card.rank == 'A':
            self.aces += 1

    def adjust_for_ace(self): 
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Bank():

    def __init__(self):
        self.total = 500
        self.bet = 0 

    def lose(self, bet):
        self.total -= self.bet

    def win(self, bet):
        self.total += self.bet


def take_bet(bank):
    while True: 

        try:
            bank.bet = int(input("How much do you want to bet? "))
        except:
            print("Please provide a valid input.")
        else:
            if bank.bet > bank.total:
                print("Sorry you don't have enough in your bank to make that bet! You have: {}".format(bank.total))
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input('Hit or Stand? Enter h or s: ')
        
        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("Player Stands - Dealer's Turn")
            playing = False
        
        else:
            print("Sorry I didn't understand that, please enter h or s only! ")
            continue

        break


def show_some(player, dealer):
    print("Dealer's Hand:")
    print(dealer.cards[1])
    print('\n')
    print("Player's Hand:")
    for card in player.cards:
        print(card)


def show_all(player, dealer):
    print("Dealer's Hand:")
    for card in dealer.cards:
        print(card)
    print('\n')
    print("Player's Hand:")
    for card in player.cards:
        print(card)


def player_busts(player, dealer, bank):
    print("Player Busts - Dealer Wins!")
    bank.lose(bank)


def player_wins(player, dealer, bank):
    print("Blackjack! Player Wins!")
    bank.win(bank)


def dealer_busts(player, dealer, bank):
    print("Dealer Busts - Player Wins!")
    bank.win(bank)

def dealer_wins(player, dealer, bank):
    print("Blackjack! Dealer Wins!")
    bank.lose(bank)


def push(player, dealer):
    print('Push - Nobody wins!')



player_bank = Bank()

while True: 

    print("Welcome to Blackjack!")

    deck = Deck()
    deck.shuffle_deck()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    #Prompt player to place a bet
    take_bet(player_bank)

    #Show Cards (Keep one of the dealers cards hidden)
    show_some(player_hand, dealer_hand)

    if player_bank.total <= 0:
        break


    while playing: 
        hit_or_stand(deck, player_hand)

        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_bank)

            break


    if player_hand.value <= 21: 
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        
        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_bank)
        elif dealer_hand.value > player_hand.value: 
            dealer_wins(player_hand, dealer_hand, player_bank)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_bank)
        else:
            push(player_hand, dealer_hand)
        
    print("\n Player total bank is: {}".format(player_bank.total))

    new_game = input("Would you like to play again? Enter y or n: \n")

    if new_game[0].lower() == 'y' and player_bank.total > 0:
        playing = True
        continue
    else:
         print("You're bank is {} thank you for playing.".format(player_bank.total))
         break





    