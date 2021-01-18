from HelperFunctionsCSP import *

class Crossword_problemCSP:
    def __init__(self,dimensions,initial_grid,dictionary):
        self.dimensions = dimensions
        self.initial_grid = initial_grid
        self.dictionary = dictionary
    

#Initializes the variables dictionary. The key has the format (coordinates,mode) and the value has the format (coordinates,mode,length,intersections,assigned_value)
#The value format is changed after the domain and the constraints dictionaries are defined to only contain the assigned value, as this is the only needed field afterwards.
    def initialize_variables(self):
        variables = {}
        for i in range(len(self.initial_grid)):
            for j in range(len(self.initial_grid[i])):
                if(not is_wall_cell(i,j,self.initial_grid)):
                    mode = is_word_beginning_cell(i,j,self.initial_grid,self.dimensions)
                    if(mode == "Vertical" or mode == "Horizontal"):
                        
                        length_and_intersections = get_word_length_and_intersections(self.initial_grid,i,j,mode,self.dimensions)
                        length = length_and_intersections[0]
                        intersections = length_and_intersections[1]
                        variables[((i,j),mode)] = [(i,j),mode,length,intersections,-1]
                        
                    elif(mode == "VerticalHorizontal"):
                        mode = "Vertical"
                        length_and_intersections = get_word_length_and_intersections(self.initial_grid,i,j,mode,self.dimensions)
                        length = length_and_intersections[0]
                        intersections = length_and_intersections[1]
                        variables[((i,j),mode)] = [(i,j),mode,length,intersections,-1]
                                                
                    
                        mode = "Horizontal"
                        length_and_intersections = get_word_length_and_intersections(self.initial_grid,i,j,mode,self.dimensions)
                        length = length_and_intersections[0]
                        intersections = length_and_intersections[1]
                        variables[((i,j),mode)] = [(i,j),mode,length,intersections,-1]
                                             
                        mode = "VerticalHorizontal"
        return variables

#Initializes the domain dictionary. The key has the format (coordinates,mode) and the value is a list of valid words for the variable 
    def initialize_domain(self,variables):
        domain = {}
        for i in variables.values():
            key = (i[0],i[1])
            domain[key] = []

        for i in self.dictionary:
            for j in variables.values():
                variable_length = j[2]
                if (len(i) == variable_length):
                    coordinates = j[0]
                    mode = j[1]
                    key = (coordinates,mode)
                    domain[key].append(i)
        return domain

#Initializes the constraints dictionary. The key has the format (coordinates,mode) and the value is a list of tuples
#Where each tuple consists of three entries: They key to the constrained variable, the index of intersection relative to the constraining variable
#and the index of intersection relative to the constrained variable
    def initialize_constraints(self,variables):
        constraints = {}
        for i in variables.values():
            intersections = i[3]
            mode = i[1]
            coordinates = i[0]
            key = (coordinates,mode)
            constraints[key] = get_variable_constraints(intersections,mode,self.initial_grid)
        return constraints

#Returns the initial state dictionary. A state for a CSP problem is a dictionary which was fours keys: "Variables","Domain","Constraints", and"Grid"
#and they contain the variables dictionary, the domain dictionary, the constraints dictionary, and the grid respectively
    def initial_state(self):
        state = {}
        variables = self.initialize_variables()
        domain = self.initialize_domain(variables)
        constraints = self.initialize_constraints(variables)

        for key,value in variables.items():
            variables[key] = value[4]

        state["Variables"] = variables
        state["Domain"] = domain
        state["Constraints"] = constraints
        state["Grid"] = self.initial_grid
        return state


        
    
    

        

    
