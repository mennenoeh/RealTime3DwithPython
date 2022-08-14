import numpy as np  

zerosout = np.zeros((50,30),dtype=np.int8)

# np.savetxt("test.csv", zerosout.T, delimiter=",", fmt="%2i")

# zerosin = np.loadtxt("test.csv", delimiter=",").T
# print(zerosin)

print(zerosout-1)