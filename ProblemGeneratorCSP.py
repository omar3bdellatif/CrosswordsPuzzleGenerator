from CrosswordDefinitionCSP import Crossword_problemCSP
from HelperFunctionsCSP import fill_grid
import copy,datetime

#Gets the variable with the minimum remaining values
def get_MRV_variable(state):
    #Initialize min size to 1000, a more robust way would be to initialize it to the dictionary size
    min_domain_size = 1000

    #Iterate over the domain of each variable, and get the variable which has min domain size and has no assigned
    #value
    for variable,domain in state["Domain"].items():
        assigned_value = state["Variables"][variable]
        if(assigned_value != -1):
            continue
        if(len(domain) < min_domain_size):
            min_domain_size = len(domain)
            MRV_variable = variable
    
    return MRV_variable


#Get a list of the values in the domain of a variable, ordered ascendingly by how constraining the value is
def get_least_constraining_values(state,variable):

    #get all values from the variable's domain, and get all the constraints that the variable participates in
    candidate_values = state["Domain"][variable]
    constraints = state["Constraints"][variable]
    values = []
    
    #Loop over the candidate values, and compute how many constraints using each value would enforce
    for value in candidate_values:
        number_of_constraints = 0
        for constraint in constraints:
            #Unpack the constraints
            constrained_variable = constraint[0]
            constraining_index=constraint[1]
            constrained_index = constraint[2]

            #The value which should be equal in both variables since it lies at the intersection of the two variables
            value_at_index = value[constraining_index]

            #There are the values which might be removed if they do not satisfy the constraint
            constrained_values = state["Domain"][constrained_variable]

            #For each of these values (which are strings), check that letter at the intersection is the same
            #As the value_at_index, and if not, then that would be a constraint, so we will increment the
            #number of constraints for the value
            for constrained_value in constrained_values:
                if(constrained_value[constrained_index] != value_at_index):
                    number_of_constraints += 1
        
        #Finally, append the value alongside the number of constraints to the values list
        values.append([value,number_of_constraints])
    
    #Sort the values list by the second element (number of constraints)
    values.sort(key= lambda x: x[1])

    #Now that the list has been sorted, retrieve only the first element (the value) of each item in the list
    values = [i[0] for i in values]

    return values


#Works very similarly to the get_least_constraining_values function, except that when it finds a value for
#a constrained variable that doesn't satisfy the constraint, it removes the value from its domain
def forward_propagation(state,variable,value):

    constraints = state["Constraints"][variable]
    for constraint in constraints:
        constrained_variable = constraint[0]
        constraining_index=constraint[1]
        constrained_index = constraint[2]
        value_at_index = value[constraining_index]
        constrained_values = state["Domain"][constrained_variable]
        remove_list = []
        for constrained_value in constrained_values:
            if(constrained_value[constrained_index] != value_at_index):
                remove_list.append(constrained_value)
        for i in remove_list:
            state["Domain"][constrained_variable].remove(i)
    return state
    

#Returns true iff a value has been assigned to all variables
def is_goal(state):
    for assigned_value in state["Variables"].values():
        if(assigned_value == -1):
            return False
    return True


def CSP_Solver(problem:Crossword_problemCSP):
    #To keep track of states in case we need to back propagate
    state_tracker = []

    #Initalizations
    state = problem.initial_state()
    backtracking = False
    MRV_variable = 0
    least_constraining_values = 0
    value = 0

    #Main loop, terminates when a solution is found or no possible solution exists
    while(True):
        if(backtracking == False):
            MRV_variable = get_MRV_variable(state)
            least_constraining_values = get_least_constraining_values(state,MRV_variable)

            #Possibly because forward propagation removed all values from the variables domain, so backtrack
            if(len(least_constraining_values) == 0):
                backtracking = True
                continue

            value = least_constraining_values[0]

            #This value index is used to keep track of which value we used last time, so if we backtrack, we
            #will know which value to use next
            value_index = 0
            
        else:
            #No more states to backtrack to, which happens when we have backtracked all the way to the first
            #variable and tried all of its values
            if(len(state_tracker) == 0):
                return -1,-1,-1

            full_state = state_tracker.pop()

            #Extract items from the state-tracker element retrieved
            state = full_state[0]
            MRV_variable = full_state[1]
            least_constraining_values = full_state[2]
            value_index = full_state[3]

            #Now we will increment the index to get the next value to be assigned, but first check that
            #it is within bounds of the least_constraining_values list, if not, back-track again
            value_index += 1
            if(len(least_constraining_values) == value_index):
                continue

            value = least_constraining_values[value_index]
            backtracking = False

        #Extract items from the MRV_variable
        coordinates = MRV_variable[0]
        mode = MRV_variable[1]

        #Fill the grid with the new value (for visualization) and assign the new value to the variable
        fill_grid(state["Grid"],coordinates,mode,value)
        state["Variables"][MRV_variable] = value

        #If we have reached a goal state (a full assignment), return the variables and the assigned values, alongside the grid for visualization
        if(is_goal(state)):
            variables = []
            assignments = []
            for variable,value in state["Variables"].items():
                variables.append(variable)
                assignments.append(value)
            return variables,assignments,state["Grid"]

        #If we did not reach a goal state, then get a copy of the state and push it into the state-tracker, then
        #perform forward propagation
        state_copy = copy.deepcopy(state)
        state_tracker.append([state_copy,MRV_variable,least_constraining_values,value_index])
        state = forward_propagation(state,MRV_variable,value)


