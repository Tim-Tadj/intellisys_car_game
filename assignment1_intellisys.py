# work of Timothy Tadj s5178358
import os
import sys
import copy
import time
import multiprocessing
import random
import queue
from itertools import count

checked_cars = set()

class Timeout(Exception):
    pass

def handler(sig, frame):
    raise Timeout

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
        self.stringboard =""

    def stringToBoard(self, str1): #make board and understand cars wihtin it
        #storing board in 2d array
        self.stringboard=str1
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
    
    def boardToString(self):
        result = ""
        for i in self.board:
            for j in i:
                result += j
        return result

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

    def expand(self): 
        next_states = []
        for key, car in self.cars.items():
            if self.moves_made:
                if self.moves_made[-1][-3] == key:
                    continue
            
            #look for move at head of car
            boarder = car.dimension[car.isHorizontal]+1
            for i in range(1, boarder):
                h_domain = car.dimension[0] - car.isVertical * i
                v_domain = car.dimension[1] - car.isHorizontal * i
                if(h_domain >= 0 and v_domain >=0):
                    if (self.board[h_domain][v_domain] == '.'): #check position before head of car
                        move = ""
                        movNum = i
                        move += key + car.isVertical * 'U' + car.isHorizontal * 'L' + str(movNum)#make move symbol
                        temp_board = copy.deepcopy(self) #use tempboard to append to list of boards
                        temp_board.moves_made.append(move) #keep track of move
                        for j in range(car.size):
                            temp_board.board[car.dimension[0] + (car.isVertical * j)][car.dimension[1] + (car.isHorizontal * j)] = "."
                            
                        for j in range(car.size):
                            temp_board.board[car.dimension[0] - (car.isVertical * (movNum - j))][car.dimension[1] - (car.isHorizontal * (movNum - j))] = key
                        temp_board.cars[key].dimension = [car.dimension[0]-movNum*car.isVertical, car.dimension[1]-movNum*car.isHorizontal]
                        temp_board.stringboard = temp_board.boardToString()
                        next_states.append(temp_board) #append to list of boards
                    else:
                        break
            
            #look for move at tail of car
            boarder = (7 - car.dimension[car.isHorizontal] - car.size)
            for i in range(1, boarder):
                h_domain = car.dimension[0] + (car.isVertical * (car.size + i -1))
                v_domain = car.dimension[1] + (car.isHorizontal * (car.size + i -1))
                if(h_domain < 6 and v_domain < 6):
                    if (self.board[h_domain][v_domain] == '.'):
                        move = ""
                        movNum = i
                        move += key + car.isVertical * 'D' + car.isHorizontal * 'R' + str(movNum)#make move symbol
                        temp_board = copy.deepcopy(self) #use tempboard to append to list of boards
                        temp_board.moves_made.append(move) #keep track of move
                        for j in range(car.size):
                            temp_board.board[car.dimension[0] + (car.isVertical * j)][car.dimension[1] + (car.isHorizontal * j)] = "."
                        
                        for j in range(car.size):
                            temp_board.board[car.dimension[0] + (car.isVertical * (movNum + j))][car.dimension[1] + (car.isHorizontal * (movNum + j))] = key
                        temp_board.cars[key].dimension = [car.dimension[0]+movNum*car.isVertical, car.dimension[1]+movNum*car.isHorizontal]
                        temp_board.stringboard = temp_board.boardToString()
                        next_states.append(temp_board) #append to list of boards
                    else:
                        break
        return next_states
    def Blocked_val(self, car_char):
        
        global checked_cars # needs to be global as having recursion effect this would ruin our solution
        current_car_obj = self.cars.get(car_char)
        # print(car_char)
        # current_car_obj.properties()
        v_val = current_car_obj.dimension[0]
        h_val = current_car_obj.dimension[1]
        num = 0 #our heuristic val of the state
        if current_car_obj.size == 3 and current_car_obj.isVertical: # for vertical car of size 3
            
            for i in range(v_val+3, 6): #for tail 
                if self.board[i][h_val] != '.' : # check if piece is a car
                    num+=1
                    if  self.board[i][h_val] not in checked_cars:
                        checked_cars.add(self.board[i][h_val]) # if not in checked cars add to checked cars
                        num+=self.Blocked_val(self.board[i][h_val]) #recursivly add to our heuristic val the heuristic val of the block
            if h_val > self.cars['X'].dimension[1]: #return if it isnt front of x as it can only go down 
                return num
            for i in range(v_val-1, -1, -1): #for head
                if self.board[i][h_val] != '.' :
                    num+=1
                    if  self.board[i][h_val] not in checked_cars:
                        checked_cars.add(self.board[i][h_val]) 
                        num+=self.Blocked_val(self.board[i][h_val])

        elif current_car_obj.size == 3 and current_car_obj.isHorizontal: # for horizontal car of size 3 #needs fix
            if h_val > 2: # has to move left if its on the right hand side of the board
                for i in range(h_val-1, -1, -1): #head
                    if self.board[v_val][i] != '.' :
                        num+=1
                        if  self.board[v_val][i] not in checked_cars:
                            checked_cars.add(self.board[v_val][i])
                            num+=self.Blocked_val(self.board[v_val][i])
            else: # has to move right if its on the left hand side of the board
                for i in range(h_val+3, 6): #tail
                    if self.board[v_val][i] != '.' :
                        num+=1
                        if  self.board[v_val][h_val] not in checked_cars:
                            checked_cars.add(self.board[v_val][i])
                            num+=self.Blocked_val(self.board[v_val][i])
        elif current_car_obj.isVertical: #if car is vertical and size 2
            for i in range(v_val-1, -1, -1): #head
                if self.board[i][h_val] !='.':
                    num+=1
                    if self.board[i][h_val] not in checked_cars:
                        checked_cars.add(self.board[i][h_val])
                        num += self.Blocked_val(self.board[i][h_val])
            for i in range(h_val+2, 6): #tail
                if self.board[v_val][i] !='.':
                    num+=1
                    if self.board[v_val][i] not in checked_cars:
                        checked_cars.add(self.board[v_val][i])
                        num += self.Blocked_val(self.board[v_val][i])
        elif current_car_obj.size == 2: #if car is size 2
            for i in range(v_val-1, -1, -1): #head
                if self.board[i][h_val] !='.':
                    num+=1
                    if self.board[i][h_val] not in checked_cars:
                        checked_cars.add(self.board[i][h_val])
                        num += self.Blocked_val(self.board[i][h_val])
            for i in range(h_val+2, 6): #tail
                num+=1
                if self.board[v_val][i] != '.':
                    if self.board[v_val][i] not in checked_cars:
                        checked_cars.add(self.board[v_val][i])
                        num += self.Blocked_val(self.board[v_val][i])

        return num


    def heuristic_val(self):
        num = 0
        global checked_cars 
        checked_cars.clear()
        checked_cars.add("X")
        for i in range(5, 0, -1):
            if self.board[2][i] == "X":
                break
            elif self.board[2][i] != '.':
                # print(self.board[2][i])
                num += self.Blocked_val(self.board[2][i])
        # print(num)
        return num + len(self.moves_made)

    


    

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
    BFSqueue = []

    BFSqueue.append(initial_board)
    current_state = initial_board
    discovered = set()
    count = 0
    while BFSqueue:
        current_state = BFSqueue.pop(0)

        if current_state.win():
            print(count)
            return current_state

        stringboard= current_state.boardToString()
        if stringboard not in discovered:
            temp_nextstates = current_state.expand()
            count += 1
            
            for next_state in temp_nextstates:
                BFSqueue.append(next_state)
            discovered.add(stringboard)
    return False

