# Utilities for the second and third lab class in aisde
Please read this readme carefully.

Nine hours of life wasted, hope someone, someday will have easier life because of it.

For your convenience, please install git, then type:
```bash
git clone https://github.com/jazzsewera/aisde-lab2.git
```
if you want to check out new improvements in this script, type:
`git pull` from the repo directory.

## Usage
First, check if you have python3 installed. If you are not sure, type in:
```bash
python3 --version
```
if you see `Python 3.6.x` or `Python 3.7.x`, you are almost all set. If not,
`sudo apt install python3` for Debian-based distros (incl. Ubuntu)

`sudo pacman -S python3` for Arch-based distros (eg. Manjaro)

Then you need to install python packages. `cd` to this repo, then type:
```bash
sudo -H pip3 install -r requirements.txt
```
if the command does not exist, try: `sudo -H python3 -m pip install -r requirements.txt`

If you see `No module named pip`, install `pip` package:

`sudo apt install python3-pip` for Debian-based

`sudo pacman -S python-pip` for Arch-based

Set desired parameters in `src/control*` files, then:
```bash
./lab.sh
```
and follow the instructions. Oh, and of course, you will also need `make` and `g++`

### Hint
Choose filename accordingly to the algorithm you want to test. Eg. `quick_lomuto` or `heap_leaf_root_exchange`.  
You can type it with underscores (`_`) or with spaces (` `), which will be automatically converted to underscores.

### Performance
To improve the performance slightly,
edit the following lines in `lab.sh`:
```bash
# << @63
  make > /dev/null # -j 4 or -j 2 for multi-threading
# >> @63
  make -j 4 > /dev/null # -j 4 or -j 2 for multi-threading
```
change this `4` to the number of CPU cores that you have.

Usage of comparison of two or more algorithms is explained in lab.sh file.

Everyting mine licensed under MIT license. If stated otherwise (different copyright claim), the code is 2019 (C) Błażej Sewera

Everything not mine has no explicit license statement. Please do not use this code unless having a permission, verbal or written from people stated in copyright claims.

Works quite well on Linux, did not test on other platforms

-----------------------------

As always, made with <3 by [jazz](https://github.com/jazzsewera)
