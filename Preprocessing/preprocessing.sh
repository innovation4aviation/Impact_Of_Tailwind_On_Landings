rm metar_web.txt
rm metar_infos_airports.txt
while read date
do
curl https://s3.amazonaws.com/metars/metarfile$date.txt -o metar_web.txt
while read airport
do
    grep -e "^$airport" metar_web.txt >> metar_infos_airports.txt
done < airports.txt
done < dates.txt
