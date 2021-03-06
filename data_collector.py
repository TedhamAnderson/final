import pandas as pd
import math

def obtain_data():
    df = pd.read_excel(r'C:\UT\Spring 2020\software Class\Final\Residential_Average_Monthly_kWh_and_Bills.xlsx', delimiter='\t')
    Dates = df.Date
    JD = []
    for ii in range(len(Dates)):
        temp_date = Dates[ii]
        year = temp_date.year
        month = temp_date.month
        day = temp_date.day
        hour = 0
        minute = 0
        second = 0
        julian_date = 367 * year - math.floor((7 * (year + math.floor((month + 9) / 12))) / 4) + math.floor(
        275 * month / 9) + day + 1721013.5 + (1 / 24) * (hour + (1 / 60) * (minute + second / 60))
        JD.append(julian_date)

    df['Julian Dates'] = JD
    return df
obtain_data()