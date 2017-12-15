#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

typedef struct elemento{
	char nome[50];
	float x;
	float y;
	int cluster;
} Elemento;

typedef struct cluster{
	int id;
	int qt_elementos;
	Elemento **elem;
} Cluster;

typedef struct clusters{
	Cluster *c;
	int qt_clusters;
	int total_elementos;
} Clusters;

typedef struct retorno{
	int menor[2];
	float **matriz;
} Retorno;

typedef struct distancias{
	int id1;
	float *distancia;
} Distancias;

void le_arquivo(char *arquivo, Elemento *el, int n_linhas);

int conta_linhas(char *arquivo);

Retorno cria_matriz(float **matriz, int tam, Elemento *el);

float calc_dist(Elemento el1, Elemento el2);

void merge(int *menor, float **matriz, int tam_el, Elemento *el, Clusters *clus);

void exibe_clusters(Clusters clus);

void recalcula_dist(float **matriz, int tam, Elemento *el, int id, Clusters *clus);

void exibe_matriz(float **matriz, int tam);

Retorno pega_menor(float **matriz, int tam);

void exibe_elementos(Elemento *el, int tam);

void salvar(Clusters clus, char *nome_arquivo);

int main(int argc, char *argv[]){
	int kmin, kmax, tam_el, continua = -2;
	char *ptr, nome_arquivo[100];
	float **matriz;
	double time_spent;
	Clusters clus;
	Elemento *el;
	Retorno ret;
	clock_t begin = clock();
	clock_t end;
	

	kmin = strtol(argv[2], &ptr, 10);
	kmax = strtol(argv[3], &ptr, 10);
	
	tam_el = conta_linhas(argv[1]);
	el = (Elemento *) malloc(tam_el * sizeof(Elemento));
	
	clus.qt_clusters = 0;
	clus.total_elementos = 0;
	clus.c = (Cluster *) malloc(tam_el * sizeof(Cluster));
	
	le_arquivo(argv[1], el, tam_el);
	
	ret = cria_matriz(matriz, tam_el, el);
	matriz = ret.matriz;

//	exibe_matriz(matriz, tam_el);	printf("\n\n");
//	exibe_elementos(el, tam_el);	printf("\n\n");

	merge(ret.menor, matriz, tam_el, el, &clus);

//	exibe_matriz(matriz ,tam_el);	printf("\n\n\n");
//	exibe_elementos(el, tam_el);	printf("\n\n\n");
	
	//para usar os K: de max a min clusters. Fiz cagado. Como arrumar?
	//acho que se fizer a conta os k clusters contem todos os elems (conta pelo n de elementos dos clusters); usar total_elementos de Clusters;
	while(continua){
		ret = pega_menor(matriz, tam_el);
//		printf("ret: i: %d, j: %d\n", ret.menor[0], ret.menor[1]);

		printf("Rodando.\n");

		merge(ret.menor, matriz, tam_el, el, &clus);
		if(clus.total_elementos == tam_el){
			if(clus.qt_clusters <= kmax){
				if(clus.qt_clusters == kmin){
					continua = 0;
				}
				
				sprintf(nome_arquivo, "Resultado %s  -%d-", argv[1], clus.qt_clusters);
				salvar(clus, nome_arquivo);
			}
		}
		
		printf("Rodando...\n");

//		printf("n total em cluster: %d\n", clus.total_elementos);
		
//		exibe_matriz(matriz ,tam_el);	printf("\n\n\n");
//		exibe_elementos(el, tam_el);	printf("\n\n\n**************************************************\n");
//		continua++;
	}
	
//	exibe_matriz(matriz, tam_el);	printf("\n\n");
//	exibe_elementos(el, tam_el);	printf("\n\n");
	exibe_clusters(clus);
	
	end = clock();
	time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
	
	printf("A resposta foi salva nos arquivos!\nTempo de execucao: %lf segundos\n", time_spent);
	return 0;
}


