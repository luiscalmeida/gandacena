#!/bin/bash

if [[ $# != 1 ]] || [ $1 == "-h" ]; 
then
	echo "Usage: ./csf_script.sh [dd image]"; 
	exit 1; 
fi
umount mnt 2>/dev/null
rm -r mnt 2>/dev/null
mkdir ./mnt
mmls_result=`mmls $1 2>/dev/null`
ntfs_result=`echo "$mmls_result" | grep NTFS`
if [ -z "$ntfs_result" ]; 
	then echo "There's no NTFS file system in $1."; 
	exit 1; 
fi
biggest_ntfs=`echo "$ntfs_result" | cut -d" " -f12`
echo "NTFS LENGTHS"
echo "$biggest_ntfs"
echo " "
max=0
index=0
index_stop=0
for line in `echo "$biggest_ntfs"`;
do	
	((index++))
	echo "FOR LINE ON NTFS LENGTHS"
	echo $line;
	value=$((10#$line))
	if [[ $max < $value ]]; then 
		max=$value;
		index_stop=$index;
	fi
done
echo " "
echo "MAX SIZE NTFS LENGTH: $max"
echo " "
echo "MAX SIZE NTFS LENGTH INDEX : $index_stop"
echo " "
index=0
echo "GREP NTFS RESULT"
echo "$ntfs_result"
echo " "
offset=`echo "$ntfs_result" | cut -d" " -f6`
echo "MAX SIZE NTFS OFFSET:" 
echo "$offset"
echo " "
for linee in `echo "$offset"`;
do
	echo "FOR LINE IN MAX SIZE NTFS OFFSET"
	echo "$linee"
	((index++))
	if [[ $index == $index_stop ]]; then
		offset=`echo "$linee"`	
	fi
done
echo " "
echo "MAX SIZE NTFS CONFIRMATION OFFSET"
echo "$offset"

clean_offset=$((10#$offset))
echo "MAX SIZE NTFS CONFIRMATION CLEAN OFFSET"
echo "$clean_offset"
echo " "
offset_bytes=$(($clean_offset * 512))
echo "OFFSET * BYTES(512) = $offset_bytes"
echo " "
echo "MOUNTING NTFS.."
`mount -t ntfs -o ro,loop,offset=$offset_bytes $1 ./mnt/`
cd mnt/Windows/System32/config/
echo " "
echo "Now in path: "
echo `pwd`

