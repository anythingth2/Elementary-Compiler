flex ./hello.l
bison -dy ./hello.y
gcc ./lex.yy.c ./y.tab.c ./main.c -o ./hello.exe
./hello.exe < ./test.txt
pause
