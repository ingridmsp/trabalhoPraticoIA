import sys
from math import sqrt

dic = {}
d = {}
keys = []

def main():
	file = sys.argv[1]
	k = int(sys.argv[2])
	iterations = int(sys.argv[3])
	centroids = {0:(11.111,8.644),1:(13.222,5.444),2:(8.988,11.444)} # so pra teste aleatorio
	# for i in range(0,iterations):
	#    centroids[i] = (randomx,randomy)
	
	F = open(file,"r")
	c = 0
	for line in F:
	    if c != 0 :
		    words = line.split()
		    point = words[1],words[2]
		    dic[words[0]] = point
		    keys.append(words[0])
	    c = c+1
	F.close()
	kmeans(centroids,k,iterations)
	
def kmeans(cent,k,it):

    for x in range(0,it):
	    for i in range(len(keys)):
	        menor = sqrt((pow(float(dic[keys[i]][0])-cent[0][0],2)) + (pow(float(dic[keys[i]][1])-cent[0][1],2)))
	        num = 0
	        for z in range(1,it):
	            dist = sqrt((pow(float(dic[keys[i]][0])-cent[z][0],2)) + (pow(float(dic[keys[i]][1])-cent[z][1],2)))
	            if dist < menor:
	                menor = dist
	                num = z
	                
	        d[keys[i]] = num

    print(d)            

def calcCentroid(clist):
	cont = 0
	sumx = 0
	sumy = 0
	for i in range(len(clist)):
		sumx = sumx + clist[0]
		sumy = sumy + clist[1]	
		cont = cont+1	

	r = (sumx/cont, sumy/cont)
	return r	

if __name__ == '__main__':
	main()
