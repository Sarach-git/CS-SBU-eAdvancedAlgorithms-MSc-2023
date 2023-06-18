def mul(a,b):
    # Meshkat Ahmadi
    
    len1 = len(str(a))
    len2 = len(str(b))
    
    # max length of a,b
    n = max(len1, len2)
    
    # ending condition
    if n ==1:
        return a*b
    
    # adding zeros to the smaller number
    if len1 < len2:
        a = ''.join(['0']*(len2-len1)) + str(a)
        b = str(b)
    else:
        a = str(a)        
        b = ''.join(['0']*(len1-len2)) + str(b)
    
    # turning a into halfs
    a1 = int(a[0:int(n/2)])
    a2 = int(a[int(n/2)::])   
    b1 = int(b[0:int(n/2)])
    b2 = int(b[int(n/2)::])    
    
    # half zeros count
    halfns = n-int(n/2)
    
    # recursive def. of multiplication
    x = int(str(mul(a1,b1))+''.join(['0']*halfns*2))
    y = int(str((mul(a2,b1)+mul(a1,b2)))+''.join(['0']*halfns))
    z = mul(a2,b2)
    
    return x+y+z