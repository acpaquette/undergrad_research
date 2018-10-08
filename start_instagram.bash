#!/bin/bash

keyword=("NativeVote" "NativeVoices" "GOTNV" "Honorthetreaties" "NativeLivesMatter" \
"NativesforBernie" "NotYourMascot" "MMIW" "Appropriation" "idlenomore" "nlm" \
"nativelivesmatter" "notyourmascot" "notamascot" "notacostume" "eonm" "saveoakflat" \
"protectoakflat" "dearnonnatives" "changethemascot" "changethename" "turtleisland" \
"indigenous" "NDN" "N8V" "Colonialism" "decolonize" "indigenize" "IndianCountry" \
"ihs" "indianhealthservices" "greatplains" "nativehealth" "flyingwhilebrown" \
"freeleonardpeltier" "drivingwhilebrown" "nohonor" "nohonorinracism" "nativeyouth" \
"nativevote" "apachestronghold" "TAIRP" "stopdisenrollment")

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
