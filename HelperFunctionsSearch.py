#To be converted to an Enum
Cells_to_fill = 0
grid_index= 1
Words = 2
Next_Cell=3

'''
State format:
state[Cell_to_fill] is a tuple of tuples, where each tuple inside it has the following format (coordinates, length,mode,intersections)
intersections itself is a tuple or tuples as well, where each tuple has the following format (coordinates of intersection, index of intersection relative to starting coordinate)
state[grid_index] is a tuple of tuples, each tuple represents a row in the grid
state[Words] is a tuple consisting of the words that have not yet been inserted into the grid
state[Next_Cell] is an integer used to index into the state[Cell_to_fill] tuple, to get the cell we will fill next
'''

#Convert the state to a mutable list
def state_from_tuple_to_list(state):
    state = list(state)
    state[Cells_to_fill] = list(state[Cells_to_fill])
    state[grid_index] = list(state[grid_index])
    for i in range(len(state[grid_index])):
        state[grid_index][i] = list(state[grid_index][i])
    state[Words] = list(state[Words])
    return state

#Convert the state to an immutable tuple
def state_from_list_to_tuple(state):
    state[Cells_to_fill] = tuple(state[Cells_to_fill])
    for i in range(len(state[grid_index])):
        state[grid_index][i] = tuple(state[grid_index][i])
    state[grid_index] = tuple(state[grid_index])   
    state[Words] = tuple(state[Words])
    state = tuple(state)
    return state


#To be removed
def append_to_tuple(my_tuple,x):
    my_tuple = list(my_tuple)
    my_tuple.append(x)
    my_tuple = tuple(my_tuple)

#Used to insert a word starting at a given coordinate in the grid, either vertically or horizontally
def fill_grid(grid,coordinates,mode,word):
    x = coordinates[0]
    y = coordinates[1]
    word_length = len(word)
    if(mode == "Vertical"):
        for i in range(x,x+word_length):
            grid[i][y] = word[i-x]
    elif(mode == "Horizontal"):
        for j in range(y,y+word_length):
            grid[x][j] = word[j-y]
    


#Used to create the initial form of initial state, sort of like a skeleton of the initial state
#(((starting_coordinates,length,mode,(intersections,each intersection is a tuple containing the coordinates and the index)),(),.....),........)
def initilize_initial_state(initial_state,dimensions,grid,words):
    initial_state = list(initial_state)
    initial_state.append(())
    initial_state.append(grid)
    initial_state.append(words)
    initial_state.append(0)
    initial_state = tuple(initial_state)
    return initial_state

#Used to get the coordinates of the next cell to be filled
#To be removed
def get_next_cell_to_fill(state,dimensions):
    grid = state[grid_index]
    i,j=state[3]
    i_limit = len(grid)
    j_limit = len(grid[0])
    
    while(True):
        j +=1
        if(j >= j_limit):
            j = 0
            i +=1
            if(i >= i_limit):
                return(-1,-1)
            else:
                if(grid[i][j] == 0):
                    continue
                else:
                    if(is_word_beginning_cell(i,j,grid,dimensions) != "False"):
                        return(i,j)
        else:
            if(grid[i][j] == 0):
                continue
            else:
                if(is_word_beginning_cell(i,j,grid,dimensions) != "False"):
                    return(i,j)    

    return(i,j)

#Used to check whether the cell is a wall cell or not
def is_wall_cell(i,j,grid):
    if(grid[i][j] == 0):
        return True
    else:
        return False

'''
Used to check whether the cell is a word-beginning cell or not, note that we return a string, not a boolean
Because we have 4 possible outcomes, not a word-beginning cell, a vertical word-beginning cell, a horizontal
word-beginning cell, or a vertical and a horizontal word-beginning cell
'''
def is_word_beginning_cell(i,j,grid,dimensions):
    vertical_dim=dimensions[0]
    horizontal_dim = dimensions[1]
    result = "False"

    #Check if the cell is the beginning of a vertical word
    if(i-1 < 0 or grid[i-1][j] == 0):
        if(i+1 < vertical_dim and grid[i+1][j] == 1):
            result = "Vertical"
    
    #Check if the cell is the beginning of a horizontal word
    if(j-1 < 0 or grid[i][j-1] == 0):
        if(j+1 < horizontal_dim and grid[i][j+1] == 1):
            if(result == "Vertical"):
                result += "Horizontal"
            else:
                result = "Horizontal"
    return result  


