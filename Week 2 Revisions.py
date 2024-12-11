import random
import math

first_time=0

'''
Update Notes [8.21.2024] (by Lanz):
- added math module
- added find_factors method
- added is_perfect_square method

Update Notes [8.22.2024] (by Lanz):
- FINALLY implemented the new render
- still havent implemented the row and column labelling
-definitely should thoooo
'''
      
def find_factors(number):
    factors = set()
    for i in range(1, int(math.sqrt(number)) + 1):
        if number % i == 0:
            factors.add(i)
            factors.add(number // i)
    return sorted(factors)

def is_perfect_square(n):
    if n < 0:
        return False
    i = 0
    while i * i <= n:
        if i * i == n:
            return True
        i += 1
    return False

class Card:
    def __init__(self, symbol):
        self.symbol = symbol
        self.row =""
        self.is_matched = False
        self.is_shown = False

    def reveal(self):
        return self.symbol if self.is_matched or self.is_shown else "?"

    def tempreveal(self): #edited by Justine. Renamed from hide(self) because it was unused anyway. Converted it to a second reveal method that just temporarily reveals the symbol of a card.
        #return "*" if not self.is_matched else self.symbol
        self.is_shown = True

class GameBoard:
    def __init__(self,card_count):
        self._card_count = card_count
        self._grid_of_cards = self._setup_board()
        self.row_count = ""
        self.column_count = ""

    def _setup_board(self):  
        symbols = [chr(i) for i in range(65, 65 + (self._card_count) // 2)]
        symbols *= 2 #tried retyping by Anne
        random.shuffle(symbols)
        card_factors=(find_factors(len(symbols)))
        middle=(len(card_factors)//2)
        if is_perfect_square(len(symbols))==False:
            self.row_count=card_factors[middle]
            self.column_count=card_factors[middle-1]
        else:
            self.row_count=card_factors[middle]
            self.column_count=card_factors[middle]
        if self.column_count>self.row_count:
            column_count,row_count=row_count,column_count
        print(f'Cards printed:{self._card_count}\nRow:{self.row_count} Column:{self.column_count}\n---')
        
        board = []
        append_count=0
        for i in range(self.column_count):
            row = []
            for j in range(self.row_count):
                row.append(Card(symbols[append_count]))
                append_count+=1
            board.append(row)
        return board


    def display(self):                      #Added by Kevin. This is to show the current state of the board.
        board_display=[]
        for row in self._grid_of_cards:
            print(' '.join('+-+' for card in row))
            print(' '.join(f'|{card.reveal()}|' for card in row))
            print(' '.join('+-+' for card in row))
        
class MemoryGame:
    def __init__(self):                     #Changed by Kevin. Removed "moves_counter" and "matched_pairs" since they're unused parameters.
        self.game_board = GameBoard(request)
        self.moves_counter = 0
        self.matched_pairs = []

    def flip_card(self, row, col):
        card = self.game_board._grid_of_cards[row-1][col-1] #edited by Justine. Added a "-1" for both row and column values. Without this decrement, the first row and column will be numbered ZERO, which is confusing for the player.
        if row==0 or col==0: raise ValueError #introduced by Justine. Row/column values cannot be zero because they are numbered 1 to 6.
        card.tempreveal()
#update board command removed
        return card

    def check_match(self, first_card, second_card):
        if first_card.symbol == second_card.symbol:
            first_card.is_matched = True
            second_card.is_matched = True
            self.matched_pairs.append((first_card, second_card))
            return True
        return False
   
    def hide_cards(self, first_card, second_card):
        if first_card.is_matched == False: first_card.is_shown = False
        if first_card.is_matched == False: second_card.is_shown = False

    def update_board(self):
        self.game_board.display()

    def display_end_game_message(self):
        print(f'Congratulations! Moves spent: {self.moves_counter}')

    def play(self):
        print("INSTRUCTIONS:\nEnter the coordinates of two cards and see if they match! The game ends when all cards are matched correctly.") #added by Justine
        print("Please observe this format when inputting card coordinates: <row> <col>.") #added by Justine
        self.update_board()
        print("\n(Example: Input '3 1' for the card on the third row, first column.)\n") #added by Justine
        while len(self.matched_pairs) < self.game_board._card_count//2:



            try:
                if first_time==1:    
                    print("\n\n\n\n\n\n\n\n")
                else:
                    first_time==1
                print(f'Moves: {self.moves_counter}')
                row1, col1 = map(int, input("Enter the coordinates of the first card: ").split()) #edited by Justine
                first_card = self.flip_card(row1, col1)
                print("\n\n\n\n\n\n\n\n")
                self.update_board()
                print("\n\n\n\n\n\n\n\n")
                print(f'Moves: {self.moves_counter}')   
                row2, col2 = map(int, input("Enter the coordinates of the second card: ").split()) #edited by Justine
                second_card = self.flip_card(row2, col2)
                print("\n\n\n\n\n\n\n\n")
                if row1==row2 and col1==col2: #introduced by Justine. Prevents cases where a player picks the same card twice and causes it to match by itself.
                    print("You chose the same card twice! Try again.")
                elif not self.check_match(first_card, second_card): #edited by Justine
                    print("No match. Try again.")
                else:
                    print("Match!")
                self.update_board()
                self.hide_cards(first_card, second_card)
                self.moves_counter+=1
                
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid row and column numbers.")
                print("\n\n\n\n\n\n\n\n")
        self.display_end_game_message()

if __name__ == "__main__":  #Added by Kevin. This is to run the game.
    request=int(input(f'---\nCards requested:'))
    if request<2:
        request=2
    if request>52:
        request=52
    game = MemoryGame()
    game.play()
