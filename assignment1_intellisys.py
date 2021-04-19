# work of Timothy Tadj s5178358
max_time_to_run = 10 #time given for each search to run
import os
import sys
import copy
import time
import random
import queue
from itertools import count

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

    def printBoardf(self, f): #print board of current problem        
        print("    1 2 3 4 5 6 ", file = f)
        print("  +-------------+", file = f)
        for i in range(6):
            print(i+1, "|", end = " ", file = f)
            for j in range(6):
                print(self.board[i][j], end = " ", file = f)
            if i == 2:
                print("  ==>", file = f)
            else:
                print("|", file = f)

        print("  +-------------+", file = f)
        print("    a b c d e f ", file = f)

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
        for key, car in self.cars.items(): # go through all cars
            if self.moves_made: # if car was in the previous move, skip this car
                if self.moves_made[-1][-3] == key: 
                    continue
            
            #look for move at head of car
            boarder = car.dimension[car.isHorizontal]+1 #determine the distance between the car and the boarder to stay in bounds
            for i in range(1, boarder):
                h_domain = car.dimension[0] - car.isVertical * i #look at the ith position infrom tof the car
                v_domain = car.dimension[1] - car.isHorizontal * i #look at the ith position infrom tof the car
                if(h_domain >= 0 and v_domain >=0): #bounds check
                    if (self.board[h_domain][v_domain] == '.'): #check position before head of car
                        move = ""
                        movNum = i
                        move += key + car.isVertical * 'U' + car.isHorizontal * 'L' + str(movNum)#make move symbol
                        temp_board = copy.deepcopy(self) #use tempboard to append to list of boards
                        temp_board.moves_made.append(move) #keep track of move
                        for j in range(car.size): #remove car from board
                            temp_board.board[car.dimension[0] + (car.isVertical * j)][car.dimension[1] + (car.isHorizontal * j)] = "."
                            
                        for j in range(car.size): #add car in new position
                            temp_board.board[car.dimension[0] - (car.isVertical * (movNum - j))][car.dimension[1] - (car.isHorizontal * (movNum - j))] = key
                        temp_board.cars[key].dimension = [car.dimension[0]-movNum*car.isVertical, car.dimension[1]-movNum*car.isHorizontal] #update position of car
                        temp_board.stringboard = temp_board.boardToString() #update stringboard
                        next_states.append(temp_board) #append to list of boards
                    else: #if we find a car we can move anymore
                        break
            
            #look for move at tail of car
            boarder = (7 - car.dimension[car.isHorizontal] - car.size) #determine the distance between the car and the boarder to stay in bounds
            for i in range(1, boarder):
                h_domain = car.dimension[0] + (car.isVertical * (car.size + i -1)) #look at the ith position behind the car
                v_domain = car.dimension[1] + (car.isHorizontal * (car.size + i -1)) #look at the ith position behind the car
                if(h_domain < 6 and v_domain < 6):
                    if (self.board[h_domain][v_domain] == '.'):
                        move = ""
                        movNum = i
                        move += key + car.isVertical * 'D' + car.isHorizontal * 'R' + str(movNum)#make move symbol
                        temp_board = copy.deepcopy(self) #use tempboard to append to list of boards
                        temp_board.moves_made.append(move) #keep track of move
                        for j in range(car.size): #remove car from board
                            temp_board.board[car.dimension[0] + (car.isVertical * j)][car.dimension[1] + (car.isHorizontal * j)] = "."
                        
                        for j in range(car.size): #add car in new position
                            temp_board.board[car.dimension[0] + (car.isVertical * (movNum + j))][car.dimension[1] + (car.isHorizontal * (movNum + j))] = key
                        temp_board.cars[key].dimension = [car.dimension[0]+movNum*car.isVertical, car.dimension[1]+movNum*car.isHorizontal] #update position of car
                        temp_board.stringboard = temp_board.boardToString() #update stringboard
                        next_states.append(temp_board) #append to list of boards
                    else:#if we find a car we can move anymore
                        break
        return next_states

    def heuristic_val(self):
        num = 0
        for i in range(5, 0, -1): #count number of cars in front of x
            if self.board[2][i] == "X":
                break
            elif self.board[2][i] != '.':
                num += 1

        
        return num 

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

