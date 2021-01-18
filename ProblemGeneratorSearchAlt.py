from CrosswordDefinitionSearch import Crossword_problem
from HelperFunctionsSearch import print_action,initilize_initial_state,state_from_list_to_tuple,state_from_tuple_to_list
import datetime


def greedy_best_first(problem:Crossword_problem):

    initial_state = problem.get_initial_state()
    #actions,evaluation = problem.actions_heuristic(initial_state)
    frontier = [(initial_state,problem.heuristic(initial_state))]

    while(len(frontier) > 0):
        
        current_state,_ = frontier.pop(0)

        if(problem.is_goal(current_state)):
            goal_state = current_state
            return goal_state,1,1
                    

        #Action format is (word,word_length,coordinates,mode)
        actions = problem.get_actions(current_state)

        for action in actions:
            successor,_ = problem.transition_model(current_state,action)
            evaluation = problem.heuristic(successor)
            #To avoid inserting duplicate states. Note that duplicate states are only generated if there are duplicate words in the dictionary
            #Also note that, because the grid is being filled at a certain starting coordinate at a time, duplicate states will always have
            #the same parent
            if((successor,evaluation) not in frontier):
                frontier.append((successor,evaluation))
            
        frontier.sort(key= lambda tup: tup[1])
    return -1,-1,-1


if __name__ == "__main__":

    test_case = int(input("Choose test case 1 or 2 or 3 (1 is an 8x8 grid, 2 is a 10x10 grid, and 3 is a 13x13 grid): "))
    while(test_case < 1 or test_case > 3):
        test_case = int(input("Please choose 1 or 2 or 3 only: "))
    
    max_size = 5458
    if(test_case == 2):
        max_size = 500
    elif(test_case == 3):
        max_size = 100
    dict_size = int(input("Please enter the dictionary size (max = "+str(max_size)+"): "))
    while(dict_size > max_size):
        dict_size = int(input("Please enter the dictionary size (max = "+str(max_size)+"): "))


    f = open("words.txt","r")
    words = f.readlines()
    word_dict = []
    iter = 0
    for word in words:
        word_dict.append(word.strip())
        if (iter >= dict_size):
            break
        iter += 1

    if(test_case == 1):
        valid_words = ("buzzword","juggling","zoo","bag","diagonal","tomatoes","edit","urus","baum","zigzag","logout","ohio","lake","doge")
        grid =((1,1,1,1,1,1,1,1),(0,1,0,1,0,1,0,1),(1,1,1,1,1,1,1,1),(0,1,0,1,1,1,0,1),(1,0,1,1,1,0,1,0),(1,1,1,1,1,1,1,1),(1,0,1,0,1,0,1,0),(1,1,1,1,1,1,1,1))
    elif(test_case == 2):
        valid_words = ("melon","mesa","regime","midas","tuna","altar","sir","eros","ants","art","therm","dome","rupee","normal","peon","serum","mimosa","intone","dart","moo","oral","stern","nest","eras","mitre","rule","emu","ramp","senior","stream")
        grid = ((1,1,1,1,1,0,1,1,1,1),(1,0,0,1,1,1,1,1,1,0),(1,1,1,1,1,0,1,1,1,1),(1,0,1,1,1,1,1,0,1,0),(1,1,1,0,0,0,1,1,1,1),(1,1,1,1,0,0,0,1,1,1),(0,1,0,1,1,1,1,1,0,1),(1,1,1,1,0,1,1,1,1,1),(0,1,1,1,1,1,1,0,0,1),(1,1,1,1,0,1,1,1,1,1))
    elif(test_case == 3):
        valid_words = ("seep","coo","pert","axle","old","aloe","silenced","reba","stereo","racer","seacoast","sta","armoire","cons","ate","lobe","imitate","nil","macaroni","scale","modelt","cute","traveler","abes","ooh","also","mast","tea","last","sass","sci","scam","exit","tom","cuba","elle","animates","peers","stalest","nee","ace","cocoa","ata","tot","ole","cater","roe","odd","ore","omaha","ram","nov","parasol","ideal","election","ella","robe","rbi","less","tear","eel","trot")
        grid =((1,1,1,1,0,1,1,1,0,1,1,1,1),(1,1,1,1,0,1,1,1,0,1,1,1,1),(1,1,1,1,1,1,1,1,0,1,1,1,1),(1,1,1,1,1,1,0,0,1,1,1,1,1),(0,0,0,1,1,1,1,1,1,1,1,0,0),(1,1,1,0,0,0,1,1,1,1,1,1,1),(1,1,1,1,0,1,1,1,0,1,1,1,1),(1,1,1,1,1,1,1,0,0,0,1,1,1),(0,0,1,1,1,1,1,1,1,1,0,0,0),(1,1,1,1,1,0,0,1,1,1,1,1,1),(1,1,1,1,0,1,1,1,1,1,1,1,1),(1,1,1,1,0,1,1,1,0,1,1,1,1),(1,1,1,1,0,1,1,1,0,1,1,1,1))
 
    dimensions = (len(grid),len(grid[0]))

    for word in valid_words:
        word_dict.append(word)

    word_dict = tuple(word_dict)

    

    time_before = datetime.datetime.now()
    problem = Crossword_problem(dimensions,grid,word_dict)
    final_state,cost,sol = greedy_best_first(problem)
    time_after = datetime.datetime.now()

    if(cost == -1):
        print("No solution exists to this problem")
    else:
        
        problem.print_grid(final_state)
        print("Time taken: ",time_after-time_before)


