#!/bin/bash

RED="\033[31m\033[1m"
GREEN="\033[32m\033[1m"
END="\033[0m"
SEP="---------------------"
echo -e Тестирование

echo $SEP
echo "Первый тест:"
com="./comparator2.sh ./tests/test1.txt ./tests/test2.txt"
$com 
res="$?"
echo "Вводятся одинаковые строки"
if [[ $res -eq 0 ]]; then 
    echo -e "$GREEN""Тест пройден""$END"
else 
    echo -e "$RED""Тест не пройден""$END"
fi
echo $SEP

echo $SEP
echo "Второй тест:"
com="./comparator2.sh ./tests/test1.txt ./tests/test3.txt"
$com 
res="$?"
echo "Вводятся разные строки"
if [[ $res -eq 1 ]]; then 
    echo -e "$GREEN""Тест пройден""$END"
else 
    echo -e "$RED""Тест не пройден""$END"
fi
echo $SEP

echo $SEP
echo "Третий тест:"
echo "Подстрока не найдена"
com="./comparator2.sh ./tests/test4.txt ./tests/test2.txt"
echo "Вывод программы:"
$com 
res="$?"

if [[ $res -eq 3 ]]; then 
    echo -e "$GREEN""Тест пройден""$END"
else 
    echo -e "$RED""Тест не пройден""$END"
fi
echo $SEP

echo $SEP
echo "Четвертый тест:"
echo "Файл не найден"
com="./comparator2.sh ./tests/no.txt ./tests/test2.txt"
echo "Вывод программы:"
$com 
res="$?"
if [[ $res -eq 2 ]]; then 
    echo -e "$GREEN""Тест пройден""$END"
else 
    echo -e "$RED""Тест не пройден""$END"
fi
echo $SEP

echo $SEP
echo "Пятый тест:"
com="./comparator2.sh ./tests/test1.txt ./tests/test5.txt"
$com 
res="$?"
echo "Различия в пробельных символах"
if [[ $res -eq 1 ]]; then 
    echo -e "$GREEN""Тест пройден""$END"
else 
    echo -e "$RED""Тест не пройден""$END"
fi
echo $SEP