def BFSv2(initial_board):
    BFSqueue = []

    BFSqueue.append(initial_board)
    current_state = initial_board
    discovered = set()
    count = 0
    while not current_state.win():
        

        temp_nextstates = current_state.expand()
        count += 1
        for next_state in temp_nextstates:
            if next_state.stringboard not in discovered:
                BFSqueue.append(next_state)
                discovered.add(next_state.stringboard)
        current_state = BFSqueue.pop(0)
    print(count)       
    return(current_state)

def DFS(initial_board):
    DFSstack = queue.LifoQueue()
    DFSstack.put(initial_board)
    current_state = initial_board
    discovered = []
    while not current_state.win() and not DFSstack.empty():
        current_state = DFSstack.get()
        temp_nextstates = current_state.nextstates()
        if current_state.board not in discovered:
            for next_state in temp_nextstates:
                DFSstack.put(next_state)
            discovered.append(current_state.board)
    return current_state

def DepthLimitedSearch(initial_board, depth_limit):
    DLSstack = [initial_board]
    current_state = initial_board
    discovered = dict()
    while DLSstack:
        current_state = DLSstack.pop()
        if current_state.win():
            return current_state

        # print(current_state.moves_made)
        stringboard= current_state.boardToString()
        if (stringboard not in discovered or len(current_state.moves_made) < discovered[stringboard]) and len(current_state.moves_made) < depth_limit:
            temp_nextstates = current_state.expand()
            for next_state in temp_nextstates:
                
                DLSstack.append(next_state)
            discovered[stringboard] = len(current_state.moves_made)

    return False
    
