
rm ./$1
rm ./$1.o
echo compiling...
nasm -fmacho64 ./$1.nasm
echo assembling...
gcc ./$1.o -o $1 -v
echo done!
./$1
