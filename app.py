from flask import Flask, request, jsonify
import json
import os
import statistics
import datetime
import math
import data_collector


app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World'

def get_data():
    data = data_collector.obtain_data()
    return data

@app.route('/data', methods=['GET'])
def list_data():
    data = get_data()
    return str(data)

#adds new 100 new and unique animals via a post command or displays all animals via a get command
@app.route('/animals', methods=['GET', 'POST'])
def animals():
    if request.method == 'GET':
        file_exists = os.path.exists("all_animals.txt")
        if file_exists == 0:
            return 'no animals'
        filesize = os.path.getsize("all_animals.txt")
        if filesize == 0:
            return 'no animals'
        if filesize == 2:
            return 'no animals'
        else:
            with open('all_animals.txt') as json_file:
                all_animals = json.load(json_file)
            return jsonify({'animals': [all_animals]})
    if request.method == 'POST':
        file_exists = os.path.exists("all_animals.txt")
        if file_exists == 0:
            open("all_animals.txt", "w+")

        with open('all_animals.txt') as json_file:
            all_animals = json.load(json_file)

        value = len(all_animals)

        new_animals = get_new_data(value)


        for animal in new_animals:
            all_animals.append(animal)

        with open('all_animals.txt', 'w') as outfile:
            json.dump(all_animals, outfile)

        return jsonify({'animals': [all_animals]})

#clears all animals that where previously generated
@app.route('/clear_animals',methods=['POST'])
def clear_animals():
    all_animals = []
    with open('all_animals.txt', 'w') as outfile:
        json.dump(all_animals, outfile)
    with open('Teds_Animals_temp.txt', 'w') as outfile:
        json.dump(all_animals, outfile)
    return "Animals Cleared"

#returns all animals with specified head type
@app.route('/heads/<animal>', methods=['GET'])
def get_head(animal):
    temp_data = []
    d = get_data()
    a = animal
    for objects in d:
        if objects[0] == a:
            temp_data.append(objects)
    return jsonify({'animals': [temp_data]})

#returns mean number of arms in current list of animals
@app.route('/mean_arms',methods=['GET'])
def mean_arms():
    temp_data = []
    d = get_data()
    for objects in d:
        temp_data.append(objects[1])
    average_arms = statistics.mean(temp_data)
    return str(average_arms)

#returns mean number of legs in current list of animals
@app.route('/mean_legs',methods=['GET'])
def mean_legs():
    temp_data = []
    d = get_data()
    for objects in d:
        temp_data.append(objects[2])
    average_legs = statistics.mean(temp_data)
    return str(average_legs)

#allows you to edit an animal with the specified uuid and puts the animal back into the list of all animals at its original position allows you to choose 'same' if you don't want to change a certain characteristic
@app.route('/edit_animal/<uuid>/<head>/<arm>/<leg>/<tail>',methods=['POST'])
def edit_animal(uuid, head, arm, leg, tail):

    with open('all_animals.txt') as json_file:
        d = json.load(json_file)

    temp_animal = []
    counter = -1
    print(d)
    for objects in d:
        counter = counter + 1
        print(counter)
        if objects[5] == uuid:
            location_animal = counter
            temp_animal.append(objects)
            initial_head = objects[0]
            initial_arm = objects[1]
            initial_leg = objects[2]
            initial_tail = objects[3]
            time_stamp = ': {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            year = int(time_stamp[0:4])
            month = int(time_stamp[5:7])
            day = int(time_stamp[8:10])
            hour = int(time_stamp[11:13])
            minute = int(time_stamp[14:16])
            second = int(time_stamp[17:19])
            julian_date = 367 * year - math.floor((7 * (year + math.floor((month + 9) / 12))) / 4) + math.floor(
                275 * month / 9) + day + 1721013.5 + (1 / 24) * (hour + (1 / 60) * (minute + second / 60))

    if 'location_animal' in locals():
        if head == 'same':
            temp_animal.append(initial_head)
        else:
            temp_animal.append(head)
        if arm == 'same':
            temp_animal.append(initial_arm)
        else:
            temp_animal.append(arm)
        if leg == 'same':
            temp_animal.append(initial_leg)
        else:
            temp_animal.append(leg)
        if tail == 'same':
            temp_animal.append(initial_tail)
        else:
            temp_animal.append(tail)
    else:
        return 'uuid does not exist'

    temp_animal.append(time_stamp)
    temp_animal.append(uuid)
    temp_animal.append(julian_date)

    d[location_animal] = temp_animal

    with open('all_animals.txt', 'w') as outfile:
        json.dump(d, outfile)
    return 'Animal has been edited'

#querry a range of Julian Dates. I chose my time system as Julian dates because they're much easier to work with when looking for dates within a range
@app.route('/query_dates/<JD1>/<JD2>', methods=['GET'])
def query_dates(JD1,JD2):
    JD1 = float(JD1)
    JD2 = float(JD2)
    dates = []
    querried_dates = []
    d = get_data()
    counter_1 = 0
    counter_2 = 0
    for objects1 in d:
        dates.append(objects1[6])
    for objects2 in dates:
        counter_1 = counter_1 + 1
        if objects2 >= JD1:
            for objects3 in dates:
                counter_2 = counter_2 + 1
                if objects3 >= JD2:
                    for ii in range(counter_1, counter_2):
                        querried_dates.append(dates[ii])
                    return jsonify({'animals': [querried_dates]})

#allows user to input a range of Julian Dates and returns all animals that are outside of this range of dates
@app.route('/query_dates_animals/<JD1>/<JD2>', methods=['GET'])
def query_dates_animals(JD1,JD2):
    JD1 = float(JD1)
    JD2 = float(JD2)
    dates = []
    querried_animals = []
    d = get_data()
    counter_1 = 0
    counter_2 = 0
    for objects1 in d:
        dates.append(objects1[6])
    for objects2 in dates:
        counter_1 = counter_1 + 1
        if objects2 >= JD1:
            for objects3 in dates:
                counter_2 = counter_2 + 1
                if objects3 >= JD2:
                    for ii in range(0, counter_1 - 1):
                        querried_animals.append(d[ii])
                    for ii in range(counter_2, (len(d) - 1)):
                        querried_animals.append(d[ii])
                    with open('all_animals.txt', 'w') as outfile:
                        json.dump(querried_animals, outfile)
                    return jsonify({'animals': [querried_animals]})

#allows user to delete an animal with a specific uuid
@app.route('/remove_animal/<uuid>', methods=['Get'])
def remove_animal(uuid):
    appended_list = []
    d = get_data()
    for animal in d:
        if animal[5] != uuid:
            appended_list.append(animal)
    with open('all_animals.txt', 'w') as outfile:
        json.dump(appended_list, outfile)
    return jsonify({'animals': [appended_list]})

if __name__ == '__main__':
    app.run()