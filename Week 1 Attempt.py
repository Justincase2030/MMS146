import random

class Card:
    def __init__(self, symbol):
        self.symbol = symbol
        self.is_matched = False

    def reveal(self):
        return self.symbol if self.is_matched else "*"

    def tempreveal(self): #edited by Justine. Renamed from hide(self) because it was unused anyway. Converted it to a second reveal method that just temporarily reveals the symbol of a card.
        #return "*" if not self.is_matched else self.symbol
        return self.symbol

class GameBoard:
    def __init__(self, board_size=6):
        self._board_size = board_size
        self._grid_of_cards = self._setup_board()

    def _setup_board(self):
        symbols = [chr(i) for i in range(65, 65 + (self._board_size * self._board_size) // 2)]
        symbols *= 2 #tried retyping by Anne
        random.shuffle(symbols)

        board = []
        for i in range(self._board_size):
            row = []
            for j in range(self._board_size):
                row.append(Card(symbols.pop()))
            board.append(row)
        return board

    def display(self):                      #Added by Kevin. This is to show the current state of the board.
        for row in self._grid_of_cards:
            print(" ".join(card.reveal() for card in row))

class MemoryGame:
    def __init__(self):                     #Changed by Kevin. Removed "moves_counter" and "matched_pairs" since they're unused parameters.
        self.game_board = GameBoard()
        self.moves_counter = 0
        self.matched_pairs = []

    def flip_card(self, row, col):
        card = self.game_board._grid_of_cards[row-1][col-1] #edited by Justine. Added a "-1" for both row and column values. Without this decrement, the first row and column will be numbered ZERO, which is confusing for the player.
        if row==0 or col==0: raise ValueError #introduced by Justine. Row/column values cannot be zero because they are numbered 1 to 6.
        print (f"Card at ({row}, {col}) : {card.tempreveal()}") #edited by Justine. This will now temporarily reveal the symbol and give players an idea of what the card they flipped is.
        return card

    def check_match(self, first_card, second_card):
        if first_card.symbol == second_card.symbol:
            first_card.is_matched = True
            second_card.is_matched = True
            self.matched_pairs.append((first_card, second_card))
            return True
        return False

    def update_board(self):
        self.game_board.display()

    def display_end_game_message(self):
        print("Congratulations!")

    def play(self):
        print("INSTRUCTIONS: Enter the coordinates of two cards and see if they match! The game ends when all cards are matched correctly.") #added by Justine
        print("Please observe this format when inputting card coordinates: <row> <col>. Rows and columns are numbered 1 (first) to 6 (sixth).") #added by Justine
        print("Example: Input '3 1' for the card on the third row, first column.") #added by Justine
        while len(self.matched_pairs) < (self.game_board._board_size * self.game_board._board_size) // 2:
            self.update_board()
            try:
                row1, col1 = map(int, input("Enter the coordinates of the first card: ").split()) #edited by Justine
                first_card = self.flip_card(row1, col1)

                row2, col2 = map(int, input("Enter the coordinates of the second card: ").split()) #edited by Justine
                second_card = self.flip_card(row2, col2)

                self.moves_counter += 1

                if row1==row2 and col1==col2: #introduced by Justine. Prevents cases where a player picks the same card twice and causes it to match by itself.
                    print("You chose the same card twice! Try again.")
                elif not self.check_match(first_card, second_card): #edited by Justine
                    print("No match. Try again.")
                else:
                    print("Match!")
                      
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid row and column numbers.")
        
        self.update_board()
        self.display_end_game_message()

if __name__ == "__main__":  #Added by Kevin. This is to run the game.
    game = MemoryGame()
    game.play()

#Changed by Arianna. Removed the last line: MemoryGame.display_end_game_message() because display_end_game_message() is an instance method, not a class method. 