void le_arquivo(char *arquivo, Elemento *el, int n_linhas){
	int i;
	char linha[100], *token, x[25], y[25], *ptr;
	FILE *f;
	
	f = fopen(arquivo, "r");
	if(f == NULL){
		printf("Erro ao abrir o arquivo!\n");
		return;
	}
	
//	printf("%d", n_linhas);
	
	fgets(linha, 100, f);
	
	for(i=0;i<n_linhas;i++){
		memset(linha, '\0', 100);
		
		fgets(linha, 100, f);
		
		token = strtok(linha, "\t");
		strcpy(el[i].nome, token);
	
		token = strtok(NULL, "\t");
		strcpy(x, token);

		token = strtok(NULL, "\n");
		strcpy(y, token);

		el[i].x = (float) strtod(x,NULL);
		el[i].y = (float) strtod(y,NULL);
		
		el[i].cluster = -1;
//		printf("%s %f %f\n\n", el[i].nome, el[i].x, el[i].y);
	}	
	fclose(f);
}

int conta_linhas(char *arquivo){
	int linhas = 0;
	char ch;
	FILE *fp;
	
	fp = fopen(arquivo, "r");
	
	while(!feof(fp)){
		ch = fgetc(fp);
		if(ch == '\n'){
			linhas++;
		}
	}
	
	fclose(fp);
	return linhas - 1;		//-1 pra nao contar a primeira dos nomes
}

Retorno cria_matriz(float **matriz, int tam, Elemento *el){
	int i, j, *menor_el;
	float menor;
	Retorno ret;
	
	menor_el = (int *) malloc(2 * sizeof(int));
	
	matriz = (float**) malloc(tam * sizeof(float*));
	for(int i = 0; i < tam; i++){
		matriz[i] = (float *) malloc(tam * sizeof(float));
	}
	
	menor = calc_dist(el[1], el[0]);
	
	for(i=0;i<tam;i++){
		for(j=0;j<tam;j++){
			if(j > i){
				matriz[i][j] = -1;
			}
			else if(i == j){
				matriz[i][j] = 0;
			}
			else{			
				matriz[i][j] = calc_dist(el[i], el[j]);
				if(matriz[i][j] < menor){
					ret.menor[0] = i;
					ret.menor[1] = j;
					
					menor = matriz[i][j];
				}
			}
		}
	}
//	printf("tam: %d\tmenor: %d %d %f\n\n", tam, menor_el[0], menor_el[1], menor);

	ret.matriz = matriz;

	return ret;
}

float calc_dist(Elemento el1, Elemento el2){
	return sqrt(((el1.x - el2.x) * (el1.x - el2.x))  +  ((el1.y - el2.y) * (el1.y - el2.y)));
}

