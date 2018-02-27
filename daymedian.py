#!/usr/bin/python3
#calculate dayly mean
import pandas as pd
from datetime import datetime


data = pd.read_csv('/root/1.txt',index_col=0,sep=",",parse_dates=[0])
#data.columns = ["PPM25", "PPM10"]
#data.index.name ="DateTime"


das=data.resample(rule='15Min',how='median')

das.index.name="DateTime"
das.columns=["PPM25", "PPM10"]
#print(das)
#das.to_csv('mean.csv',sep=",",encoding='utf-8')
das.to_csv('/var/www/html/median15.csv',sep=",",encoding='utf-8')

