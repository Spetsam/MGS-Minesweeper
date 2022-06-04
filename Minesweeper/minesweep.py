import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board= self.make_new_board()
        self.assign_values_to_board() #Function initialization
        self.dug = set()

    
    def assign_values_to_board (self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)
    

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1): #Below and above, right and left, based on current collumn
                if r == row and c == col:
                    continue #This is our original location, no need to check this
                if self.board[r][c] == '*':
                    num_neighboring_bombs+=1
        return num_neighboring_bombs


    
    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)] #If logic doesn't work, contact @Spetsam

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*': #Bomb has been planted here already
                continue

            board[row][col] = '*' #Planting the bomb
            bombs_planted+=1
        return board

    def dig(self, row, col):
        self.dug.add((row, col)) #Adding a Tuple
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r,c) in self.dug:
                    continue #Skip the digging where the digging was already done
                self.dig(r,c)

        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' ' #We can later put this entire representation into a string


def play(dim_size= 10, num_bombs = 10): #Formatting code addition skipped, focused on functionality
    
    board = Board(dim_size,num_bombs)

    safe = True

    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)
        user_input = re.split(', (\\s)*', input("Where would you like to dig? Input row and collumn: ")) #Regex string split can be used
        row, col = int(user_input[0]), int(user_input[-1]) #Declaring them as integers
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid.")
            continue
        safe = board.dig(row, col)
        if not safe:
            break #Game over

    if safe: #Checking all exits
        print("Congratulations! You won!")
    else:
        print("Sorry, game over!")

        board.dug[(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print (board)

if __name__ == '__main__':
    play() #Playing the game