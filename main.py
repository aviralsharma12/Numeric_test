import streamlit as st
import pandas as pd
import numpy as np
import math

#___zip files___
df = pd.read_csv("combined.csv")

#___trip info___
df1= pd.read_csv("Trip-Info.csv")

#___end datetime
import datetime
end_date = datetime.datetime(2018, 2, 28, 23, 00, 00).timestamp()

#___start datetime
start_date = datetime.datetime(2017, 11, 17, 11, 28, 28).timestamp()

#___calculate the distance___
df['distance'] = 6367 * 2 * np.arcsin(np.sqrt(np.sin((np.radians(df['lat']) - math.radians(25.613802))/2)**2 + math.cos(math.radians(25.613802))
* np.cos(np.radians(df['lat'])) * np.sin((np.radians(df['lon']) - math.radians(85.053558))/2)**2))
#print(df)

#--change datetime formate
df["date_time"] = pd.to_datetime(df['tis'], unit='s')
df['Hour'] = df['date_time'].dt.hour

#calculate Avg speed
df["avg_speed"] = df.distance/ df.Hour

#---convert Trip csv datetime to epoch---
azx = pd.to_datetime(df1['date_time'],  format='%Y%m%d%H%M%S', errors='coerce')
ass = df1['date_time'].astype(str)
epoch_time = pd.to_datetime(ass).values.astype(np.int64) // 10 ** 9
df1["tis"]= epoch_time
df1['date_times'] = azx
df1.drop(columns=["date_time"],inplace = True)
df1.rename(columns={"date_times":"date_time"},inplace=True)

#---create final df from combine csv and trip csv--
final_df = pd.merge(df,df1 ,on= "tis",how='left')
final_df['Epoch_Datetime'] = final_df['tis'].astype(str) + "_" + final_df['date_time_x'].astype(str)


#--sort the datetime for user input--
Start_date = final_df.sort_values(by=['Epoch_Datetime'], ascending=True)
End_date = final_df.sort_values(by=['Epoch_Datetime'], ascending=False)

#---replace boliena to number type in osf--
final_df['osf'].replace({False: 0, True: 1}, inplace=True)

started_time = Start_date.Epoch_Datetime.unique()
End_time = End_date.Epoch_Datetime.unique()


#---creating Api--
st.title("Report")
Select_Starting_date = st.selectbox('Select Start Date ?',started_time)
Select_End_date = st.selectbox('Select End Date?',End_time)


#--- create report on basi on input time epoch--
def report():
    filtered_df = final_df.loc[(final_df['Epoch_Datetime'] >= Select_Starting_date)
                               & (final_df['Epoch_Datetime'] <= Select_End_date )]
    return filtered_df[["lic_plate_no", "distance", "avg_speed", "transporter_name", "osf",]]

if st.button('Get Report'):
     st.write(report())
