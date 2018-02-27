#!/usr/bin/python
#calculate dayly mean
import pandas as pd
from datetime import datetime


data = pd.read_csv('/srv/html/ppm/1.txt',index_col=0,sep=",",parse_dates=[0])
#data.columns = ["PPM25", "PPM10"]
#data.index.name ="DateTime"
print(data[:24:])

das=data.resample(rule='24H', closed='left', label='left', how='mean')

das.index.name="DateTime"
das.columns=["PPM25", "PPM10"]

print(das.iloc[::-1])
#das.to_csv('mean.csv',sep=",",encoding='utf-8')

#das.to_csv('/srv/html/ppm/1h.json',sep=",",encoding='utf-8')

