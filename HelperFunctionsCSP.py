from HelperFunctionsSearch import is_intersection_cell,fill_grid

def is_wall_cell(i,j,grid):
    if(grid[i][j] == 0):
        return True
    else:
        return False


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

#Returns a list of constraints for a given variable, where we only need the list of intersections from the variable, and the variable mode
#(vertical of horizontal). Each constraint consists of: the key to the constrained variable, the index of intersection relative to the 
#constraining variable, and the index of intersection relative to the constrained variable.
def get_variable_constraints(intersections,mode,grid):
    #mode if related to V1 (input variable)
    if(mode == "Horizontal"):
        mode2 = "Vertical"
        constraints = []
        for i in intersections:
            L1 = i[1]
            L2 = 0
            x = i[0][0]
            y = i[0][1]
            while(True):
                if(x-1 > -1 and grid[x-1][y] != 0):
                    x = x-1
                    L2 += 1
                else:
                    break
            constraints.append((((x,y),mode2),L1,L2))
        return constraints
            

    elif(mode == "Vertical"):
        constraints = []
        mode2 = "Horizontal"
        for i in intersections:
            L1 = i[1]
            L2 = 0
            x = i[0][0]
            y = i[0][1]
            while(True):
                if(y-1 > -1 and grid[x][y-1] != 0):
                    y = y-1
                    L2 += 1
                else:
                    break
            constraints.append((((x,y),mode2),L1,L2))
        return constraints

