#!/bin/bash

set -e

trap 'curl https://api.telegram.org/bot6263600311:AAHd2YPx8E4faYtlL4-pNv1WJfjf0y97e-8/sendMessage\?chat_id\=-986487257\&text\=ocean-Error' ERR

rm -rf tmp
mkdir tmp
cd tmp

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    curl https://api.telegram.org/bot6263600311:AAHd2YPx8E4faYtlL4-pNv1WJfjf0y97e-8/sendMessage\?chat_id\=-986487257\&text\=ocean-Error
    exit 1
fi

vid=$1
to=$2

echo $vid
echo $to

yt-dlp --fragment-retries "infinite" --socket-timeout 15 --no-playlist --external-downloader aria2c --external-downloader-args '-c -j 3 -x 3 -s 3 -k 1M' $vid -o "$to.%(ext)s"

toe=$(ls | grep $to)
echo "$toe"


ffmpeg -i $toe -af "afftdn=nr=20:nf=-20:tn=1" ffmpeg-$toe

rm $toe

#auto-editor ffmpeg-$toe --edit audio:threshold=2% --silent-speed 2 -o editor-$toe

#rm ffmpeg-$toe

mv ffmpeg-$toe ../$toe
cd ..
#rm -rf tmp

curl https://api.telegram.org/bot6263600311:AAHd2YPx8E4faYtlL4-pNv1WJfjf0y97e-8/sendMessage\?chat_id\=-986487257\&text\=ocean-Finished-$toe
