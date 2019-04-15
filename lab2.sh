#!/bin/bash

if [[ $(cat ./src/control.h | grep -e "^#define NUMER_INDEKSU *999999") ]]
then
  read -p "Podaj nr indeksu: " id_no
  sed -i -e "s/^#define NUMER_INDEKSU *[0-9]*/#define NUMER_INDEKSU $id_no/g" ./src/control.h
fi

sed -i -e "s/^#define WYPISZ_NA_KONSOLE tak/#define WYPISZ_NA_KONSOLE nie/g" ./src/control.h

read -p "Podaj nazwe pliku dla tego algorytmu (bez rozszerzenia): " filename
read -p "Podaj badane wartosci: " values
count=$(echo $values | wc -w)
pass=0

mkdir -p out

echo -ne "[\n" >> ./out/$filename.json
echo -ne "[ " >> ./out/$filename\_count.json

for N in $values
do
  ((pass=pass+1))
  sed -i -e "s/^#define LICZNOSC [0-9]*/#define LICZNOSC $N/g" ./src/control.h

  rm -f ./aisde23 ./bin/main.o
  make

  ./aisde23 | tail -n 1 >> ./out/$filename.json
  if (( $pass != count ))
  then
    echo -ne "$N, " >> ./out/$filename\_count.json
    echo -ne ",\n" >> ./out/$filename.json
  else
    echo -ne "$N " >> ./out/$filename\_count.json
    echo -ne "\n" >> ./out/$filename.json
  fi
done

echo -ne "]\n" >> ./out/$filename.json
echo -ne "]\n" >> ./out/$filename\_count.json