def Iterative_d(initial_board):
    count = 0
    while True:
        count +=1
        result = DepthLimitedSearch(initial_board, count)
        if result !=False:
            return result

def A_star(initial_board):
    Prio_Q = queue.PriorityQueue()
    Order = dict()
    Order[initial_board.heuristic_val()] = count()
    Prio_Q.put((initial_board.heuristic_val(), Order[initial_board.heuristic_val()], initial_board))
    current_state = initial_board
    discovered = set()
    counter = 0


    while not Prio_Q.empty():
        current_state = Prio_Q.get()[2]
        if current_state.win():
            print(counter)
            return current_state
        stringboard = current_state.boardToString()
        if stringboard not in discovered:
            discovered.add(stringboard)
            counter +=1
            temp_nextstates = current_state.expand()
            for next_state in temp_nextstates:
                NV=next_state.heuristic_val()
                if(NV not in Order):
                    Order[NV]=count()
                Prio_Q.put((NV, next(Order[NV]), next_state))
    return False

def A_starv2(initial_board):
    Prio_Q = queue.PriorityQueue()
    Order = count()
    Prio_Q.put((initial_board.heuristic_val(), Order, initial_board))
    current_state = initial_board
    discovered = set()
    counter = 0

    while not Prio_Q.empty():
        current_state = Prio_Q.get()[2]
        if current_state.win():
            print(counter)
            return current_state
        stringboard = current_state.boardToString()
        if stringboard not in discovered:
            discovered.add(stringboard)
            counter+=1
            temp_nextstates = current_state.expand()
            for next_state in temp_nextstates:
                NV=next_state.heuristic_val()
                Prio_Q.put((NV, next(Order) + 1000000*len(next_state.moves_made), next_state))
    return False

def hill_climbing(initial_board):
    unique = count()
    discovered = set()
    current_state = initial_board

    while not initial_board.win():
        local_states = queue.PriorityQueue()
        next_local_states = current_state.expand()
        



def random_restart(initial_board):
    random_boards = []
    BFSqueue = []

    BFSqueue.append(initial_board)
    current_state = initial_board
    discovered = set()
    count = 0
    while BFSqueue:
        current_state = BFSqueue.pop(0)
        # print(current_state.moves_made)
        stringboard= current_state.boardToString()
        if stringboard not in discovered and len(current_state.moves_made) < 5:
            temp_nextstates = current_state.expand()
            count += 1
            
            for next_state in temp_nextstates:
                BFSqueue.append(next_state)
                random_boards.append(next_state)
            discovered.add(stringboard)
    return random_boards

def random_restartv2(initial_board):
    node_expand_list = initial_board.expand() #initilise expand list
    for i in range(random.randint(0, 4)): #go to random node depth (max of 5)
        node_expand_list = node_expand_list[random.randint(0, len(node_expand_list)-1)].expand() # remake node expand list with a randomly chosen next node
    return node_expand_list[random.randint(0, len(node_expand_list)-1)] # return randomly chosen node
            
        


game = Game()
x = game.boards[1]
x.printBoard()
start = time.time()
x= A_star(x)
finish = time.time()
x.printBoard()
print(x.moves_made)
print(finish-start)


# times = []
# lessthan3 = 0
# lessthan5  =0
# lessthan10 = 0
# other = 0
# for Qustion in range (1, 41):
#     #prints initial board and proposed solutions
#     print("\n  Problem", Qustion, ":")
#     game.boards[Qustion].printBoard()

#     start = time.time()
#     x = BFS(game.boards[Qustion])
#     finish = time.time()
#     print("Solution:")
#     x.printBoard()
#     print(x.moves_made)
#     time_taken = finish - start
#     if time_taken <3:
#         lessthan3 +=1
#     elif time_taken <5:
#         lessthan5 +=1
#     elif time_taken <10:
#         lessthan10 +=1
#     else:
#         other +=1


#     times.append(time_taken)
#     print("Time taken:", time_taken)

# total = 0.0
# for num in times:
#     total+= num
# average = total/len(times)
# print("Average Time Taken:", average)
# print("Less than 3s:", lessthan3)
# print("Less than 5s:", lessthan5)
# print("Less than 10s:", lessthan10)
# print("Other", other)

#class inheritance structure
#game.boards[problem_No].board
#game.boards[problem_No].solution
#game.boards[problem_No].cars[car_letter].car_property