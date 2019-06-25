#!/usr/bin/env sh

CUR_EX='ex00'
cd $CUR_EX
cc decrypt.c main.c
# echo `./a.out '000010' '+' '000011'`
[[ `./a.out '000010' '+' '000011'` != '000101 (5)' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '000110' '+' '000001'` != '000111 (7)' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '000110' '+' '000000'` != '000110 (6)' ]] && echo "$CUR_EX failed test 2" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex01/
cc bit.c main.c
CUR_EX='ex01'
[[ `./a.out '0010' '&' '0000'` != '0000 (0)' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '0010' '&' '1111'` != '0010 (2)' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '0010' '&' '0010'` != '0010 (2)' ]] && echo "$CUR_EX failed test 2" && exit 1
[[ `./a.out '0010' '&' '1101'` != '0000 (0)' ]] && echo "$CUR_EX failed test 3" && exit 1
[[ `./a.out '0010' '&' '~1101'` != '0010 (2)' ]] && echo "$CUR_EX failed test 4" && exit 1
[[ `./a.out '0010' '|' '0000'` != '0010 (2)' ]] && echo "$CUR_EX failed test 5" && exit 1
[[ `./a.out '0010' '|' '1111'` != '1111 (15)' ]] && echo "$CUR_EX failed test 6" && exit 1
[[ `./a.out '0010' '|' '0010'` != '0010 (2)' ]] && echo "$CUR_EX failed test 7" && exit 1
[[ `./a.out '0010' '|' '1101'` != '1111 (15)' ]] && echo "$CUR_EX failed test 8" && exit 1
[[ `./a.out '~0010' '|' '1101'` != '1101 (13)' ]] && echo "$CUR_EX failed test 9" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex02/
cc 'shift.c' main.c
CUR_EX='ex02'
[[ `./a.out '000011' '<<' '2'` != '001100 (12)' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '101000' '>>' '3'` != '111101 (-3)' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '110100' '>>' '5'` != '111111 (-1)' ]] && echo "$CUR_EX failed test 2" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex03/
cc 'xor.c' main.c
CUR_EX='ex03'
[[ `./a.out '111111' '^' '010101'` != '101010 (42)' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '000000' '^' '101010'` != '101010 (42)' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '101101' '^' '101010'` != '000111 (7)' ]] && echo "$CUR_EX failed test 2" && exit 1
[[ `./a.out '101010' '^' '101010'` != '000000 (0)' ]] && echo "$CUR_EX failed test 3" && exit 1
[[ `./a.out '011111' '^' '101010'` != '110101 (53)' ]] && echo "$CUR_EX failed test 4" && exit 1
[[ `./a.out '110100' '^' '101010'` != '011110 (30)' ]] && echo "$CUR_EX failed test 5" && exit 1
[[ `./a.out '010101' '^' '101010'` != '111111 (63)' ]] && echo "$CUR_EX failed test 6" && exit 1
[[ `./a.out '111111' '^' '101010'` != '010101 (21)' ]] && echo "$CUR_EX failed test 7" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex04/
cc 'getPlace.c' main.c
CUR_EX='ex04'
[[ `./a.out '42' '0'` != 'Parking place 0: vacant' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '42' '1'` != 'Parking place 1: occupied' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '42' '2'` != 'Parking place 2: vacant' ]] && echo "$CUR_EX failed test 2" && exit 1
[[ `./a.out '42' '3'` != 'Parking place 3: occupied' ]] && echo "$CUR_EX failed test 3" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex05/
cc 'clearPlace.c' main.c
CUR_EX='ex05'
[[ `./a.out '42' '3'` != 'New parking row: 34' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '42' '5'` != 'New parking row: 10' ]] && echo "$CUR_EX failed test 1" && exit 1
rm -f a.out
echo "$CUR_EX Complete"


cd ../ex06/
cc 'setPlace.c' main.c
CUR_EX='ex06'
[[ `./a.out '42' '0'` != 'New parking row: 43' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '42' '2'` != 'New parking row: 46' ]] && echo "$CUR_EX failed test 1" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex07/
cc 'updatePlace.c' main.c
CUR_EX='ex07'
[[ `./a.out '42' '1' '0'` != 'Updated parking row: 40' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '42' '2' '1'` != 'Updated parking row: 46' ]] && echo "$CUR_EX failed test 1" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex08/
cc 'isFilled.c' main.c
CUR_EX='ex08'
[[ `./a.out '42'` != 'Parking row 42 is not filled from right to left' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '15'` != 'Parking row 15 is filled from right to left' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '1024'` != 'Parking row 1024 is not filled from right to left' ]] && echo "$CUR_EX failed test 2" && exit 1
[[ `./a.out '1023'` != 'Parking row 1023 is filled from right to left' ]] && echo "$CUR_EX failed test 3" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex09/
cc 'occupiedPlaces.c' main.c
CUR_EX='ex09'
[[ `./a.out '42'` != 'Parking row 42 has 3 occupied places' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '15'` != 'Parking row 15 has 4 occupied places' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '1024'` != 'Parking row 1024 has 1 occupied places' ]] && echo "$CUR_EX failed test 2" && exit 1
[[ `./a.out '1023'` != 'Parking row 1023 has 10 occupied places' ]] && echo "$CUR_EX failed test 3" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex10/
cc 'carPosition.c' main.c
CUR_EX='ex10'
[[ `./a.out '0'` != 'Parking row 0 has 1 car at position -1' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '1'` != 'Parking row 1 has 1 car at position 0' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '16'` != 'Parking row 16 has 1 car at position 4' ]] && echo "$CUR_EX failed test 2" && exit 1
[[ `./a.out '1024'` != 'Parking row 1024 has 1 car at position 10' ]] && echo "$CUR_EX failed test 3" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex11/
cc 'carPosition.c' main.c
CUR_EX='ex11'
[[ `./a.out '0'` != 'Parking row 0 has 1 car at position -1' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '1'` != 'Parking row 1 has 1 car at position 0' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '16'` != 'Parking row 16 has 1 car at position 4' ]] && echo "$CUR_EX failed test 2" && exit 1
[[ `./a.out '1024'` != 'Parking row 1024 has 1 car at position 10' ]] && echo "$CUR_EX failed test 3" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex12/
cc 'clearBits.c' main.c
CUR_EX='ex12'
[[ `./a.out '42' '4'` != 'Cleared parking row: 32' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '1023' '5'` != 'Cleared parking row: 992' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '1023' '9'` != 'Cleared parking row: 512' ]] && echo "$CUR_EX failed test 2" && exit 1
[[ `./a.out '367' '6'` != 'Cleared parking row: 320' ]] && echo "$CUR_EX failed test 3" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex13/
cc 'leftmostCar.c' main.c
CUR_EX='ex13'
[[ `./a.out '42'` != 'Parking row 42: the leftmost car is at position 5' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '15'` != 'Parking row 15: the leftmost car is at position 3' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '1024'` != 'Parking row 1024: the leftmost car is at position 10' ]] && echo "$CUR_EX failed test 2" && exit 1
[[ `./a.out '1023'` != 'Parking row 1023: the leftmost car is at position 9' ]] && echo "$CUR_EX failed test 3" && exit 1
[[ `./a.out '1022'` != 'Parking row 1022: the leftmost car is at position 9' ]] && echo "$CUR_EX failed test 4" && exit 1
[[ `./a.out '31'` != 'Parking row 31: the leftmost car is at position 4' ]] && echo "$CUR_EX failed test 5" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex14/
cc 'rightmostCar.c' main.c
CUR_EX='ex14'
[[ `./a.out '42'` != 'Parking row 42: the rightmost car is at position 1' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '15'` != 'Parking row 15: the rightmost car is at position 0' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '1024'` != 'Parking row 1024: the rightmost car is at position 10' ]] && echo "$CUR_EX failed test 2" && exit 1
[[ `./a.out '1023'` != 'Parking row 1023: the rightmost car is at position 0' ]] && echo "$CUR_EX failed test 3" && exit 1
[[ `./a.out '1022'` != 'Parking row 1022: the rightmost car is at position 1' ]] && echo "$CUR_EX failed test 4" && exit 1
[[ `./a.out '352'` != 'Parking row 352: the rightmost car is at position 5' ]] && echo "$CUR_EX failed test 5" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex15/
cc 'longestSequence.c' main.c
CUR_EX='ex15'
[[ `./a.out '42'` != 'Parking row 42: the longest sequence has 1 car(s)' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '15'` != 'Parking row 15: the longest sequence has 4 car(s)' ]] && echo "$CUR_EX failed test 1" && exit 1
[[ `./a.out '1024'` != 'Parking row 1024: the longest sequence has 1 car(s)' ]] && echo "$CUR_EX failed test 2" && exit 1
[[ `./a.out '1023'` != 'Parking row 1023: the longest sequence has 10 car(s)' ]] && echo "$CUR_EX failed test 3" && exit 1
[[ `./a.out '1022'` != 'Parking row 1022: the longest sequence has 9 car(s)' ]] && echo "$CUR_EX failed test 4" && exit 1
[[ `./a.out '352'` != 'Parking row 352: the longest sequence has 2 car(s)' ]] && echo "$CUR_EX failed test 5" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex16/
cc 'piano.c' main.c
CUR_EX='ex16'
if [[ ! -f 'song1.piano' ]]; then
	printf "32\n1 1 1 1 2 2 2 2 2 4 4 4 4 8 8 8 8 16 16 16 16\n" > song1.piano
