# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import warnings

"""
a method that takes a data set and a date as its arguments and returns a 
data structure with the average and sample standard deviation of the Fahrenheit dry-bulb 
temperature between the hours of sunrise and sunset.
"""
def avg_and_dev(data,date):
    ex_data = pd.read_csv(data)

    #Date dataframe
    ex_data['DATE'] = pd.to_datetime(ex_data.DATE)    
    date = pd.to_datetime(date)
    date = date.date()

    # new Dataframe with given dates only
    new_frame =ex_data.loc[ex_data.DATE.dt.date == date, :]
    sunrise = str(new_frame['DAILYSunrise'].iloc[1])
    sunrise_time = datetime.time(hour=int(sunrise[0:1]), minute=int(sunrise[1:3]))
    sunset = str(new_frame['DAILYSunset'].iloc[1])
    sunset_time=datetime.time(hour=int(sunset[0:2]), minute=int(sunset[2:4]))

    #Final data frame between sunrise and sunset
    mask = (new_frame['DATE'].dt.time>=sunrise_time) & (new_frame['DATE'].dt.time<=sunset_time)
    final_frame = new_frame.loc[mask]

    final_frame['HOURLYDRYBULBTEMPF'] = final_frame['HOURLYDRYBULBTEMPF'].map(lambda x: x.lstrip('+-').rstrip('s'))
    final_frame['HOURLYDRYBULBTEMPF'] = final_frame['HOURLYDRYBULBTEMPF'].fillna(0.0).astype(int)
    mean = final_frame.HOURLYDRYBULBTEMPF.mean()
    std = final_frame.HOURLYDRYBULBTEMPF.std()
    arr_answer = ["mean: ", mean,"std: ", std]
    print(arr_answer)


"""
a method that takes a data set and a date as its arguments and returns the wind chill 
rounded to the nearest integer for the times when the temperature is less than or equal to 40
degrees Fahrenheit.
Dry Bulb Temp (F) <=40

Formula USED: Wind Chill = 35.74 + 0.6215T – 35.75(Vpow(0.16)) + 0.4275T(Vpow(0.16))

"""
def wind_chill(data,date):
    ex_data = pd.read_csv(data)
    ex_data['DATE'] = pd.to_datetime(ex_data.DATE)
    
    date = pd.to_datetime(date)
    date = date.date()

    # new Data frame with given dates only
    new_frame =ex_data.loc[ex_data.DATE.dt.date == date, :]

    new_frame['HOURLYDRYBULBTEMPF'] = pd.to_numeric(new_frame['HOURLYDRYBULBTEMPF'], errors='coerce')
    new_frame = new_frame.dropna(subset=['HOURLYDRYBULBTEMPF'])
    new_frame['HOURLYDRYBULBTEMPF'] = new_frame['HOURLYDRYBULBTEMPF'].astype(str)
    new_frame['HOURLYDRYBULBTEMPF'] = new_frame['HOURLYDRYBULBTEMPF'].map(lambda x: x.lstrip('+-').rstrip('s'))
    new_frame['HOURLYDRYBULBTEMPF'] = new_frame['HOURLYDRYBULBTEMPF'].fillna(0.0).astype(float).astype(int)
    new_frame['HOURLYWindSpeed'] = new_frame['HOURLYWindSpeed'].fillna(0.0).astype(int)

    # Data Frame with temperatures <=40
    temp_frame = new_frame.loc[new_frame.HOURLYDRYBULBTEMPF<=40, :]
    temp = temp_frame['HOURLYDRYBULBTEMPF']
    wind_speed = temp_frame['HOURLYWindSpeed']
    date = temp_frame['DATE']

    i = 0
    while i<len(wind_speed)-1:
        wind_chills = ((35.74+0.6215*temp[i])-((35.75*(wind_speed[i]**0.16))+((0.4275*temp[i])*(wind_speed[i]**0.16))))
        wind_chills = round(wind_chills)
        if wind_chills > 0:
            wind_chills = "n/a"
        print("Date: "+str(date[i])+" temp: "+str(temp[i])+" Wind Speed "+str(wind_speed[i])+" Wind Chill Factor: "+str(wind_chills))
        i=i+1
"""
a method that reads both data sets and finds the day in which the 
conditions in Canadian, TX, were most similar to Atlanta's Hartsfield-Jackson Airport. 
You may use any column for your similarity metric, but be prepared to justify your choice of measurements.

"""
def similarty(data1,data2):
    ex_data = pd.read_csv(data1)
    ex_data1 = pd.read_csv(data2)
    ex_data['DATE'] = pd.to_datetime(ex_data.DATE)
    # DataFrame 1
    ex_data['HOURLYDRYBULBTEMPC'] = pd.to_numeric(ex_data['HOURLYDRYBULBTEMPC'], errors='coerce')
    ex_data = ex_data.dropna(subset=['HOURLYDRYBULBTEMPC'])
    ex_data['HOURLYDRYBULBTEMPC'] = ex_data['HOURLYDRYBULBTEMPC'].astype(str)
    ex_data['HOURLYDRYBULBTEMPC'] = ex_data['HOURLYDRYBULBTEMPC'].map(lambda x: x.lstrip('+-').rstrip('s'))
    ex_data['HOURLYDRYBULBTEMPC'] = ex_data['HOURLYDRYBULBTEMPC'].fillna(0.0).astype(float).astype(int)
    df = ex_data.loc[:,['DATE','HOURLYDRYBULBTEMPC']]
    df = df.resample('d', on='DATE').mean().dropna(how='all')

    #DataFrame 2
    ex_data1['DATE'] = pd.to_datetime(ex_data.DATE)
    ex_data1['HOURLYDRYBULBTEMPC'] = pd.to_numeric(ex_data1['HOURLYDRYBULBTEMPC'], errors='coerce')
    ex_data1 = ex_data1.dropna(subset=['HOURLYDRYBULBTEMPC'])
    ex_data1['HOURLYDRYBULBTEMPC'] = ex_data1['HOURLYDRYBULBTEMPC'].astype(str)
    ex_data1['HOURLYDRYBULBTEMPC'] = ex_data1['HOURLYDRYBULBTEMPC'].map(lambda x: x.lstrip('+-').rstrip('s'))
    ex_data1['HOURLYDRYBULBTEMPC'] = ex_data1['HOURLYDRYBULBTEMPC'].fillna(0.0).astype(float).astype(int)
    df1= ex_data1.loc[:,['DATE','HOURLYDRYBULBTEMPC']]
    df1 = df1.resample('d', on='DATE').mean().dropna(how='all')

    # finding least difference
    df['diff_A_B'] = abs(df['HOURLYDRYBULBTEMPC'] - df1['HOURLYDRYBULBTEMPC'])
    print("The day with the least difference in HOURLYDRYBULBTEMPC is: ")
    df = df.loc[df['diff_A_B'].idxmin()]
    print(df.name)

def main():
  
    warnings.filterwarnings('ignore')
    print("Testing Method 1: ")
    avg_and_dev("1089419.csv",'1/1/2017' )
    print("Testing Method 2: ")
    wind_chill("1089419.csv",'1/1/2017')
    print("Testing Method 3: ")
    similarty("1089419.csv","1089441.csv")
  
if __name__== "__main__":
    main()

