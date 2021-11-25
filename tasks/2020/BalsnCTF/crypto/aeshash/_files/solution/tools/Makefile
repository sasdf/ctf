all: gen rev rec

gen: gen.c hash.c hash.h
	gcc -O3 -maes -msse4.1 -march=native -fopenmp gen.c hash.c -o gen

rev: rev.c hash.c hash.h
	gcc -O3 -maes -msse4.1 -march=native -fopenmp rev.c hash.c -o rev

rec: rec.c aes.c
	gcc -O3 -maes -msse4.1 -march=native -fopenmp rec.c -o rec