fi
if [[ ! -f 'cmp_out' ]]; then
	echo "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
	echo "0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 " >> cmp_out
fi
./a.out 'song1.piano' > ./usr_out
[[ -n `diff ./usr_out ./cmp_out` ]] && echo "$CUR_EX failed test 0" && exit 1
rm -f a.out song1.piano usr_out cmp_out
echo "$CUR_EX Complete"

cd ../ex17/
cc 'correctSong.c' main.c
CUR_EX='ex17'
if [[ ! -f 'empty.piano' ]]; then
	printf "32\n0 0 0 0 0 0 0 0 0 0 0 0 0 0\n" >> 'empty.piano'
fi
./a.out 'empty.piano' '0' '1' '3' > ./usr_out
printf "32\n2 2 2 0 0 0 0 0 0 0 0 0 0 0 \n" > ./cmp_out
[[ -n `diff ./usr_out ./cmp_out` ]] && echo "$CUR_EX failed test 0" && exit 1
./a.out 'empty.piano' '3' '3' '6' > ./usr_out
printf "32\n0 0 0 8 8 8 8 8 8 0 0 0 0 0 \n" > ./cmp_out
[[ -n `diff ./usr_out ./cmp_out` ]] && echo "$CUR_EX failed test 1" && exit 1
rm -f a.out empty.piano usr_out cmp_out
echo "$CUR_EX Complete"

