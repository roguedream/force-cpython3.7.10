
for file in sample-1/*.py
do
    echo $file 
    out="$(basename $file)"
    C:\\Users\\User\\Desktop\\cpython-3.7\\PCbuild\\amd64\\python $file
    mv C:\\Users\\User\\Desktop\\output\\mylog-3.7.txt .\\outlog\\"log-${out}.txt"
done
