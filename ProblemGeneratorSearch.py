from CrosswordDefinitionSearch import Crossword_problem
from HelperFunctionsSearch import print_action,initilize_initial_state,state_from_list_to_tuple,state_from_tuple_to_list
import datetime

#COMMENT THE GARBAGE COLLECTION PART 
#UNCOMMENT THE COMMENTED PARTS IN THE HEURISTIC FUNCTION



#Recursively remove parents whose successors have been fully explored and yielded no solution (a dead end)
def garbage_collection(predecessor,deleted_parent):
    grand_parent = predecessor[deleted_parent][0]
    del predecessor[deleted_parent]
    for i in predecessor.values():
        if(i[0] == grand_parent):
            return
    garbage_collection(predecessor,grand_parent)


def greedy_best_first(problem:Crossword_problem):

    initial_state = problem.get_initial_state()

    #Predecessor: key is a state, value is a tuple containing the parent state, the action that was performed
    #on the parent state to get to that state, and the total cost to get to that state (not the parent state)
    predecessor = {initial_state: (None,None,0)}

    frontier = [(initial_state,problem.heuristic(initial_state))]
    while(len(frontier) > 0):
        
        current_state,current_evaluation = frontier.pop(0)

        if(problem.is_goal(current_state)):
            
            solution = [0]
            goal_state = current_state
            total_cost = predecessor[current_state][2]

            while(True):
                current_state,action,cost = predecessor[current_state]
                if(current_state == None):
                    #This means that we have reached the root state, which does not have a parent state
                    #exclude the last element of the solution list (which was 0)
                    return solution[:-1],total_cost,goal_state
                else:
                    #Insert the action at the beginning of the solution list
                    solution.insert(0,action)
                    

        #Action format is (word,word_length,coordinates,mode)
        actions = problem.get_actions(current_state)
        
        #If the state has no successors, it doesn't need to be kept in the memory
        #and also, if the parent's successors have been fully explored, and none of them yielded a solution, we can safely remove the parent
        #from the memory. We will remove the parent by the recursive garbage collection function, in case the grandparent's successors have
        #been fully explored, so we might want to remove the grandparent as well, and so on.
        
        if(len(actions) == 0):
            if(len(frontier) > 0 and frontier[0][1] != current_evaluation):
                parent = predecessor[current_state][0]
                garbage_collection(predecessor,parent)
            del predecessor[current_state]
            del current_state
            continue


        for action in actions:
            successor,cost = problem.transition_model(current_state,action)
            accumulated_costs = predecessor[current_state][2]
            #Now cost is the total cost to get to that state
            cost += accumulated_costs

            #This is true if this is the first time we have reached that state
            if successor not in predecessor:
                predecessor[successor] = (current_state,action,cost)
                evaluation = problem.heuristic(successor)
                frontier.append((successor,evaluation))
            else:
                #We have seen this state before, so in case our path to it now was better than the previous
                #one (it costs less), we want to modify it in the predecessor

                #Note that the situation where a path to a state costs than another path will not occur
                #in our problem, because the cost to get to a state by any path will always be the number
                #of words assigned, I wrote it to make the algorithm more general

                prev_cost = predecessor[successor][2]
                if(cost < prev_cost):
                    successor_info = list(predecessor[successor])
                    successor_info[0] = current_state
                    successor_info[1] = action
                    successor_info[2] = cost
                    predecessor[successor] = tuple(successor_info)

                    prev_evaluation = problem.heuristic(successor)
                    evaluation = problem.heuristic(successor)

                    if((successor,prev_evaluation) in frontier):
                        frontier.remove((successor,prev_evaluation))
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
    sol,cost,final_state = greedy_best_first(problem)
    time_after = datetime.datetime.now()

    if(cost == -1):
        print("No solution exists to this problem")
    else:
        for i in sol:
            print_action(i)
        problem.print_grid(final_state)
        print("Time taken: ",time_after-time_before)


