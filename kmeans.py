import sys
from math import sqrt
import numpy as np

dic = {} # dicionario que possui ids e coordenadas
d = {} # estrutura resultante da iteracao
sumx = [] # soma valores em x (pra cada cluster)
sumy = [] # soma valores em y (pra cada cluster)
nums = [] # quantidade de elementos em cada cluster
keys = [] # vetor de ids 

def main():
	file = sys.argv[1]
	k = int(sys.argv[2])
	iterations = int(sys.argv[3])
	#centroids = ["11.111,8.644","13.222,5.444","8.988,11.444"] # so pra teste aleatorio
	centroids = ["1.0,1.0","5.0,7.0"]
	# for i in range(0,k):
	#    centroids[i].append(str(randomx)+","+str(randomy))
	sumx = [0]*k
	sumy = [0]*k
	nums = [0]*k
	
	F = open(file,"r")
	c = 0
	for line in F:
	    if c != 0 : # ignora a primeira linha do arquivo
		    words = line.split() # pega cada linha e faz o split nos espacos em branco
		    point = words[1],words[2] # coordenadas
		    dic[words[0]] = point
		    keys.append(words[0])
	    c = c+1
	F.close()
	res = kmeans(centroids,k,iterations,sumx,sumy,nums)
	
	file = file.split('.')
	file =file[0]+"Result.clu"
	arq = open(file,"w")

	for x in range(0,len(res)):
		arq.write(keys[x]+"	"+str(d[keys[x]])+'\n')	 		
	
	arq.close()
def kmeans(cent,k,it,sumx,sumy,nums):
    c = cent
    for x in range(0,it):
        d = aux(c,k,it,sumx,sumy,nums) # faz uma iteracao
    
    for a in range(0,k):
	    if nums[a] > 0 :
	        c[a] = str(sumx[a]/nums[a])+","+str(sumy[a]/nums[a]) # recalcula os centroids       
    return d	

	
def aux(cent,k,it,sumx,sumy,nums):

    for b in range(0,k): # zera as somas e numero de elementos de cada cluster
        sumx[b] = 0
        sumy[b] = 0
        nums[b] = 0
    
    for i in range(len(keys)): 
        c = cent[0].split(',') # faz o split pra pegar os valores do centroid 
        menor = sqrt((pow(float(dic[keys[i]][0])-float(c[0]),2)) + (pow(float(dic[keys[i]][1])-float(c[1]),2))) # seta o menor valor
        num = 0 # seta o valor de qual centroid o ponto pertence ate o momento
        for z in range(1,k):
            c = cent[z].split(',')
            dist = sqrt((pow(float(dic[keys[i]][0])-float(c[0]),2)) + (pow(float(dic[keys[i]][1])-float(c[1]),2)))
            if dist < menor:
                menor = dist
                num = z
                
        d[keys[i]] = num 

	# atualiza as somas e numero de elementos do cluster
        sumx[num] += float(dic[keys[i]][0])
        sumy[num] += float(dic[keys[i]][1])
        nums[num] += 1
            
    return d	

if __name__ == '__main__':
	main()