cd ../ex18/
cc 'isEqual.c' main.c
CUR_EX='ex18'
[[ `./a.out '42' '42'` != '0' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out '10' '12'` != '6' ]] && echo "$CUR_EX failed test 1" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex19/
cc 'aloneCan.c' main.c
CUR_EX='ex19'
[[ `./a.out 20 5 10 18 20 18 10` != '5' ]] && echo "$CUR_EX failed test 0" && exit 1
[[ `./a.out 10 3 10` != '3' ]] && echo "$CUR_EX failed test 1" && exit 1
rm -f a.out
echo "$CUR_EX Complete"

cd ../ex20/
cc 'aloneCans.c' main.c
CUR_EX='ex20'
./a.out 3 20 20 10 5 18 20 10 20 18 > ./usr_out
[[ `grep -q '[35]' ./usr_out` ]] && echo "$CUR_EX failed test 0" && exit 1
./a.out 1 2 2 3 > ./usr_out
[[ `grep -q '[13]' ./usr_out` ]] && echo "$CUR_EX failed test 1" && exit 1
./a.out 1 2 2 3 2 2 2 2 > ./usr_out
[[ `grep -q '[13]' ./usr_out` ]] && echo "$CUR_EX failed test 2" && exit 1
rm -f a.out
echo "$CUR_EX Complete"
