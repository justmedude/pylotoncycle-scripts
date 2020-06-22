#!/usr/bin/env python

import time

import common

# class_type_dict = {}
global class_type_dict
class_type_dict = {}



def GenWorkoutData(data):
    wlist = []
    for workout in data:
        class_type_id = workout['class_type_ids'][0]
        class_type = class_type_dict[class_type_id]
        fitness_discipline = workout['fitness_discipline']
        original_air_time = time.ctime(workout['original_air_time'])
        instructor_id = workout['instructor_id']
        try:
            instructor = conn.GetInstructorById(instructor_id)['name']
        except KeyError:
            instructor = 'None'
        length_in_minutes = workout['pedaling_duration'] / 60
        wstr = '%s,%s,%s,%s,%s\n' % (
            original_air_time, class_type,
            fitness_discipline, instructor, length_in_minutes)
        wlist.append(wstr)
    return wlist


if __name__ == '__main__':
    url = 'https://api.onepeloton.com/api/v2/ride/archived?limit=500&page=%s'
    conn = common.get_connection()

    fetch_url = url % '0'
    resp = conn.GetUrl(fetch_url)
    page_count = resp['page_count']

    # class id dictionary
    for i in resp['class_types']:
        class_type_dict[i['id']] = i['name']

    lines = GenWorkoutData(resp['data'])
    f = open('AllWorkouts.csv', 'w')
    for i in lines:
        f.write(i)

    for p in range(1, page_count):
        fetch_url = url % p
        resp = conn.GetUrl(fetch_url)
        lines = GenWorkoutData(resp['data'])
        for i in lines:
            f.write(i)
    f.close()
    print('Finished Fetching Workouts')
