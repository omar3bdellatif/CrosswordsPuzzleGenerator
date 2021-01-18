from HelperFunctionsSearch import *

class Crossword_problem:
    def __init__(self,dimensions,initial_grid,dictionary):
        self.dimensions=dimensions
        self.initial_grid=initial_grid
        self.dictionary=dictionary
        self.initial_state=()

    #Sets the state[Cells_to_fill] tuple by iterating over each cell in the grid, getting the mode (vertical,horizontal,or both)
    #getting the length of the word, and getting all intersections
    def get_initial_state(self):
        self.initial_state =  initilize_initial_state(self.initial_state,self.dimensions,self.initial_grid,self.dictionary)
        for i in range(len(self.initial_grid)):
            for j in range(len(self.initial_grid[i])):
                if(not is_wall_cell(i,j,self.initial_grid)):
                    mode = is_word_beginning_cell(i,j,self.initial_grid,self.dimensions)
                    if(mode == "Vertical" or mode == "Horizontal"):
                        length_and_intersections = get_word_length_and_intersections(self.initial_grid,i,j,mode,self.dimensions)
                        self.initial_state =  modify_initial_state(self.initial_grid,i,j,mode,length_and_intersections,self.initial_state)
                    elif(mode == "VerticalHorizontal"):
                        mode = "Vertical"
                        length_and_intersections = get_word_length_and_intersections(self.initial_grid,i,j,mode,self.dimensions)
                        self.initial_state =  modify_initial_state(self.initial_grid,i,j,mode,length_and_intersections,self.initial_state)
                        mode = "Horizontal"
                        length_and_intersections = get_word_length_and_intersections(self.initial_grid,i,j,mode,self.dimensions)
                        self.initial_state =  modify_initial_state(self.initial_grid,i,j,mode,length_and_intersections,self.initial_state)
                        mode = "VerticalHorizontal"
        
        return(self.initial_state)

    
    #Returns a list of valid actions from a state
    def get_actions(self,state):
        grid = state[grid_index]
        actions = []

        #get the cell to be filled
        cell_index = state[Next_Cell]
        cell_to_fill = state[Cells_to_fill][cell_index]

        #unpack its items
        coordinates = cell_to_fill[0]
        word_length = cell_to_fill[1]
        mode = cell_to_fill[2]

        #get all the available words
        words = state[Words]

        #filter the words to get only the words that fit
        candidate_words = [i for i in words if len(i) == word_length]

        #for each word, if the word doesn't modify any intersection cell (Causes no conflict), then inserting
        #it is a valid action
        #The action format is shown below
        for word in candidate_words:
            if(is_valid_action(cell_to_fill,word,grid)):
                actions.append((word,word_length,coordinates,mode))
        return actions

    #Returns the successor state after applying a certain action to a given state
    def transition_model(self,state,action):
        #The cost of inserting a word is simply 1
        cost = 1

        #To modify the state, first convert it to a list
        state = state_from_tuple_to_list(state)

        #unpack the needed attributes from the action tuple
        word = action[0]
        coordinates = action[2]
        mode = action[3]

        #update the grid
        fill_grid(state[grid_index],coordinates,mode,word)

        #remove the used word from the list of available words to be used
        state[Words].remove(word)

        #Now the cell to fill should be updated, so simply increment its index
        state[Next_Cell] = state[Next_Cell] + 1

        #convert the state back to a tuple
        state = state_from_list_to_tuple(state)
        return state,cost

    #The estimation here is the number of words needed to completely fill the puzzle
    def heuristic(self,state):
        #if(state[Next_Cell] == len(state[Cells_to_fill])):
        #    return 0
        word_index = state[Next_Cell]

        estimation = len(state[Cells_to_fill]) - word_index
        #estimation = len(self.get_actions(state))
        
        return estimation

    #If there are no empty cells, return true, else, return false
    def is_goal(self,state):
        if(state[Next_Cell] == len(state[Cells_to_fill])):
            return True
        return False

        

    def print_grid(self,state):
        grid = state[grid_index]
        for i in grid:
            print(i)
        

        




        
        

        
