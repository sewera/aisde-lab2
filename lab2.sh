#!/bin/bash

if [[ $(cat ./src/control.h | grep -e "^#define NUMER_INDEKSU *999999") ]]
then
  read -p "Input your student id no.: " id_no
  sed -i -e "s/^#define NUMER_INDEKSU *[0-9]*/#define NUMER_INDEKSU $id_no/g" ./src/control.h
fi

sed -i -e "s/^#define WYPISZ_NA_KONSOLE tak/#define WYPISZ_NA_KONSOLE nie/g" ./src/control.h

read -p "Enter filename (without an extension): " filename
read -p "Enter tested values (space separated): " values
if [ -z "$values" ]
then
  values="50 150 250 500 1000 1500 2000 2500 5000 10000\
  15000 20000 25000 30000 40000 50000 60000 75000 85000 100000\
  125000 150000 200000 250000 300000 400000 500000 600000 700000\
  800000 900000 1000000"
fi
count=$(echo $values | wc -w)
pass=0

make clean > /dev/null # delete all binaries
echo "[I] Removed binaries"

mkdir -p out

echo -ne "[\n" >> ./out/$filename.json
echo -ne "[ " >> ./out/$filename\_count.json

echo "[I] Started sample collection"

for N in $values
do
  ((pass=pass+1))
  sed -i -e "s/^#define LICZNOSC [0-9]*/#define LICZNOSC $N/g" ./src/control.h

  rm -f ./aisde23 ./bin/main.o
  make > /dev/null
  echo -n "."

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
echo "OK"
echo "[S] Done collecting samples"

echo -ne "]\n" >> ./out/$filename.json
echo -ne "]\n" >> ./out/$filename\_count.json

python3 plot.py out/$filename.json out/$filename\_count.json
echo "[I] Plots should be in out/ directory"
