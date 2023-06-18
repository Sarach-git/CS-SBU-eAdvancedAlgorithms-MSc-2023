def trace(source, dest, edges, totalDistance, path, lastIndex):
    for i in range(0, len(edges)):
        # if the source of the edge is equal to our source and the target is the same too, return the distance and update the path
        if(edges[i][0] == source and edges[i][1] == dest):
            result = totalDistance + edges[i][2] , (path + str(edges[i][1]))
            edges.pop(i)
            return result
        
        # if the source of the edge is the same with our source, but target is not, and we have not visited this node, call this function recursively
        if(edges[i][0] == source and not path.__contains__(str(source))):
            nextNode = trace(edges[i][1], dest, edges, totalDistance + edges[i][2], (path + str(edges[i][1])), i)                
            return nextNode
        
    edges.pop(lastIndex)

N, M = map(int, input().split())
edges = []
for _ in range(M):
    A, B, C = map(int, input().split())
    edges.append((A, B, C))

edges.sort(key= lambda item : item[0])

# create a n x n array to find the distance of each two nodes
minimumDistance = [[ float("inf") for i in range(N) ] for j in range(N) ]
for i in range(1, N + 1):
    for j in range(1, N + 1):
        tempGraph = edges.copy()
        if(i == j):
            minimumDistance[i-1][j-1]=0
        for _ in range(0, M):
            if(len(tempGraph) == 0):
                break
            result = trace(i,j,tempGraph,0,str(1),-1)
            minimumDistance[i-1][j-1] = result[0] if result != None and minimumDistance[i-1][j-1] > result[0] else minimumDistance[i-1][j-1]
        # print(result)

for row in range(0, len(minimumDistance)):
    for col in range(0,len(minimumDistance[row])):
        print("distance(" + str(row) + "," + str(col) + "): " + str(minimumDistance[row][col]))