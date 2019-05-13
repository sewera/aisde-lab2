#!/bin/bash

if [[ $(cat ./src/control.h | grep -e "^#define NUMER_INDEKSU *999999") ]]
then
  read -p "Input your student id no.: " id_no
  sed -i -e "s/^#define NUMER_INDEKSU *[0-9]*/#define NUMER_INDEKSU $id_no/g" ./src/control.h
fi

read -p "Enter exercise number [2/3]: " ex_no
if [[ "$ex_no" -eq 2 ]]
then
  sed -i -e "s/^#define CWICZENIE_2 *.../#define CWICZENIE_2 tak/g" ./src/control.h
else
  sed -i -e "s/^#define CWICZENIE_2 *.../#define CWICZENIE_2 nie/g" ./src/control.h
fi

sed -i -e "s/^#define WYPISZ_NA_KONSOLE tak/#define WYPISZ_NA_KONSOLE nie/g" ./src/control.h

read -p "Enter filename (without an extension): " filename
filename=$(echo $filename | sed -e "s/ /_/g")

read -p "Enter tested array sizes (space separated): " values
if [ -z "$values" ]
then
  values="50 150 250 500 1000 1500 2000 2500 5000 10000\
  15000 20000 25000 30000 40000 50000 60000 75000 85000 100000\
  125000 150000 200000 250000 300000 400000 500000 600000 700000\
  800000 900000 1000000 1025000 1050000 1075000 1100000 1250000 1500000 1750000 2000000"
fi
count=$(echo $values | wc -w)
pass=0

if [[ "$ex_no" -eq 3 ]]
then
  read -p "Repeating values? [0/1]: " repeat
fi

make clean > /dev/null # delete all binaries; -j 4 or -j 2 for multi-threading
echo "[I] Removed binaries"

mkdir -p out/pdf
rm -f ./out/$filename.json
rm -f ./out/$filename\_count.json

echo -ne "[\n" >> ./out/$filename.json
echo -ne "[ " >> ./out/$filename\_count.json

echo "[I] Started sample collection"

for N in $values
do
  ((pass=pass+1))
  sed -i -e "s/^#define LICZNOSC *[0-9]*/#define LICZNOSC $N/g" ./src/control.h
  if [[ "$ex_no" -eq 3 && "$repeat" -eq 1 ]]
  then
    sed -i -e "s/^#define MAX_WARTOSC_KLUCZA *[0-9]* *\/\//#define MAX_WARTOSC_KLUCZA $(($N/100)) \/\//g" ./src/control.h
  elif [[ "$ex_no" -eq 3 && "$repeat" -eq 0 ]]
  then
    sed -i -e "s/^#define MAX_WARTOSC_KLUCZA *[0-9]* *\/\//#define MAX_WARTOSC_KLUCZA 0 \/\//g" ./src/control.h
  fi

  rm -f ./aisde23 ./bin/main.o
  make > /dev/null # -j 4 or -j 2 for multi-threading

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

python3 plot.py -l out/$filename.json out/$filename\_count.json
# You may have to change python3 to python on OSX

echo "[I] Plots should be in out/ directory"
echo
echo "Tip: you can compare on one plot two or more different algorighms"
echo "Usage: python3 plot.py -c <input_file0>,<input_file1>,... -u <in_file_count>"
echo " for example:"
echo "python3 plot.py -c out/shell_knuth.json,out/shell_sedgewick.json,out/shell_tokuda.json -n out/shell_knuth_count.json"
echo "When comparing, use the same array sizes across all algorithms"
echo "-> If you find this script usable in any way,"
echo "-> feel free to star me on github: https://github.com/jazzsewera/"
