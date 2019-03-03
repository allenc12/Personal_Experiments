#!/usr/bin/env bash
ARCHIVE='./generator.gz'
ONE='flone'
TEN='flten'
THOUSAND='flthousand'
BIG='big'
SOUP='soup'
TMP='/tmp/lem_tmp'
TIME='/usr/bin/time'

if [ -x './generator' ]; then
	GEN=./generator
else
	GEN=./generator
	CHECKSUM="/tmp/sha512sum.txt"
	grep -E '[a-f0-9]+  generator\.gz' $0 | sed 's/#//g' > $CHECKSUM
	tail -n1 $0 | sed 's/#//g' | base64 -D > $ARCHIVE
	shasum -s -a512 -c $CHECKSUM && gunzip -f $ARCHIVE && chmod +x $GEN && $GEN
	rm -f $CHECKSUM
fi

if [ -x './lem-in' ]; then
	BIN='./lem-in'
elif [ -x './lem_in' ]; then
	BIN='./lem_in'
elif [ -x './../lem-in' ]; then
	BIN='./../lem-in'
elif [ -x './../d_lem-in' ]; then
	BIN='./../d_lem-in'
else
	echo "$0: error: could not find lem-in binary"
	exit 1
fi

if [ $1 -a $1 = 'one' ]; then
	$GEN --flow-one > $ONE
	$TIME $BIN < $ONE > $TMP
	echo '--------------------------------------------------------------------'
	NODES=$(grep -Ec '^\w+ ' $ONE)
	EDGES=$(grep -Ec '^\w+-' $ONE)
	echo "Total Nodes: $NODES"
	echo "Total Edges: $EDGES"
	echo '--------------------------------------------------------------------'
	printf "Total Ants: $(head -n2 $ONE | sed 's/: /:\\t/g')\n"
	printf "Number of lines from your lem-in:\t$(grep -c '^L' $TMP)\n"
elif [ $1 -a $1 = 'ten' ]; then
	$GEN --flow-ten > $TEN
	$TIME $BIN < $TEN > $TMP
	echo '--------------------------------------------------------------------'
	NODES=$(grep -Ec '^\w+ ' $TEN)
	EDGES=$(grep -Ec '^\w+-' $TEN)
	echo "Total Nodes: $NODES"
	echo "Total Edges: $EDGES"
	echo '--------------------------------------------------------------------'
	printf "Total Ants: $(head -n2 $TEN | sed 's/: /:\\t/g')\n"
	printf "Number of lines from your lem-in:\t$(grep -c '^L' $TMP)\n"
elif [ $1 -a $1 = 'thousand' ]; then
	$GEN --flow-thousand > $THOUSAND
	$TIME $BIN < $THOUSAND > $TMP
	echo '--------------------------------------------------------------------'
	NODES=$(grep -Ec '^\w+ ' $THOUSAND)
	EDGES=$(grep -Ec '^\w+-' $THOUSAND)
	echo "Total Nodes: $NODES"
	echo "Total Edges: $EDGES"
	echo '--------------------------------------------------------------------'
	printf "Total Ants: $(head -n2 $THOUSAND | sed 's/: /:\\t/g')\n"
	printf "Number of lines from your lem-in:\t$(grep -c '^L' $TMP)\n"
elif [ $1 -a $1 = 'big' ]; then
	$GEN --big > $BIG
	$TIME $BIN < $BIG > $TMP
	echo '--------------------------------------------------------------------'
	NODES=$(grep -Ec '^\w+ ' $BIG)
	EDGES=$(grep -Ec '^\w+-' $BIG)
	echo "Total Nodes: $NODES"
	echo "Total Edges: $EDGES"
	echo '--------------------------------------------------------------------'
	printf "Total Ants: $(head -n2 $BIG | sed 's/: /:\\t/g')\n"
	printf "Number of lines from your lem-in:\t$(grep -c '^L' $TMP)\n"
elif [ $1 -a $1 = 'soup' ]; then
	$GEN --big-superposition > $SOUP
	$TIME $BIN < $SOUP > $TMP
	echo '--------------------------------------------------------------------'
	NODES=$(grep -Ec '^\w+ ' $SOUP)
	EDGES=$(grep -Ec '^\w+-' $SOUP)
	echo "Total Nodes: $NODES"
	echo "Total Edges: $EDGES"
	echo '--------------------------------------------------------------------'
	printf "$(head -n2 $SOUP | sed 's/: /:\\t/g')\n"
	printf "Number of lines from your lem-in:\t$(grep -c '^L' $TMP)\n"
elif [ $1 -a $1 = 'clean' ]; then
	rm -f $ONE $TEN $THOUSAND $BIG $SOUP $TMP
else
	echo "$0: error: invalid argument"
	echo "$0: usage: test.sh [ one | ten | thousand | big | soup | clean]"
	exit 1
fi
#0a348974f31742ca7aff3a93716bf7eb1ff157bda1944213791cf0843fbf7090befdb3e2e81850959da02f9fee951fafa562ddf06aca314b79cdb0e5678a7b0a  generator.gz
#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
