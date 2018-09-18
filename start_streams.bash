#!/bin/bash

CONFIG_ARRAY=("stream_config_1.ini" "stream_config_2.ini")

# $1 is the bash profile to source
source $1

# $2 is the anaconda environment to activate
source activate $2

for i in $CONFIG_ARRAY; do
  OUTPUT="$(pgrep python ./tweepyStream.py $i)"
  if [[ $OUTPUT ]];
  then
    echo $i Running
  else
    DATE=`date '+%Y-%m-%d %H:%M:%S'`
    echo $i stream offline @ $DATE

    echo "$(which python)"
    python ./tweepyStream.py $i &
  fi
done

echo Done
