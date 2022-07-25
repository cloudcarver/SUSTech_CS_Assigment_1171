#! /bin/bash
# author github@mikechesterwang
# this srcipt should be run in su mode

# global variables
OIFS=$IFS
save_path='default.txt'
declare -a A # unexploded directory queue
d_cnt=0 # total directories count
f_cnt=0 # total files count
dfcnt=0 # delta files count
ddcnt=0 # delta directories count

safe_mode_begin(){
    IFS=$'\0'
}
safe_mode_end(){
    IFS=$OIFS
}

list_info(){
    # print information
    safe_mode_begin
        cd $1 # the absolute path of the dir waited to explode
        echo [$(echo $1 | sed -e 's/^\///' | sed -e 's/\///' | sed -e 's/[^\/]*\///g')] >> $save_path
        ls -lA | grep '[-d]' | sed -E 's/([^ ]+ *){8}//' | awk -v str=`pwd`/ ' { print str $0 } ' >> $save_path
        echo '' >> $save_path
    safe_mode_end

    # counters increment
    dfcnt=$(ls -lA | grep '^-' | awk 'END{ print NR }')
    ddcnt=$(ls -lA | grep '^d' | awk 'END{ print NR }')
    f_cnt=$(expr $dfcnt + $f_cnt)
    d_cnt=$(expr $ddcnt + $d_cnt)

    # add the dicretories in this folder to unexploded queue (A)
    for index in `seq 1 ${ddcnt}` ; do      
        filename=$(ls -lA | grep "^d" | sed -E 's/([^ ]+ *){8}//' | awk 'NR=="'$index'" { print $0 }')
        safe_mode_begin
            A[$rear]=`pwd`/$filename; rear=$(expr $rear + 1) # enQueue
        safe_mode_end
    done
}

# variables for queue
front=0
rear=0

safe_mode_begin
    # use absolute path for save_path
    save_path=$(readlink -f $2)
    # input the first unexploded directories in queue A
    A[$rear]=$(readlink -f $1); rear=$(expr $rear + 1) # enQueue
    > $save_path
safe_mode_end

p='' # current directories

# BFS
while [ $front -ne $rear ] ; do
    safe_mode_begin
        p=${A[$front]}; front=$(expr $front + 1) # deQueue
        list_info $p
    safe_mode_end
done

safe_mode_begin
    echo "[Directories Count]:$d_cnt" >> $save_path
    echo "[Files Count]:$f_cnt" >> $save_path
safe_mode_end

# debug
safe_mode_begin
    cat $save_path
safe_mode_end