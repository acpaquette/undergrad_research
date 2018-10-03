#!/bin/bash

keyword=("dosdinjiizhuh" "lymanhoffman" "akltgovbyronmallott" "jpeshlakai" \
"chiefcaleensisk" "friends_of_lynn_decoite_" "votetupola" "kaialiikahele" \
"kanielaing" "paulette_jordan" "shariceforcongress" "karenbrandendistrict2b" \
"peggyflanagan" "kirsten4house" "mkmkunesh" "bessette4mt" "votekeatonsunchild" \
"marvinwwaxjr" "deb4congressnm" "yvetteherrell" "georgenelouis" "nananow14" \
"nmchoctaw" "devyn4ok" "carlyforok" "jehforhd35" "ashley4occ" "senpittman" \
"apittman4hd99" "lindawade4ok" "tomcoleok04" "tuppertaylor" "moranforsenate" \
"repangelaromero" "jme_urbannavajo" "nativevote")

# $1 is the bash profile to source for crontab
source $1

# $2 is the anaconda environment to activate for crontab
source activate $2

DATE=`date '+%Y_%m_%d_%H_%M'`

echo $DATE
cd data/
mkdir $DATE

# background and run instagram_search with each keyword
for i in "${keyword[@]}"; do
  python3 /Users/daniel/Desktop/undergrad_research/instagram_search.py "$i" /Users/daniel/Desktop/undergrad_research/data/$DATE &
done

# ./start_instagram.bash /Users/daniel/.bash_profile undergrad /Users/daniel/Desktop/undergrad_research/data

# Indigenous Keywords:
# "Midterm" "Vote" "Politics" "District" "Senator" "Congress" "elect" "Representative" "Sen" "Rep" "Republican" "Democrat" "Dem" "Rep" "Gov" "Debates" "Poli" "GOP" "Ballot" "Register" "Incumbent" "Delegate" "Potus" "Scotus" "Supreme court" "GA" "KS" "TX" "NE" "KY" "MO" "MS" "CA" "TN" "FL" "SD" "OK" "Georgia" "Kansas" "Texas" "Nebraska" "Kentucky" "Missouri" "Mississippi" "California" "Tennessee" "Florida" "South Dakota" "Oklahoma"

# Nativevote Keywords:
# "dosdinjiizhuh" "lymanhoffman" "akltgovbyronmallott" "jpeshlakai" "chiefcaleensisk" "friends_of_lynn_decoite_" "votetupola" "kaialiikahele" "kanielaing" "paulette_jordan" "shariceforcongress" "karenbrandendistrict2b" "peggyflanagan" "kirsten4house" "mkmkunesh" "bessette4mt" "votekeatonsunchild" "marvinwwaxjr" "deb4congressnm" "yvetteherrell" "georgenelouis" "nananow14" "nmchoctaw" "devyn4ok" "carlyforok" "jehforhd35" "ashley4occ" "senpittman" "apittman4hd99" "lindawade4ok" "tomcoleok04" "tuppertaylor" "moranforsenate" "repangelaromero" "jme_urbannavajo" "nativevote"
