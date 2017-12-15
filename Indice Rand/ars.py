import sys
from sklearn import metrics

def main():
    file1 =sys.argv[1]
    file2 =sys.argv[2] # pega os objetos em ordem de nome em um vetor onde cada valor eh o numero do cluster que ele esta
    F = open(file1,"r") # particoes reais
    labels_true = []
    for line in F:
        words = line.replace('\n', '').split('\t')
        labels_true.append(int(words[1]))
    F.close()

    F2 = open(file2,"r") #resultados do algoritmo
    labels_pred = []
    for line in F2:
        words = line.replace('\n', '').split('\t')
        labels_pred.append(int(words[1]))
    F2.close()
    print(metrics.adjusted_rand_score(labels_true, labels_pred))

if __name__ == '__main__':
	main()
