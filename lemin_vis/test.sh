#!/usr/bin/env bash
ONE='flone'
TEN='flten'
THOUSAND='flth'
BIG='big'
SOUP='soup'
TMP='/tmp/lem_tmp'
TIME='/usr/bin/time -lp'

if [ -x './lem-in' ]; then
	BIN='./lem-in'
elif [ -x './lem_in' ]; then
	BIN='./lem_in'
elif [ -x './../lem-in' ]; then
	BIN='./../lem-in'
elif [ -x './../d_lem-in' ]; then
	BIN='./../d_lem-in'
else
	BIN='./lem-in'
fi

if [ $1 -a $1 = 'one' ]; then
	./generator --flow-one > $ONE
	$TIME $BIN < $ONE > $TMP
	echo '--------------------------------------------------------------------'
	head -n2 $ONE
	grep -c '^L' $TMP
elif [ $1 -a $1 = 'ten' ]; then
	./generator --flow-ten > $TEN
	$TIME $BIN < $TEN > $TMP
	echo '--------------------------------------------------------------------'
	head -n2 $TEN
	grep -c '^L' $TMP
elif [ $1 -a $1 = 'thousand' ]; then
	./generator --flow-thousand > $THOUSAND
	$TIME $BIN < $THOUSAND > $TMP
	echo '--------------------------------------------------------------------'
	head -n2 $THOUSAND
	grep -c '^L' $TMP
elif [ $1 -a $1 = 'big' ]; then
	./generator --big > $BIG
	$TIME $BIN < $BIG > $TMP
	echo '--------------------------------------------------------------------'
	head -n2 $BIG
	grep -c '^L' $TMP
elif [ $1 -a $1 = 'soup' ]; then
	./generator --big-superposition > $SOUP
	$TIME $BIN < $SOUP > $TMP
	echo '--------------------------------------------------------------------'
	head -n2 $SOUP
	grep -c '^L' $TMP
elif [ $1 -a $1 = 'clean' ]; then
	rm -f $ONE $TEN $THOUSAND $BIG $SOUP $TMP
else
	echo "error: invalid argument"
	echo "usage: test.sh [ one | ten | thousand | big | soup | clean]"
	exit 1
fi
