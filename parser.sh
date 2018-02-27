#!/bin/bash
datadir='/srv/html/ppm'
	 echo "Date,PPM_2.5,PPM_10,mean25,mean10"> $datadir/data.csv  ; tail -n $((20*24)) $datadir/1.txt >> $datadir/data.csv
# echo "Date,PPM_2.5,PPM_10"> /var/www/html/data.csv  ; cat  /home/chip/data.txt  | sed  -E -e 's/\t\||\||ppm2.5:|ppm10:|\t\n//g' | sed 's/\t/,/g' | sed -E -e 's/[[:space:]],[[:space:]]|,[[:space:]]/,/g' >> /var/www/html/data.csv

