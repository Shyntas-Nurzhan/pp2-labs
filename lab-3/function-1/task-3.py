def puzzle(numheads,numlegs):
    rabbits = numlegs/2 - numheads
    chickens = numheads - (numlegs/2 - numheads)
    
    
    return rabbits , chickens 

numheads = 35
numlegs = 94

print(puzzle(numheads,numlegs))