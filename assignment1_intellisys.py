# work of Timothy Tadj s5178358
import os
import sys
import copy
import time
import queue

class car(): #parameter definitions for each car in problem
    def __init__(self):
        self.isVertical = False #true if car is vertical
        self.isHorizontal = False #true if car is horizontal
        self.size = 0 #size of the car
        self.dimension = [0, 0]
    def properties(self): #prints car properties to screen
        print("Is Vertical" * self.isVertical + "Is Horizontal" * self.isHorizontal)
        print("Size:", self.size)
        print("Location:", self.dimension)

class boardobj(car): #contains the board
    def __init__(self):
        self.board= [["." for i in range(6)] for j in range(6)] # 2d array for board
        self.solution = "" #solution read in from file
        self.cars = {} #all car types with parameters
        self.moves_made = [] #moves made to get to this point

    def stringToBoard(self, str1): #make board and understand cars wihtin it
        #storing board in 2d array
        for i in range(6):
            for j in range(6):
                char1 = str1[i*6+j]       
                self.board[i][j] = char1 #storing board in 2d array
                #define the size of the vehicle
                if char1 in self.cars:
                    pass
                elif char1 != '.':
                    self.cars[char1] = car()

                    if( char1 <= 'M' or char1 == 'X'):
                        self.cars[char1].size = 2
                    else:
                        self.cars[char1].size = 3

        #define the orientation and location of the vehicle
        for key, value in self.cars.items():
            key_done = False
            for i in range(5):
                if key_done:
                    break
                for j in range(5):
                    if key_done:
                        break
                    if (self.board[i][j] == key) and (self.board[i][j+1]  == key):
                        self.cars[key].isHorizontal = True
                        self.cars[key].dimension = [i,j] #define location
                        key_done = True
                    elif(self.board[i][j]== key) and (self.board[i+1][j]== key):
                        self.cars[key].isVertical = True
                        self.cars[key].dimension = [i,j] #define location
                        key_done=True
            for i in range(5):
                if key_done:
                    break
                if(self.board[i][5]== key) and (self.board[i+1][5]== key):
                    self.cars[key].isVertical = True
                    self.cars[key].dimension = [i,5] #define location
                    key_done=True
            for j in range(5):
                if key_done:
                    break
                if (self.board[5][j] == key) and (self.board[5][j+1]  == key):
                        self.cars[key].isHorizontal = True
                        self.cars[key].dimension = [5,j] #define location
                        key_done=True
        return self

    def stringToSolution(self, str1): #assign string to solution var
        self.solution = str1
        return self

    def printBoard(self): #print board of current problem        
        print("    1 2 3 4 5 6 ")
        print("  +-------------+")
        for i in range(6):
            print(i+1, "|", end = " ")
            for j in range(6):
                print(self.board[i][j], end = " ")
            if i == 2:
                print("  ==>")
            else:
                print("|")

        print("  +-------------+")
        print("    a b c d e f ")

    def win(self): #function to detect a win

        return(self.board[2][5] == 'X')

    def move(self, mov): #function to do a move based on mov instruction string and returns a new board
        boardOut = copy.deepcopy(self)
        if mov in boardOut.expand(): #if move is possible do the move
            v_domain = boardOut.cars[mov[0]].dimension[0]
            h_domain = boardOut.cars[mov[0]].dimension[1]
            size = boardOut.cars[mov[0]].size
            if mov[1] == 'U': #move up
                boardOut.board[v_domain-1][h_domain] = mov[0]
                boardOut.board[v_domain+size-1][h_domain] = '.'
                boardOut.cars[mov[0]].dimension = [v_domain-1, h_domain] #update location of car
            elif mov[1] == 'D': # move down
                boardOut.board[v_domain+size][h_domain] = mov[0]
                boardOut.board[v_domain][h_domain] = '.'
                boardOut.cars[mov[0]].dimension = [v_domain+1, h_domain] #update location of car
            elif mov[1] == 'L': #move left
                boardOut.board[v_domain][h_domain-1] = mov[0]
                boardOut.board[v_domain][h_domain+size-1] = '.'
                boardOut.cars[mov[0]].dimension = [v_domain, h_domain-1] #update location of car
            elif mov[1] == 'R': # move right
                boardOut.board[v_domain][h_domain+size] = mov[0]
                boardOut.board[v_domain][h_domain] = '.'
                boardOut.cars[mov[0]].dimension = [v_domain, h_domain+1] #update location of car
        else: #if move is not possible
            print("WARNING: cannot do move!")
        return boardOut

    def make_moves(self, moves): #performs moves based on a list of move instructions
        boardOut = copy.deepcopy(self)
        for i in moves:
            if len(i) > 2: #if multiple of same move instructions
                multiple_move = int(i[2])
                i_multiple = i[:-1]
                for j in range(multiple_move):
                    self.move(boardOut, i_multiple)
            else:
                self.move(boardOut, i) #if not multiple of same instruction
        return boardOut

    def expand(self): 
        moves = []
        for key, car in self.cars.items():
            
            #look for move at head of car
            h_domain = car.dimension[0] - car.isVertical
            v_domain = car.dimension[1] - car.isHorizontal
            if(h_domain >= 0 and v_domain >=0):
                if (self.board[h_domain][v_domain] == '.'): #check position before head of car
                    move = ""
                    move += key + car.isVertical * 'U' + car.isHorizontal * 'L' #make move symbol
                    moves.append(move) #add to list
            
            #loof for move at tail of car
            h_domain = car.dimension[0] + (car.isVertical * car.size)
            v_domain = car.dimension[1] + (car.isHorizontal * car.size)
            if(h_domain < 6 and v_domain < 6):
                if (self.board[h_domain][v_domain] == '.'):
                    move = ""
                    move += key + car.isVertical * 'D' + car.isHorizontal * 'R' #make move symbol
                    moves.append(move)  #add to list
        return moves

    def nextstates(self):
        next_states = []
        moves = self.expand()
        for i in moves: #uses moves found to make a list of boards
            temp_board = copy.deepcopy(self) #use tempboard to append to list of boards
            temp_board = temp_board.move(i)  #apply a move
            temp_board.moves_made.append(i) #keep track of move
            next_states.append(temp_board) #append to list of boards
        return next_states

