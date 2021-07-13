for file in script_files_refactored/*.py
do
    echo $file
    out="$(basename $file)"
    mv $file ./py-1/"test${out}"
done