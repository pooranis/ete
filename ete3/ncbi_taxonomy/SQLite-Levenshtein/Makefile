CC = gcc-12

levenshtein.sqlext: src/levenshtein.c
	$(CC) -Wall -shared -fPIC -I/usr/local/opt/sqlite/include -L/usr/local/opt/sqlite/lib -o levenshtein.sqlext src/levenshtein.c
##	$(CC) -Wall -shared -fPIC -Isqlite3 -o levenshtein.sqlext src/levenshtein.c

clean:
	rm levenshtein.sqlext
