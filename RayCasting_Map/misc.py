import numpy as np  

# zerosout = np.zeros((50,30),dtype=np.int8)

# np.savetxt("test.csv", zerosout.T, delimiter=",", fmt="%2i")

# zerosin = np.loadtxt("test.csv", delimiter=",").T
# print(zerosin)

class Spot:
    def __init__(self, x: np.int8, y: np.int8, blocked: np.int8) -> None:
        self.x = x
        self.y = y
        self.blocked = blocked

spots = np.ndarray((50,30), Spot)
for x in range(50):
    for y in range(30):
        spots[x,y] = Spot(x=x, y=y, blocked=1)

print(spots[5,1].x)