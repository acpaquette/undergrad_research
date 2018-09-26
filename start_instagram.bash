#!/bin/bash

keyword=("trump" "banana" "arizona" "sunset" "unicorn")

# $1 is the bash profile to source for crontab
source $1

# $2 is the anaconda environment to activate for crontab
source activate $2

echo $3

# background and run instagram_search with each keyword
for i in "${keyword[@]}"; do
  python3 instagram_search.py "$i" $3 &
done

echo Done