def is_intersection_cell(grid,i,j,mode,dimensions):

    #Check horizontal intersection (Used for cells that start a vertical word)
    if(mode == "Vertical"):
        limit = dimensions[1]
        if((j+1 < limit and grid[i][j+1] == 1) or (j-1 >= 0 and grid[i][j-1] == 1)):
            return True
        else:
            return False
        
    #Check vertical intersection (Used for cells that start a horizontal word)
    if(mode == "Horizontal"):
        limit = dimensions[0]
        if((i+1 < limit and grid[i+1][j] == 1) or (i-1 >= 0 and grid[i-1][j] == 1)):
            return True
        else:
            return False

    #Check if the cell is an intersecting cell in general
    #To be removed (bas msh mota2aked awi men dy, fa law hasal error you know where to go)
    if(mode == None):
        if(grid[i][j] == 0):
            return False

        limit = dimensions[1]
        if((j+1 < limit and grid[i][j+1] != 0) or (j-1 >= 0 and grid[i][j-1] != 0)):
            limit = dimensions[0]
            if((i+1 < limit and grid[i+1][j] != 0) or (i-1 >= 0 and grid[i-1][j] != 0)):
                return True
        return False

#Used to check if the cell is a non-empty intersection cell, and has two words contributing to its value
#To be removed, msh bahseb el heuristic kda anymore
def is_filled_intersection_cell(grid,i,j,dimensions):
    if(grid[i][j] == 0 or grid[i][j] == 1):
        return False

    limit = dimensions[1]
    if((j+1 < limit and grid[i][j+1] != 0 and grid[i][j+1] != 1) or (j-1 >= 0 and grid[i][j-1] != 0 and grid[i][j-1] != 1)):
        limit = dimensions[0]
        if((i+1 < limit and grid[i+1][j] != 0 and grid[i+1][j] != 1) or (i-1 >= 0 and grid[i-1][j] != 0 and grid[i-1][j] != 1)):
            return True
    return False

            
#Returns the length of the word beginning at i,j, given the mode (vertical or horizontal)
#and constructs a list of intersections along its path, where each intersection is a tuple, consisting of
#the coordinates of intersection, and the index of the intersection relative to the beginning cell
def get_word_length_and_intersections(grid,i,j,mode,dimensions):

    length = 1
    intersections = []

    if(mode == "Vertical"):
        iterator = i
        limit = dimensions[0]     
        while(True):
            #Check for intersections
            if(is_intersection_cell(grid,iterator,j,mode,dimensions)):
                intersections.append(((iterator,j),length-1))

            iterator += 1
            if(iterator >= limit or grid[iterator][j] == 0):
                break
            length += 1
            
        
    elif(mode == "Horizontal"):
        iterator = j
        limit = dimensions[1]
        while(True):
            #Check for intersections
            if(is_intersection_cell(grid,i,iterator,mode,dimensions)):
                intersections.append(((i,iterator),length-1))

            iterator += 1 
            if(iterator >= limit or grid[i][iterator] == 0):
                break
            length += 1

    intersections = tuple(intersections)
    result = (length,intersections)
    return result

#appends a new cell to fill, given its info (coordinates,length,mode,intersections)
def modify_initial_state(grid,i,j,mode,length_and_intersections,initial_state):
    initial_state = list(initial_state)
    length = length_and_intersections[0]
    intersections = length_and_intersections[1]
    initial_state = state_from_tuple_to_list(initial_state)
    initial_state[Cells_to_fill].append(((i,j),length,mode,intersections))
    initial_state = state_from_list_to_tuple(initial_state)
    return initial_state

#Determines whether inserting a word in the grid starting at a certain cell is valid or not,
#by simply checking all the intersecting coordinates in the grid, and making sure that if they have a letter
#then this letter matches the ith letter in the word, where i is the index of the interesecting cell relative
#to the beginning cell
def is_valid_action(cell,word,grid):
    intersections = cell[3]

    for i in intersections:
        x_coordinate = i[0][0]
        y_coordinate = i[0][1]
        word_index = i[1]
        if(grid[x_coordinate][y_coordinate] != 1 and grid[x_coordinate][y_coordinate] != 0 and grid[x_coordinate][y_coordinate] != word[word_index]):
            return False
    return True    

#Used to print an action in a neat way
def print_action(action):
    word = action[0]
    location = action[2]
    orientation = action[3]
    print("Insert word: ",word," at location: ",location," ",orientation,"ly")