def BFS(initial_board, file):
    
    BFSqueue = []

    BFSqueue.append(initial_board)
    current_state = initial_board
    discovered = set()
    count = 0
    start =  time.time()
    global max_time_to_run
    print("Attempting BFS for", str(max_time_to_run)+"s", file = file)
    while BFSqueue:
        current_state = BFSqueue.pop(0) #used as Queue

        if current_state.win(): #check win
            print("States explored:", count, file =file)
            return current_state
        elif time.time()-start > max_time_to_run: #check if we have run for too long
            print("Failed", file =  file)
            return -1

        stringboard= current_state.boardToString() #make string board to compare with/ put state in discovered
        if stringboard not in discovered: #if state is unique we will expand and add state to queue
            temp_nextstates = current_state.expand()
            count += 1
            
            for next_state in temp_nextstates: #add states to queue
                BFSqueue.append(next_state)
            discovered.add(stringboard) #add current state to dicovered set
    return False

def DepthLimitedSearch(initial_board, depth_limit, start, file):
    DLSstack = [initial_board] #use as stack
    current_state = initial_board
    discovered = dict()
    global max_time_to_run
    counter = 0
    
    while DLSstack:
        current_state = DLSstack.pop() #used as stack
        if current_state.win(): #return if win
            return [current_state, counter]
        elif time.time()-start > max_time_to_run:#check we havent run out of time
            print("Failed", file = file)
            return -1
        stringboard= current_state.boardToString() #make string board to compare with/ put state in discovered
        #if we have reachd the depth limit or the state is discovered, dont add any more states
        if (stringboard not in discovered or len(current_state.moves_made) < discovered[stringboard]) and len(current_state.moves_made) < depth_limit:
            temp_nextstates = current_state.expand()
            counter +=1
            for next_state in temp_nextstates:
                
                DLSstack.append(next_state)
            discovered[stringboard] = len(current_state.moves_made)

    return counter #if exited without win or failure, return how many states are explored
    
def Iterative_d(initial_board, file):
    start = time.time()
    counter = 0
    count =0
    global max_time_to_run
    print("Attempting Iterative Deepening for", str(max_time_to_run)+"s", file =file)
    while True:
        count+=1
        result = DepthLimitedSearch(initial_board, count, start, file)
        if type(result) != int: # if we have found a win return result and print the states explored
            print("States explored:", counter+result[1], file =file)
            return result[0]
        elif (result == -1): #if failed return out
            return -1
        counter += result

def A_star(initial_board, file):
    Prio_Q = queue.PriorityQueue()
    Order = dict()
    Order[initial_board.heuristic_val()] = count() #keeps track of order that the same heuristic has been found
    Prio_Q.put((initial_board.heuristic_val(), Order[initial_board.heuristic_val()], initial_board))
    current_state = initial_board
    discovered = set()
    counter = 0
    start = time.time()
    global max_time_to_run
    print("Attempting A star for", str(max_time_to_run)+"s", file =file)
    while not Prio_Q.empty():
        current_state = Prio_Q.get()[2] #get state from priority q 
        if current_state.win():
            print("States explored:", counter, file =file)
            return current_state
        elif time.time()-start > max_time_to_run:
            print("Failed", file =file)
            return -1
        stringboard = current_state.boardToString()
        if stringboard not in discovered:
            discovered.add(stringboard)
            counter +=1
            temp_nextstates = current_state.expand()
            for next_state in temp_nextstates:
                NV=next_state.heuristic_val()+ len(next_state.moves_made) # find the heuristic
                if(NV not in Order):#add heuristic to dict if not present
                    Order[NV]=count()
                Prio_Q.put((NV, next(Order[NV]), next_state)) #add to priority queue with heuristc and the order
    return False

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
    for i in range(random.randint(0, 9)): #go to random node depth (max of 5)
        node_expand_list = node_expand_list[random.randint(0, len(node_expand_list)-1)].expand() # remake node expand list with a randomly chosen next node
    return node_expand_list[random.randint(0, len(node_expand_list)-1)] # return randomly chosen node

