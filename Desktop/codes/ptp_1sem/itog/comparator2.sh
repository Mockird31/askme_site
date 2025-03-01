#!/bin/bash

if ! [[ -f "$1" ]]; then 
    echo "Первый файл не существует"
    exit 2
fi

if ! [[ -f "$2" ]]; then 
    echo "Второй файл не существует"
    exit 2
fi

file1=$1
file2=$2

sub1=$(grep -aob -m 1 "string: " "$file1" | cut -d: -f1)
sub2=$(grep -aob -m 1 "string: " "$file2" | cut -d: -f1)

if [[ -z "$sub1" ]]; then 
    echo "Не найдена подстрока в первом файле"
    exit 3 
fi

if [[ -z "$sub2" ]]; then 
    echo "Не найдена подстрока во втором файле"
    exit 3 
fi

size1=$(wc -c "$file1" | awk '{print $1}')
size2=$(wc -c "$file2" | awk '{print $1}')

len_str_1=$((size1 - sub1))
len_str_2=$((size2 - sub2))

if [[ "$len_str_1" != "$len_str_2" ]]; then 
    echo "Строки различаются"
    exit 1
fi

temp1=$(mktemp)
temp2=$(mktemp)

dd if="$file1" bs=1 skip="$sub1" count=$len_str_1 2>/dev/null >"$temp1"
dd if="$file2" bs=1 skip="$sub2" count=$len_str_2 2>/dev/null >"$temp2"


exec 3<"$temp1"
exec 4<"$temp2"

difference=false
while IFS= read -r -n1 -u3 symb1 && IFS= read -r -n1 -u4 symb2 ; do
    if [[ "$symb1" != "$symb2" ]]; then 
        difference=true
        break
    fi  
done 

exec 3<&-
exec 4<&-

if [[ "$difference" == true ]]; then 
    echo "Строки различаются"
    exit 1
else 
    echo "Строки совпадают"
    exit 0
fi


