def getNeighbors_prim(x):
    return [(x[0]-2,x[1]),(x[0],x[1]-2),(x[0]+2,x[1]),(x[0],x[1]+2)]
def getNeighbors_pf(x):
    return [(x[0]-1,x[1]),(x[0],x[1]-1),(x[0]+1,x[1]),(x[0],x[1]+1)]   
def l2(a,b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2
def isValid(x,w, h):
    return 0 <= x[0] < w and 0 <= x[1] < h
def getMiddle(a, b):
    return (a[0] + b[0])//2, (a[1]+b[1])//2