void merge(int *menor, float **matriz, int tam_el, Elemento *el, Clusters *clus){
	int i, j, k, l, qt, teste, id, idaux;
	Elemento **aux;
	
	i = menor[0];
	j = menor[1];
	qt = clus->qt_clusters;
	
//			printf("n clusters: %d\n", clus->qt_clusters);
	
	if(el[i].cluster == -1 && el[j].cluster == -1){
	
//		printf("entrou aqui1\n"); //scanf(" %d", &teste);
	
		//SIGNIFICA QUE OS DOIS ELEMENTOS A SEREM JUNTADOS NÃO PERTECEM A UM CLUSTER
		clus->c[qt].id = qt;
		clus->c[qt].qt_elementos = 2;
		clus->c[qt].elem = (Elemento **) malloc(2 * sizeof(Elemento*));
		clus->c[qt].elem[0] = &el[i];
		clus->c[qt].elem[1] = &el[j];
		
		el[i].cluster = qt;
		el[j].cluster = qt;
		
		
		clus->qt_clusters++;
		recalcula_dist(matriz, tam_el, el, qt, clus);

		clus->total_elementos = clus->total_elementos + 2;
	}
	else if(el[i].cluster != -1 && el[j].cluster == -1){
//			printf("entrou aqui2\n"); //scanf(" %d", &teste);
		//SIGNIFICA QUE O ELEMENTO i PERTENCE A UM CLUSTER, MAS j NÃO
		id = el[i].cluster;
		el[j].cluster = id;
		
		aux = (Elemento **) malloc((clus->c[id].qt_elementos + 1) * sizeof(Elemento*));
		for(k=0;k<clus->c[id].qt_elementos;k++){
			aux[k] = clus->c[id].elem[k];
		}
		
		free(clus->c[id].elem);
		clus->c[id].elem = aux;
		
		
		clus->c[id].elem[clus->c[id].qt_elementos] = &el[j];
		clus->c[id].qt_elementos++;
		
//		printf("qt elementos: %d\n\n", clus->c[id].qt_elementos);
		
		clus->total_elementos++;
		recalcula_dist(matriz, tam_el, el, id, clus);		
	}
	else if(el[i].cluster == -1 && el[j].cluster != -1){
//			printf("entrou aqui3\n");// scanf(" %d", &teste);
		//SIGNIFICA QUE O ELEMENTO j PERTENCE A UM CLUSTER, MAS i NÃO
		id = el[j].cluster;
		el[i].cluster = id;
		
		aux = (Elemento **) malloc((clus->c[id].qt_elementos + 1) * sizeof(Elemento*));
		for(k=0;k<clus->c[id].qt_elementos;k++){
			aux[k] = clus->c[id].elem[k];
		}
		
		free(clus->c[id].elem);
		clus->c[id].elem = aux;
		
		clus->c[id].elem[clus->c[id].qt_elementos] = &el[i];
		clus->c[id].qt_elementos++;
		
		clus->total_elementos++;
		recalcula_dist(matriz, tam_el, el, id, clus);
	}
	else{
//		printf("entrou aqui4\n"); //scanf(" %d", &teste);

		//OS DOIS PERTENCEM A UM CLUSTER, FUSÃO DE CLUSTERS! TEEENSO
		//caso o cluster de i tenha id menor: (necessario sempre manter no menor para ficar consistente)
		if(el[i].cluster < el[j].cluster){
//			printf("entrou aqui\n5");// scanf(" %d", &teste);
			id = el[i].cluster;
			idaux = el[j].cluster;
		}
		//caso o cluster de j tenha id menor
		else if(el[j].cluster < el[i].cluster){
//			printf("entrou aqui6\n"); //scanf(" %d", &teste);
			id = el[j].cluster;
			idaux = el[i].cluster;
		}
			//copiando elementos do cluster de j para o de i:
			aux = (Elemento **) malloc((clus->c[id].qt_elementos + clus->c[idaux].qt_elementos) * sizeof(Elemento*));
			for(k=0;k<clus->c[id].qt_elementos;k++){
				aux[k] = clus->c[id].elem[k];
			}
			
			free(clus->c[id].elem);
			clus->c[id].elem = aux;
			
			for(k=0;k<clus->c[idaux].qt_elementos;k++){
				clus->c[id].elem[clus->c[id].qt_elementos] = clus->c[idaux].elem[k];
				clus->c[id].elem[clus->c[id].qt_elementos]->cluster = id;
				
				
//				printf("\n\nAQUIIIIIIIIIIIIIIII*\n");
//				printf("novo id: %d\n\n", clus->c[id].elem[clus->c[id].qt_elementos]->cluster);
//				exibe_elementos(el, tam_el);
				
				clus->c[id].qt_elementos++;
			}
			
			//apagando o cluster de j, dando shift e renomeando todos os clusters depois dele:
			for(k=idaux;k<clus->qt_clusters-1;k++){
				clus->c[k] = clus->c[k+1];
				for(l=0;l<clus->c[k].qt_elementos;l++){
					clus->c[k].elem[l]->cluster--;
				}
			}
			clus->c[k].elem = NULL;
			clus->qt_clusters--;
			
			recalcula_dist(matriz, tam_el, el, id, clus);
	}
}


