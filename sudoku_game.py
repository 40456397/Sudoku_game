#import libraries
import numpy as np
import random
import time

#print a board with borders to allow the player to easily identify the various 3x3 boxes
def print_board(board):
    for r in range(9):
        for c in range(9):
            if c==0:
                print("|",end='')
            if c!=8:
                print(board[r,c],end=' ')
            else:
                print(board[r,c],end='')
            if (c+1)%3==0:
                print("|",end='')
        if (r+1)%3==0:
            print("\n---------------------",end='')
        print()

#check if the number at a given position in the puzzle is valid, based on the game rules
#rules are only 1 instance of each number in each row, column and 3x3 box
def check_if_valid(board,row,col,num):
    start_row=(row//3)*3
    start_col=(col//3)*3
    if num in board[:,col] or num in board[row,:]:
        return False
    if num in board[start_row:start_row+3,start_col:start_col+3]:
        return False
    return True
    
#look for empty cells
def find_empty_cell(board):
    for r in range(9):
        for c in range(9):
            if board[r,c]==0:
                row=r
                col=c
                check_filled=1
                res=np.array([row,col,check_filled],dtype="int8")
                return res
    res=np.array([-1,-1,0])
    return res

#produce a Sudoku board with numbers missing, based on the difficulty level entered by the player
def produce_puzzle(board,diff_choice):
    count,done=0,False
    if diff_choice==1:
        print("Generating an easy-level Sudoku puzzle\n")
        upper_limit=35
    elif diff_choice==2:
        print("Generating a medium-level Sudoku puzzle\n")
        upper_limit=41
    else:
        print("Generating a hard-level Sudoku puzzle\n")
        upper_limit=47
    while True:   
        r=random.randint(0,8)
        c=random.randint(0,8)
        if count<=upper_limit:
            if board[r,c]!=0:
                not_check=board[r,c]
                board[r,c]=0
                board_copy=board
                if solve_puzzle(board_copy,not_check):
                    board[r,c]=not_check
                    continue
                start_row=(r//3)*3
                start_col=(c//3)*3
                if diff_choice==1:
                    if np.count_nonzero(board[start_row:start_row+3,start_col:start_col+3])<5:
                        board[r,c]=not_check
                        continue
                elif diff_choice==2:
                    if np.count_nonzero(board[start_row:start_row+3,start_col:start_col+3])<4:
                        board[r,c]=not_check
                        continue
                else:
                    if np.count_nonzero(board[start_row:start_row+3,start_col:start_col+3])<3:
                        board[r,c]=not_check
                        continue
                count+=1
        else:
            done=True
            break

#this function is the main gameplay function
#the player is asked if they wish to guess, undo the previous guess, or quit the game
#if the player guesses, it asks for the row, column and value for their guess
#the row, column and value from the guess are added to lists for undoing if required
#next a function is called to check if their guess is correct
#if the guess is correct, the puzzle is updated appropriately
#there is a timer which collects the start and end time of gameplay and informs the user
#of the time played when the board is complete or the player quits the game
def play_game(complete_board,incomplete_board):
    rows=[]
    columns=[]
    guesses=[]
    start_time = time.time()
    correct_guesses=0
    incorrect_guesses=0
    
    while True:    
        guess=int(input("Enter your guess (or enter 88 to undo last correct guess or 99 to quit):"))
        if guess==99:
            print("\nThank you for playing. The completed board is:\n")
            print_board(complete_board)
            end_time = time.time()
            elapsed = end_time - start_time
            print("You played this puzzle for {:.0f} seconds.".format(elapsed))
            print("You had {} correct and {} incorrect guesses.".format(correct_guesses,incorrect_guesses))
            return
        elif guess==88:
            prev_row = rows[-1]
            prev_col = columns[-1]
            prev_guess = guesses[-1]
            
            print("Your previous guess of {:.0f}, in row {:.0f} and column {:.0f} has been undone.".format(prev_guess,prev_row+1,prev_col+1))
            interim_time = time.time()
            current_time = interim_time - start_time
            print("You have been playing this puzzle for {:.0f} seconds.".format(current_time))   
            incomplete_board[prev_row,prev_col]=0
            print_board(incomplete_board)
            rows.pop()
            columns.pop()
            guesses.pop()
            correct_guesses-=1
        else:
            row=int(input("Please enter the row number for your guess:")) - 1
            col=int(input("Please enter the column number for your guess:")) - 1
              
            if incomplete_board[row,col]==0:
                print(complete_board[row,col])
                if complete_board[row,col]==guess:
                    print("Your guess was correct. Here is the updated board:\n")
                    interim_time = time.time()
                    current_time = interim_time - start_time
                    print("You have been playing this puzzle for {:.0f} seconds.\n".format(current_time))                   
                    incomplete_board[row,col]=guess
                    print_board(incomplete_board)
                    
                    #append correct guess information to lists for undoing later if needed
                    rows.append(row)
                    columns.append(col)
                    guesses.append(guess)
                    correct_guesses+=1
                else:
                    print("Your guess was incorrect. The board currently looks like this:\n")
                    interim_time = time.time()
                    current_time = interim_time - start_time
                    print("You have been playing this puzzle for {:.0f} seconds.\n".format(current_time))   
                    print_board(incomplete_board)
                    incorrect_guesses+=1
            else:
                print("That row and column is already filled.\n")
                interim_time = time.time()
                current_time = interim_time - start_time
                print("You have been playing this puzzle for {:.0f} seconds.\n".format(current_time))   
            if np.array_equal(complete_board,incomplete_board):
                print("Well done! You have solved the Sudoku puzzle.")
                end_time = time.time()
                elapsed = end_time - start_time
                print("You took {:.0f} seconds to solve the puzzle.".format(elapsed))
                print("You had {} correct and {} incorrect guesses.".format(correct_guesses,incorrect_guesses))
                break

#this function is used to solve the puzzle, by generating a solution and using a backtracking algorithm
def solve_puzzle(board,not_check):
    x=find_empty_cell(board)
    if x[2]==0:
        return True
    else:
        row=x[0]
        col=x[1]
        for i in np.random.permutation(10):
            if i!=0 and i!=not_check:
                if check_if_valid(board,row,col,i):
                    board[row,col]=i
                    if solve_puzzle(board,not_check):
                        return True
                    board[row,col]=0 
    return False

#the main function starts the game, allows the player to choose the difficulty level and produces the board
def main():
    diff_choice=int(input("Thanks for playing Sudoku. Please choose the level of difficulty.\n1. Easy\n2. Medium\n3. Hard\n\nYour choice:"))

    board=np.zeros((9,9),dtype="int8")
    if solve_puzzle(board,-1):
        complete_board=board.copy()
        produce_puzzle(board,diff_choice)
        print("\nThe incomplete board looks like this:\n")
        print_board(board)
        incomplete_board=board.copy()
        play_game(complete_board,incomplete_board)
    else:
        print("It's not possible to solve this board")
    return

if __name__=="__main__":
    main()
