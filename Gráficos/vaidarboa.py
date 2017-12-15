import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors
import numpy as np
x = []
y = []
z = []

with open("monkey.txt") as f:
	for line in f:
		content = line.split("\t")
		x.append(content[1])
		y.append(content[2].split("\n")[0])

with open("MonkeyReal1.clu") as f:
	for line in f:
		content = line.split("\t")
		z.append((content[1]).split("\n")[0])






#N = 4000

#z =  np.random.rand(N)
print(z)

plt.scatter(x, y, c=z)
plt.show()
