

def checkTheivesTimes(theivesCount, gaurdBeingOutTime, A):
    #Checking if there is a theive who needs more time than the guard being out
    #Checking if the sum of time theives need is more than 2*time guard being out
    if(sum(A) > gaurdBeingOutTime * 2 or theivesCount > gaurdBeingOutTime * 2):
        return False
    
    for i in range(0, len(A)):
        if(A[i] > gaurdBeingOutTime):
            return False
        
    minimumSpaceNeeded = firstFit(A, len(A), gaurdBeingOutTime)
    print("minimum space needed: " + str(minimumSpaceNeeded))
        
    # checking if there is more than 2 bins needed for these theives
    return minimumSpaceNeeded <= 2

iterationTimes = int(input())

def firstFit(weight, n, c):
     
    # Initialize result (Count of bins)
    res = 0;
 
    # Create an array to store
    # remaining space in bins
    # there can be at most n bins
    bin_rem = [0]*n;
 
    # Place items one by one
    for i in range(n):
         
        # Find the first bin that
        # can accommodate
        # weight[i]
        j = 0;
         
        # Initialize minimum space
        # left and index
        # of best bin
        min = c + 1;
        bi = 0;
 
        for j in range(res):
            if (bin_rem[j] >= weight[i] and bin_rem[j] -
                                       weight[i] < min):
                bi = j;
                min = bin_rem[j] - weight[i];
             
        # If no bin could accommodate weight[i],
        # create a new bin
        if (min == c + 1):
            bin_rem[res] = c - weight[i];
            res += 1;
        else: # Assign the item to best bin
            bin_rem[bi] -= weight[i];
    return res;

for _ in range(iterationTimes):
    theivesCount, gaurdBeingOutTime = map(int, input().split())
    A = list(map(int, input().split()))
    
    A.sort()
    print(A)
    print(sum(A))

    result = checkTheivesTimes(theivesCount, gaurdBeingOutTime, A)
    
    if result:
        print("YES")
    else:
        print("NO")