void recalcula_dist(float **matriz, int tam, Elemento *el, int id, Clusters *clus){
	int i, j, k, l, teste, icluster, jcluster;
	float soma;
	Distancias *dists;
	
	dists = (Distancias *) malloc(clus->qt_clusters * sizeof(Distancias));
	for(i=0;i<clus->qt_clusters;i++){
		dists[i].id1 = i;
		dists[i].distancia = (float*) malloc(clus->qt_clusters * sizeof(float));
		for(j=0;j<clus->qt_clusters;j++){
			dists[i].distancia[j] = -1;
		}
		dists[i].distancia[i] = 0;
	}
	
/*	printf("\nDISTANCIAS");
	for(i=0;i<clus->qt_clusters;i++){
		printf("\n\ncluster %d:", i);
		for(j=0;j<clus->qt_clusters;j++){
			printf(" %f,", dists[i].distancia[j]);
		}
	}
	printf("\n\n\n");
	
	printf("TAMANHO: %d\n\n", tam);*/
	
	for(i=0;i<tam;i++){
		for(j=0;j<tam;j++){
			//só faz as contas para as iteracoes que nos interessam (sem repeticao, sem contar dist 0)
			if(j < i){
				if(matriz[i][j] == -2){
					soma = 0;
				}
				//para os casos de um pertencer a um cluster e outro não:
				//se o que não pertence a um cluster é j:
				else if(el[i].cluster == id && el[j].cluster == -1){
					soma = 0;
					for(k=0;k<clus->c[id].qt_elementos;k++){
						soma = soma + calc_dist(*(clus->c[id].elem[k]), el[j]);
					}
					soma = soma / clus->c[id].qt_elementos;
						
					matriz[i][j] = soma;
				}
				//se o que não pertence a um cluster é i:
				else if(el[i].cluster == -1 && el[j].cluster == id){
					soma = 0;
					for(k=0;k<clus->c[id].qt_elementos;k++){
						soma = soma + calc_dist(*(clus->c[id].elem[k]), el[i]);
					}
					soma = soma / clus->c[id].qt_elementos;
						
					matriz[i][j] = soma;
				}
				//se os dois pertencem ao mesmo cluster:
				else if(el[i].cluster == id && el[j].cluster == id){
					matriz[i][j] = -2;		//faz elementos do mesmo cluster ficarem com dist -2
				}
				//para os casos de os dois pertencerem a um cluster (nao o mesmo, chequei com o -2 de dist):
				//para os casos em que o cluster que demos merge ser o i:
				else if(el[i].cluster == id && el[j].cluster != -1){
					//checa se a distancia entre os dois já foi calcula (se sim, está guardada na struct dists); Se não:
					if(dists[el[i].cluster].distancia[el[j].cluster] == -1){
						//calcula a distancia de cada elemento pra cada elemento, armazena em soma, divide tudo no final por |clusterA|*|clusterB|
						soma = 0;
						for(k=0;k<clus->c[id].qt_elementos;k++){
							for(l = 0;l<clus->c[el[j].cluster].qt_elementos;l++){
								soma = soma + calc_dist(*(clus->c[id].elem[k]), *(clus->c[el[j].cluster].elem[l]));
							}
						}
						
					
						soma = soma / (clus->c[id].qt_elementos * clus->c[el[j].cluster].qt_elementos);
					
						matriz[i][j] = soma;
						
						//adicionando essa distância (reflexiva) na struct de distâncias:
						dists[el[i].cluster].distancia[el[j].cluster] = soma;
						dists[el[j].cluster].distancia[el[i].cluster] = soma;
						
//							printf("ENTROU AQUI ESPECIAL\n********************************\nDISTANCIAS");
//							printf("\n\n\n");
					}
					//Se sim:
					else{
//						printf("\n\ncopiando %f para m[%d][%d]\n\n", dists[el[i].cluster].distancia[el[j].cluster, i, j]);
						matriz[i][j] = dists[el[i].cluster].distancia[el[j].cluster];
					}
				}
				//para os casos em que o cluster que demos merge ser o j: (consultar o elseif acima para detalhes)
				else if(el[i].cluster != -1 && el[j].cluster == id){
//					printf("elicluster: %d, eljcluster: %d\n", el[i].cluster, el[j].cluster); //scanf(" %d", &teste);
				
					if(dists[el[j].cluster].distancia[el[i].cluster] == -1){
						soma = 0;
						for(k=0;k<clus->c[id].qt_elementos;k++){
							for(l = 0;l<clus->c[el[i].cluster].qt_elementos;l++){
								soma = soma + calc_dist(*(clus->c[id].elem[k]), *(clus->c[el[i].cluster].elem[l]));
							}
						}
					
						soma = soma / (clus->c[id].qt_elementos * clus->c[el[i].cluster].qt_elementos);
					
						matriz[i][j] = soma;
						
						dists[el[i].cluster].distancia[el[j].cluster] = soma;
						dists[el[j].cluster].distancia[el[i].cluster] = soma;
						
//							printf("ENTROU AQUI ESPECIAL\n********************************\nDISTANCIAS");						
					}
					else{
//						printf("\n\ndists eli cluster: %d, dists elj cluster: %d\n\n", dists[el[i].cluster].distancia[el[j].cluster]);
//						printf("\n\ncopiando %f para m%i %i com tam: %i\n\n", dists[el[i].cluster].distancia[el[j].cluster], i, j, tam);
						matriz[i][j] = dists[el[i].cluster].distancia[el[j].cluster];			//nao me preocupo com o que é i e o que é j porque a dist é reflexiva
					}
				}
			}
		}
	}
	
	for(i=0;i<clus->qt_clusters;i++){
		free(dists[i].distancia);
	}
	free(dists);
}

