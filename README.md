# airstation

#Fornend 
required js hlibs

* https://plot.ly/
* http://bernii.github.io/gauge.js/
* http://justgage.com/
* and jquery 


##CRON
```
*/33 * * * * /usr/bin/python /home/ppm/15median.py                                              
*/2 * * * *  /bin/bash  /home/ppm/parser.sh     
58  6,11,19,23 * * * /usr/bin/python /home/ppm/daymean.py ```