def hill_climbing(initial_board, file): #random restart and greedy first
    discovered = dict() # stores the string board and keep track of how namy move it took to get to that board
    current_state = initial_board
    neighbour_counter = 0 #counts sideways moves
    local_states = [current_state] #stores states with best heuristics
    start = time.time()
    better_found = False
    counter =0
    global max_time_to_run
    print("Attempting Hill Climbing for", str(max_time_to_run)+"s", file =file)
    while not current_state.win() :
        if neighbour_counter > 50 or not local_states: #random restart if win not found or too many sideways moves done
            local_states = [random_restartv2(initial_board)]
            neighbour_counter = 0
        if time.time()-start > max_time_to_run:
            print("Failed", file =file)
            return -1
        current_state = local_states.pop()
        counter +=1
        next_local_states = current_state.expand()
        for state in next_local_states:
            #if not discovered or state has less moves than a previously found state
            if state.stringboard not in discovered or len(state.moves_made) < discovered[state.stringboard]:
                discovered[state.stringboard] = len(state.moves_made)
                if state.heuristic_val() < current_state.heuristic_val(): # if heuristic is better then replace current state
                    current_state = state
                    local_states.clear()
                if state.heuristic_val() == current_state.heuristic_val(): # if found state with equal heuristic, add to stack (neighbour found)
                    local_states.append(state)
                    neighbour_counter +=1 #increment neighbour counter
    print("States explored:", counter, file =file)
    return current_state

game = Game()
with open(os.path.join(sys.path[0], "output.txt"), "w") as output:
    for Question in range(1, 41):
        print("Finding solution for Question", str(Question)+"...")
        print("\nQuestion", str(Question)+":", file = output)
        initial_board = game.boards[Question]
        initial_board.printBoardf(output)
        print("Sol: " + initial_board.solution, file = output)
        start = time.time()
        result = BFS(initial_board, output)
        if result != -1:
            print("Found Sol:", " ".join(result.moves_made), file=output)
            print("CPU time:", time.time()-start,"s",  file = output)
            print("Depth:", len(result.moves_made),  file = output)
            print("Difference in solution length:", len(result.moves_made) - len(initial_board.solution)//4,  file = output)
            
        start = time.time()
        result = Iterative_d(initial_board, output)
        if result != -1:
            print("Found Sol:", " ".join(result.moves_made), file=output)
            print("CPU time:", time.time()-start,"s", file = output)
            print("Depth:", len(result.moves_made),  file = output)
            print("Difference in solution length:", len(result.moves_made) - len(initial_board.solution)//4,  file = output)
            
        start = time.time()
        result = A_star(initial_board, output)
        if result != -1:
            print("Found Sol:", " ".join(result.moves_made), file=output)
            print("CPU time:", time.time()-start,"s", file = output)
            print("Depth:", len(result.moves_made),  file = output)
            print("Difference in solution length:", len(result.moves_made) - len(initial_board.solution)//4,  file = output)
            
        start = time.time()
        result = hill_climbing(initial_board, output)
        if result != -1:
            print("Found Sol:", " ".join(result.moves_made), file=output)
            print("CPU time:", time.time()-start,"s", file = output)
            print("Depth:", len(result.moves_made),  file = output)
            print("Difference in solution length:", len(result.moves_made) - len(initial_board.solution)//4,  file = output)
            