from flask import Flask, request, jsonify
import json
import os
import statistics
import datetime
import math
import data_collector
import pandas as pd
import pygal
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World'

def get_data():
    file_exists = os.path.exists(Current_data.csv)
    if file_exists == 0:
        data = data_collector.obtain_data()
    else:
        data = pd.read_csv(r'C:\UT\Spring 2020\software Class\Final\Current_data.csv')
    return data

def get_counters(JD1, JD2):
    JD1 = float(JD1)
    JD2 = float(JD2)
    data = get_data()
    JD = data['Julian Dates']
    counter_1 = 0
    counter_2 = 0
    for objects in JD:
        counter_1 = counter_1 + 1
        if objects >= JD1:
            for objects2 in JD:
                counter_2 = counter_2 + 1
                if objects2 >= JD2:
                    return [counter_1, counter_2, data]

@app.route('/data', methods=['GET'])
def list_data():
    data = get_data()
    return data.to_string()

@app.route('/query_dates/<JD1>/<JD2>', methods=['GET'])
def query_dates(JD1,JD2):
    [counter_1, counter_2, data] = get_counters(JD1, JD2)
    return data.iloc[counter_1:counter_2].to_string()

@app.route('/mean_bill/<JD1>/<JD2>',methods=['GET'])
def mean_bill(JD1,JD2):
    [counter_1, counter_2, data] = get_counters(JD1, JD2)
    querried_bills = data['Average Bill'][counter_1:counter_2]
    average_bill = statistics.mean(querried_bills)
    return str(average_bill)

@app.route('/mean_fuel_charge/<JD1>/<JD2>',methods=['GET'])
def mean_fuel_charge(JD1,JD2):
    [counter_1, counter_2, data] = get_counters(JD1, JD2)
    querried_fuel_charge = data['Fuel Charge (Cents/kWh)'][counter_1:counter_2]
    average_fuel_charge = statistics.mean(querried_fuel_charge)
    return str(average_fuel_charge)

@app.route('/mean_kWh/<JD1>/<JD2>',methods=['GET'])
def mean_kWh(JD1,JD2):
    [counter_1, counter_2, data] = get_counters(JD1, JD2)
    querried_kWh = data['Average kWh'][counter_1:counter_2]
    average_kWh = statistics.mean(querried_kWh)
    return str(average_kWh)

@app.route('/graph/kwh/<JD1>/<JD2>',methods=['GET'])
def creategraph_kwh(JD1,JD2):
        [counter_1, counter_2, data] = get_counters(JD1, JD2)
        JD1 = float(JD1)
        JD2 = float(JD2)
        average_kwh = data['Average kWh'][counter_1:counter_2]
        date_range = np.linspace(JD1,JD2,len(average_kwh))
        graph = pygal.Line(x_label_rotation=40, show_minor_x_labels=False)
        graph.title = 'Average kWh Data Over Specified Julian Date Range'
        graph.x_labels = date_range
        graph.x_labels_major = [JD1, JD2]
        graph.add('Average kWh', average_kwh)
        return graph.render_response()

@app.route('/graph/fuel_charge/<JD1>/<JD2>',methods=['GET'])
def creategraph_fuelcharge(JD1,JD2):
        [counter_1, counter_2, data] = get_counters(JD1, JD2)
        JD1 = float(JD1)
        JD2 = float(JD2)
        average_fuelcharge = data['Fuel Charge (Cents/kWh)'][counter_1:counter_2]
        date_range = np.linspace(JD1, JD2, len(average_fuelcharge))
        graph = pygal.Line(x_label_rotation=40, show_minor_x_labels=False)
        graph.title = 'Fuel Charge Data Over Specified Julian Date Range'
        graph.x_labels = date_range
        graph.x_labels_major = [JD1, JD2]
        graph.add('Cents/kWh', average_fuelcharge)
        return graph.render_response()

@app.route('/graph/bill/<JD1>/<JD2>',methods=['GET'])
def creategraph_averagebill(JD1,JD2):
        [counter_1, counter_2, data] = get_counters(JD1, JD2)
        JD1 = float(JD1)
        JD2 = float(JD2)
        average_bill = data['Average Bill'][counter_1:counter_2]
        date_range = np.linspace(JD1, JD2, len(average_bill))
        graph = pygal.Line(x_label_rotation=40, show_minor_x_labels=False)
        graph.title = 'Average Bill Data Over Specified Julian Date Range'
        graph.x_labels = date_range
        graph.add('USD Per Month', average_bill)
        return graph.render_response()

@app.route('/add_data/<year>/<month>/<day>/<kwh>/<fuel_charge>/<bill>',methods=['POST'])
def add_data(year,month,day,kwh,fuel_charge,bill):
    year = int(year)
    month = int(month)
    day = int(day)
    date = pd.Timestamp(year, month, day)
    hour = 0
    minute = 0
    second = 0
    julian_date = 367 * year - math.floor((7 * (year + math.floor((month + 9) / 12))) / 4) + math.floor(
        275 * month / 9) + day + 1721013.5 + (1 / 24) * (hour + (1 / 60) * (minute + second / 60))
    data = get_data()
    modified_data = data.append({'Date': date, 'Average kWh': kwh, 'Fuel Charge (Cents/kWh)': fuel_charge, 'Average Bill': bill, 'Julian Dates': julian_date}, ignore_index=True)
    modified_data.to_csv('Current_data.csv', index=False)
    return modified_data.to_string()

if __name__ == '__main__':
    app.run()