void exibe_clusters(Clusters clus){
	int i, j, k;
	
	printf("\n\n\n********************************\nqt clusters: %d\n\n", clus.qt_clusters);
	
	for(i=0;i<clus.qt_clusters;i++){
		printf("cluster id: %d\nqt_elementos: %d\n", clus.c[i].id, clus.c[i].qt_elementos);
		printf("\n");
		for(j=0;j<clus.c[i].qt_elementos;j++){
			printf("nome: %s\nx: %f\ny: %f\ncluster: %d\n\n", clus.c[i].elem[j]->nome, clus.c[i].elem[j]->x, clus.c[i].elem[j]->y, clus.c[i].elem[j]->cluster);
		}
	}
}

void exibe_matriz(float **matriz, int tam){
	//print da matriz pra teste:
	int i, j;
	for(i=0;i<tam;i++){
		for(j=0;j<tam;j++){
			printf("%f\t", matriz[i][j]);
		}
		printf("\n");
	}
}

void exibe_elementos(Elemento *el, int tam){
	//print dos elementos pra teste:
	int i, j;
	for(i=0;i<tam;i++){
		printf("nome: %s\nx: %f\ny: %f\ncluster: %d", el[i].nome, el[i].x, el[i].y, el[i].cluster);
		printf("\n");
	}
}


Retorno pega_menor(float **matriz, int tam){
	int i, j, teste, flag =0;
	float menor;
	Retorno ret;
	

	for(i=0;i<tam;i++){
		for(j=0;j<tam;j++){
			if(matriz[i][j] > 0){
				if(flag == 0){
					menor = matriz[i][j];
					ret.menor[0] = i;
					ret.menor[1] = j;
					
					flag = 1;
				}				
				else if(matriz[i][j] < menor){
					ret.menor[0] = i;
					ret.menor[1] = j;
				
					menor = matriz[i][j];
				}
			}
		}
	}
	
//	printf("menor: %f\n", menor);

	ret.matriz = matriz;
	return ret;
}

void salvar(Clusters clus, char *nome_arquivo) {
	int i, j;
	FILE *arquivo;

	arquivo = fopen(nome_arquivo, "w"); //cria novo arquivo

	for(i=0;i<clus.qt_clusters;i++){       //para cada cluster
		for(j=0;j<clus.c[i].qt_elementos;j++){   //para cada elemento
			fprintf(arquivo,"%s\t%d\n", clus.c[i].elem[j]->nome, clus.c[i].elem[j]->cluster); //escreve registros
		}
	}
    
	fclose(arquivo);
}
