#! /bin/bash
# author 11710403
# date   2020/2/28

dir_cnt=0
file_cnt=0
save_path='output.file'
output_str=''

list_all(){

    # /xxx/yyyy/zzzz/ -> zzzz
    current_file_name=$(echo $1 | sed 's/\/$//' | sed 's/^\///' | sed 's/[^\/]*\///g') # 1. if the first character is /, delete it. 2. If the last character is /, delete it. 3. delte all the pattern xxx/

    # Enter the directory
    OIFS=$IFS;IFS=$'\0' # the null byte '\0' is the only character which cannot be apply in file name
    cd `pwd`/$current_file_name
    IFS=$OIFS

    # Counters increment
    this_file_cnt=$(ls -lA | grep "^-" | sed -E 's/([^ ]+ *){8}//' | awk 'END{ print NR }') #([^ ]+ *){8}: delete the first 8 segment in the output of ls -lA
    this_dir_cnt=$(ls -lA | grep "^d" | sed -E 's/([^ ]+ *){8}//' | awk 'END{ print NR }')
    file_cnt=$(expr $file_cnt + $this_file_cnt)
    dir_cnt=$(expr $dir_cnt + $this_dir_cnt)

    # Output name
    echo "[$current_file_name]" 

    # Output the information of this directory
    OIFS=$IFS;IFS=$'\0'
    ls -lA | grep '[-d]' | sed -E 's/([^ ]+ *){8}//' | awk -v str=`pwd`/$current_file_name/ ' { print str $0 } '
    IFS=$OIFS

    # Output new line
    echo ''
    
    # Explode subdirectories in this directory
    for index in `seq 1 ${this_dir_cnt}`
    do
        filename=$(ls -lA | grep "^d" | sed -E 's/([^ ]+ *){8}//' | awk 'NR=="'$index'"{ print $0 }')
        list_all "$filename"
    done

    # return
    cd ..
}

OIFS=$IFS;IFS=$'\0'
save_path=$(readlink -f $2)
IFS=$OIFS

list_all $1

echo "[Directories Count]:$dir_cnt"
echo "[Files Count]:$file_cnt" 
