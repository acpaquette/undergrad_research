#!/bin/bash

my_list=("trump" "banana" "arizona" "sunset" "unicorn")

# $1 is the bash profile to source
source $1

# $2 is the anaconda environment to activate
source activate $2
#
for i in "${my_list[@]}"; do
  python ./instagram_search.py "$i" &
done

# OUTPUT="$(pgrep -f "python ./tweepyStream.py $i")"
# if [[ $OUTPUT ]];
# then
#   echo $i Running
# else
#   DATE=`date '+%Y-%m-%d %H:%M:%S'`
#   echo $i stream offline @ $DATE
#
#   echo "$(which python)"

# python ./instagram_search.py &

echo Done


#argsparse
