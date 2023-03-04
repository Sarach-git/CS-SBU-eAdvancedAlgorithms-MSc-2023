def zarb(m,n):
    if(m<10 or n<10): # if m and n are single digits
        return m*n
    else:
        mstring = str(m)
        nstring = str(n)
        k = max(len(mstring), len(nstring))
        mid=int(k/2)
            #finding a and c i.e. the higher bits for each number
        a = int(mstring[:-mid])
        c = int(nstring[:-mid])
            #finding b and d i.e. the lower bits for each number
        b = int(mstring[-mid:])
        d = int(nstring[-mid:])
            #finding ac, bd and ad_plus_bc
        ac = zarb(a, c)
        bd = zarb(b, d)
        ad_plus_bc = zarb(a + b, c + d) - ac - bd
        return ac*10**(2 * mid) + ad_plus_bc*10**(mid) + bd
print("Answer is:")
print(zarb(4563,2486))
