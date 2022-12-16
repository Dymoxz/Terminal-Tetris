board = [[0,16], [2,18], [3,17], [3,19], [1,16], [6,10], [0,15], [0,17]]
neeee = [[0,1], [2,2], [3,3], [3,7], [1,2]]
ylsit = []
for (a, b) in neeee:
    bList = [x[1] for x in board if x[0] == a]
    ylsit.append(min(bList))
print(ylsit)
print(min(ylsit))



