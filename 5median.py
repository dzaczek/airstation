#!/usr/bin/python
#calculate dayly mean
import pandas as pd
from datetime import datetime


data = pd.read_csv('/srv/html/ppm/1.txt',index_col=0,sep=",",parse_dates=[0])
#data.columns = ["PPM25", "PPM10"]
#data.index.name ="DateTime"


das=data.resample(rule='5Min',how='median')
mea=das.resample('D',how='mean')

das.index.name="DateTime"
mea.index.name="DateTime"
das.columns=["PPM25", "PPM10"]
mea.columns=["PPM25", "PPM10"]
#print(das)
#das.to_csv('mean.csv',sep=",",encoding='utf-8')
das.to_csv('/srv/html/ppm/median5.csv',sep=",",encoding='utf-8')
mea.to_csv('/srv/html/ppm/meandmedian.csv',sep=",",encoding='utf-8')

