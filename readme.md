# COE332 FINAL PROJECT
### By Tedham Anderson, Corey Finnigan and Juan Martinez

1. **Purpose of this Project:** This project looks at the average residential monthly energy bills, focusing on cost based on kWh consumption. We chose to look at this data based on its availability from the City of Austin, and its longevity, given the fact that the data has been collected for almost 20 years.

2. **Uses of this Project:** By using the app, consumers can query a range of dates and see the average bill cost, the average fuel charge, the average kWh consumption within the City of Austin, and get a graphical representation of the data. This information can be extremely useful *especially* when considering the increasing trend of households determining to shift to a purely solar-powered residential model.

3. **Consumer Charges to use this Project:** Ideally, I would want to see this project implemented by the city from which the data is received. I would like this program to have been made by city employees, as the local government has the assets to support it; that would make this a project for a salaried engineer, and not a service that consumers need to pay to use in order to receive *very* public data. In this regard, everyone wins and then the local government will have developed something that could actually be useful to its citizens. That is the best possible result to me. If not, the program could be sold to any wanting city to disperse at their discretion. 

### **Additional Notes:**

**a.** This code was tested originally on local desktop machines and then modified to operate on the TACC machine. All code was tested to be fully operational prior to shifting to the TACC machine.

**b.** All graph-generating routes will not generate actual graphical representations of the data when SSH'd to the TACC machine, and therefore example graphs have been attached in the "Graphs" folder. The graph examples where successfully generated through Postman.

**c.** The curl function for adding additional data should read as follows:
`curl -X POST localhost:<port>/add_data/<yyyy>/<mm>/<ddd>/<kWh>/<fuel_charge>/<bill>`

### **Code Execution Examples:**

**I.** To query a specific date range, use the Julian Date conversion generated from the get_data function and enter: `curl localhost:5050/query_dates/2458362.5/2458543.5`

*Output:*

| Entry |    Date   |  Average kWh  | Fuel Charge (Cents/kWh)| Average Bill |  Julian Dates |
| ----- | ---------:|:-------------:|:----------------------:|:------------:| -------------:|
|  225  | 2018-10-01|           819 |                  2.936 |       82.41  |    2458392.5  |
|  226  | 2018-11-01|           685 |                  2.895 |       68.01  |    2458423.5  |
|  227  | 2018-12-01|           663 |                  2.895 |       65.67  |    2458453.5  |
|  228  | 2019-01-01|           761 |                  2.895 |       76.13  |    2458484.5  |
|  229  | 2019-02-01|           707 |                  2.895 |       70.38  |    2458515.5  |
|  230  | 2019-03-01|           658 |                  2.895 |       65.13  |    2458543.5  |

**II.** To find the mean bill for a specific date range, enter: `curl localhost:5050/mean_bill/2458362.5/2458543.5` Note: this format applies to **all mean routes**.

*Output:* `71.28833333333333`

**III.** To reset the data and undo any modifications you may have done to the initial data reset, enter: `curl -X POST localhost:5050/reset_data_route`

*Output:* `Data Reset`

**IV.** If you want to obtain the data from your source .xlsx without having to launch flask, enter: `python data_collector.py`

*Output:* This will output **all** of the data collected from the source .xls database.