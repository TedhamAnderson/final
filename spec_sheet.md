# Spec Sheet

## /data', methods=['GET']
Simply create a url with /data and the app will return the current list of data to you.

## /query_dates/<JD1>/<JD2>', methods=['GET']
This url will return you data that is within the boundaries of JD1 to JD2. Note JD1 < JD2. Also JD1 and JD2 are in a julian date format. This allows for less complicated imputs by the user. Traditionally the user would need to insert a year, month, day, hour, minute, second. Now the user imputs a single float value.

## /mean_bill/<JD1>/<JD2>',methods=['GET']
returns the mean bill value in the range from JD1 to JD2. Once again JD1 > JD2. JD1 and JD2 are in julian dates.

## /mean_fuel_charge/<JD1>/<JD2>',methods=['GET']
returns the mean fuel charge value in the range from JD1 to JD2. Once again JD1 > JD2. JD1 and JD2 are in julian dates.

## /mean_kWh/<JD1>/<JD2>',methods=['GET']
returns the mean kwh value in the range from JD1 to JD2. Once again JD1 > JD2. JD1 and JD2 are in julian dates.

## /graph/kwh/<JD1>/<JD2>',methods=['GET']
returns a graph of the kwh data in the range from JD1 to JD2. Once again JD1 > JD2. JD1 and JD2 are in julian dates. The graphs work when produced in a web browser or post man. When using the tack machine the graphs do not come out in a correct format.

## /graph/fuel_charge/<JD1>/<JD2>',methods=['GET']
returns a graph of the fuel_charge data in the range from JD1 to JD2. Once again JD1 > JD2. JD1 and JD2 are in julian dates. 

## /graph/bill/<JD1>/<JD2>',methods=['GET']
returns a graph of the bill data in the range from JD1 to JD2. Once again JD1 > JD2. JD1 and JD2 are in julian dates. 

## /add_data/<year>/<month>/<day>/<kwh>/<fuel_charge>/<bill>',methods=['POST']
this route will add new data to the current data. You choose the imputs and they must be in the order described in the url. after ther route is done, it will return your new data set.

## /reset_data_route',methods=['POST']
this route will reset your data to what it was origingally, before any new data was added.