#Prints the variables and te assignments in a neat way
def print_solution(variables,assignments):
    for variable,assignment in zip(variables,assignments):
        print("Variable: ",variable," Assignment: ",assignment)




if __name__ == "__main__":

    test_case = int(input("Choose test case 1 or 2 or 3 (1 is an 8x8 grid, 2 is a 10x10 grid, and 3 is a 13x13 grid): "))
    while(test_case < 1 or test_case > 3):
        test_case = int(input("Please choose 1 or 2 or 3 only: "))

    dict_size = int(input("Please enter the dictionary size (max = 5458): "))
    while(dict_size > 5458):
        dict_size = int(input("Please enter the dictionary size (max = 5458): "))

    
    f = open("words.txt","r")
    words = f.readlines()
    word_dict = []
    for word in words:
        word_dict.append(word.strip())


    if(test_case == 3):
        valid_words = ("seep","coo","pert","axle","old","aloe","silenced","reba","stereo","racer","seacoast","sta","armoire","cons","ate","lobe","imitate","nil","macaroni","scale","modelt","cute","traveler","abes","ooh","also","mast","tea","last","sass","sci","scam","exit","tom","cuba","elle","animates","peers","stalest","nee","ace","cocoa","ata","tot","ole","cater","roe","odd","ore","omaha","ram","nov","parasol","ideal","election","ella","robe","rbi","less","tear","eel","trot")
        grid =[[1,1,1,1,0,1,1,1,0,1,1,1,1],[1,1,1,1,0,1,1,1,0,1,1,1,1],[1,1,1,1,1,1,1,1,0,1,1,1,1],[1,1,1,1,1,1,0,0,1,1,1,1,1],[0,0,0,1,1,1,1,1,1,1,1,0,0],[1,1,1,0,0,0,1,1,1,1,1,1,1],[1,1,1,1,0,1,1,1,0,1,1,1,1],[1,1,1,1,1,1,1,0,0,0,1,1,1],[0,0,1,1,1,1,1,1,1,1,0,0,0],[1,1,1,1,1,0,0,1,1,1,1,1,1],[1,1,1,1,0,1,1,1,1,1,1,1,1],[1,1,1,1,0,1,1,1,0,1,1,1,1],[1,1,1,1,0,1,1,1,0,1,1,1,1]]
    elif(test_case == 2):
        valid_words = ("melon","mesa","regime","midas","tuna","altar","sir","eros","ants","art","therm","dome","rupee","normal","peon","serum","mimosa","intone","dart","moo","oral","stern","nest","eras","mitre","rule","emu","ramp","senior","stream")
        grid = [[1,1,1,1,1,0,1,1,1,1],[1,0,0,1,1,1,1,1,1,0],[1,1,1,1,1,0,1,1,1,1],[1,0,1,1,1,1,1,0,1,0],[1,1,1,0,0,0,1,1,1,1],[1,1,1,1,0,0,0,1,1,1],[0,1,0,1,1,1,1,1,0,1],[1,1,1,1,0,1,1,1,1,1],[0,1,1,1,1,1,1,0,0,1],[1,1,1,1,0,1,1,1,1,1]]
    elif(test_case == 1):
        valid_words = ("buzzword","juggling","zoo","bag","diagonal","tomatoes","edit","urus","baum","zigzag","logout","ohio","lake","doge")
        grid =[[1,1,1,1,1,1,1,1],[0,1,0,1,0,1,0,1],[1,1,1,1,1,1,1,1],[0,1,0,1,1,1,0,1],[1,0,1,1,1,0,1,0],[1,1,1,1,1,1,1,1],[1,0,1,0,1,0,1,0],[1,1,1,1,1,1,1,1]]

    dimensions = (len(grid),len(grid[0]))

    for word in valid_words:
        word_dict.append(word)

    word_dict = tuple(word_dict)


    time_before = datetime.datetime.now()
    problem = Crossword_problemCSP(dimensions,grid,word_dict)
    variables,assignments,grid = CSP_Solver(problem)
    time_after = datetime.datetime.now()

    

    if(assignments == -1):
        print("No solution exists for this problem")
    else:
        
        print("Variables list: ", variables)
        print("Assignment list: ",assignments)
        print("---------------------------------------")
        print("To better observe the solution: ")
        print_solution(variables,assignments)
        print("Resulting grid: ")
        for i in grid:
            print(i)

    

    print("Time taken = ",time_after-time_before)

