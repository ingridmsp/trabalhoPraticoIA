#import numpy 
import sys

def main():
	file = sys.argv[1]
	F = open(file,"r")
	for line in F:
		words = line.split()
		print words[0]	

if __name__ == '__main__':
	main()

#def kmeans(centroids,K,it):
	