class Game(boardobj): #stores all game boards
    def __init__(self):
        self.boards = {} #contains all problems

        file = open(os.path.join(sys.path[0], "rh.txt"), "r")
        i =1
        check = False

        #add the board string to object in the dictionary that stores it as a 2d array
        for line in file: #read file
            boardTemp = boardobj()

            if line.startswith("--- RH-input ---"):
                check=True
            elif line.startswith("--- end RH-input ---"):
                break
            elif check:
                self.boards[i] = boardTemp.stringToBoard(line.rstrip())
                i+=1
            
        #add the solution to a string in the same object 
        for i in range(1, 41):
            problemString = "  Problem "
            problemString += str(i)
            problemString += " "
            check2 = False
            
            solutionTemp = ""

            for line in file: #continue reading file
                if line.startswith(problemString):
                    check2 = True #set check to true so that next line will be saved
                elif check2 == True:
                    if(line.startswith("  Sol:")):
                        solutionTemp+= line.replace("  Sol: ", "").rstrip()

                        if solutionTemp.find('.')!= -1: #condition if solution is one line long
                            check2 = False
                            break
                        else: #condition if solution is more than one line long
                            x =file.read(1)
                            while x != ".":  
                                solutionTemp+=x
                                solutionTemp=solutionTemp.replace("      ", "").replace("\n", "").replace("  ", " ") #formatting string
                                x = file.read(1)
                            break
            solutionTemp = solutionTemp.replace(".", "") #formatting string
            TempBoard = self.boards[i] #make copy of stored object
            TempBoard.stringToSolution(solutionTemp) #make changes 
            self.boards[i] = TempBoard #store copy in origional      
        
        file.close()

def BFS(initial_board):
    BFSqueue = queue.Queue()
    current_state  = initial_board
    discovered = [current_state]
    total = 0
    while current_state.win() != True:
        temp_nextstates = current_state.nextstates()
        for next_state in temp_nextstates:
            if next_state.board not in discovered:
                BFSqueue.put(next_state)
        total +=1
        current_state = BFSqueue.get()
        # print(total)
        discovered.append(current_state.board)

    return current_state

def Iterative_d(initial_board):
    pass

game = Game()
game.boards[40].printBoard()
x = BFS(game.boards[40])
x.printBoard()

# for i in range(1, 41):
#     #prints initial board and proposed solutions
#     print("\n  Problem", i, ":")
#     game.boards[i].printBoard()

# #new state example
#     print("Possible Moves:")
#     print(game.boards[i].expand(), "\n")
#     print("New state example:")
#     print("Possible states:", game.boards[1].expand())
#     new_board = game.boards[1].move(game.boards[1].expand()[0]) #create a new state with the first posiible move in problem 1
#     new_board.printBoard()
#     new_board.cars['A'].properties()#prints properties of car 'A' in new board

# move(game.boards[1], 'QD')



#class inheritance structure
#game.boards[problem_No].board
#game.boards[problem_No].solution
#game.boards[problem_No].cars[car_letter].car_property