#!/bin/sh
rsync -z -e "ssh -p22" /root/data/* ppm@XX.XXX.XXX.XXX:/srv/html/ppm/
exit 0
