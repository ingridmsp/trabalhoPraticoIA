import sys
from math import sqrt

dic = {}
d = {}
keys = []

def main():
	file = sys.argv[1]
	k = int(sys.argv[2])
	iterations = int(sys.argv[3])
	centroids = ["11.111,8.644","13.222,5.444","8.988,11.444"] # so pra teste aleatorio
	# for i in range(0,iterations):
	#    centroids[i].append(str(randomx)+','+str(randomy))
	sumx = [0]*iterations
	sumy = [0]*iterations

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
	res = kmeans(centroids,k,iterations,sumx,sumy)
	#print(res)


def kmeans(cent,k,it,sumx,sumy):
    c = cent
    for x in range(0,it):
        print(c)
        d = aux(c,it,sumx,sumy)
        for a in range(0,it):
            c[a] = str(sumx[a]/len(keys))+","+str(sumy[a]/len(keys))

    return d

def aux(cent,it,sumx,sumy):

    for b in range(0,it):
        sumx[b] = 0
        sumy[b] = 0

    for i in range(len(keys)):
        c = cent[0].split(',')
        menor = sqrt((pow(float(dic[keys[i]][0])-float(c[0]),2)) + (pow(float(dic[keys[i]][1])-float(c[1]),2)))
        num = 0
        for z in range(1,it):
            c = cent[z].split(',')
            dist = sqrt((pow(float(dic[keys[i]][0])-float(c[0]),2)) + (pow(float(dic[keys[i]][1])-float(c[1]),2)))
            if dist < menor:
                menor = dist
                num = z

        d[keys[i]] = num
        sumx[num] += float(dic[keys[i]][0])
        sumy[num] += float(dic[keys[i]][1])

    return d

if __name__ == '__main__':
	main()
