#!/bin/bash

keyword=("dosdinjiizhuh" "lymanhoffman" "akltgovbyronmallott" "jpeshlakai" \
"chiefcaleensisk" "friends_of_lynn_decoite_" "votetupola" "kaialiikahele" \
"kanielaing" "paulette_jordan" "shariceforcongress" "karenbrandendistrict2b" \
"peggyflanagan" "kirsten4house" "mkmkunesh" "bessette4mt" "votekeatonsunchild" \
"marvinwwaxjr" "deb4congressnm" "yvetteherrell" "georgenelouis" "nananow14" \
"nmchoctaw" "devyn4ok" "carlyforok" "jehforhd35" "ashley4occ" "senpittman" \
"apittman4hd99" "lindawade4ok" "tomcoleok04" "tuppertaylor" "moranforsenate" \
"repangelaromero" "jme_urbannavajo" "nativevote" "sherepresents")

# $1 is the bash profile to source for crontab
source $1

# $2 is the anaconda environment to activate for crontab
source activate $2

DATE=`date '+%Y_%m_%d_%H_%M'`

cd data/
mkdir $DATE

# background and run instagram_search with each keyword
for i in "${keyword[@]}"; do
  python3 /Users/daniel/Desktop/undergrad_research/instagram_search.py "$i" /Users/daniel/Desktop/undergrad_research/data/$DATE &
done
