#retrieve bloodGlucose Info

import pandas as pd
import dateutil as date
import numpy as np

import datetime as dt 
import statistics as stats

import blood_glucose_crud as bgc
import importlib.util
import sys

#returns a list of classes of the type Blood Glucose
listOfBloodGlucoseClasses = bgc.blood_glucose_select_by_days(90)



#get the attributes of the class

BGcolumns = listOfBloodGlucoseClasses.pop().__dict__.keys()



#create a dataframe with only columns

df = pd.DataFrame(data=None,index=None,columns=BGcolumns)



index = 0

#add row by row to the dataframe

for BG_Class in listOfBloodGlucoseClasses:

df.loc[index] = [BG_Class.blood_glucose_id,BG_Class.meal,BG_Class.reading,BG_Class.record_date,BG_Class.notes]

index = index + 1



# start_date = '2017-10-27 00:00:00'

# end_date = '2017-10-28 00:00:00'



#mask = (df['record_date'] >= start_date) & (df['record_date'] <= end_date)



#df = df.loc[mask]



MaxBloodGlucoseReading = df.loc[df['reading'].argmax(),'reading']

#MaxBloodGlucoseDate = df.loc[df['reading'].argmax(),'record_date']



MinBloodGlucoseReading = df.loc[df['reading'].argmin(),'reading']

#MinBloodGlucoseDate = df.loc[df['reading'].argmin(),'record_date']



All_Average = df['reading'].mean()



# start_date = '2017-10-27 00:00:00'

# end_date = '2017-10-28 00:00:00'



#mask = (df['record_date'] >= start_date) & (df['record_date'] <= end_date)





print('Highest Blood Glucose Reading: ', MaxBloodGlucoseReading)

print('Lowest Blood Glucose Reading: ' , MinBloodGlucoseReading)

print('All-Time Average: ', All_Average)



#print('Last 30 Days Average: ', Last30Days_Average)





#print(today)

#todayMean = df.loc[df['record_date'] == today].mean().to_string(index=False)

#print(todayMean)

##apply consistent formatting to the date

#df['RecordDate'] = df['RecordDate'].apply(dateutil.parser.parse, dayfirst=True)

#print(todayMean)