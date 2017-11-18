import pandas as pd
import dateutil 
import datetime as dt

#open the file
d= pd.read_csv('bg.csv')
#convert data to dataframe
df = pd.DataFrame(data=d)

##apply consistent formatting to the date
df['date'] = df['date'].apply(dateutil.parser.parse, dayfirst=True)

today = dt.date.today().strftime("%Y-%m-%d")

#dates
dates = df['date'].to_string(index=False)
BGmean = 1.0

messageHighBG = "BG is high! Take you medicine!"

#get today's mean of the BG. Use to_string(index=False) to remove the index
todayMean = df.loc[df['date'] == today].mean().to_string(index=False)

#If today's mean is greater than the desired BG mean, then you get a warning message.
if (todayMean != BGmean):
    print(messageHighBG)


#print("max = ", df['bg'].max())
#print("min = ", df['bg'].min())
#print("readings per date =\n", df['date'].value_counts())
#print("average bg per date ", df.groupby('date').mean())