#!/usr/bin/env python

import time

import common

# class_type_dict = {}
global class_type_dict
class_type_dict = {}

global filehandle_dict
filehandle_dict = {}


def WriteWorkoutData(data):
    wlist = []
    for workout in data:
        class_type_id = workout['class_type_ids'][0]
        class_type = class_type_dict[class_type_id]
        fitness_discipline = workout['fitness_discipline']
        title = workout['title']
        original_air_time = time.ctime(workout['original_air_time'])
        instructor_id = workout['instructor_id']
        try:
            instructor = conn.GetInstructorById(instructor_id)['name']
        except KeyError:
            instructor = 'None'
        length_in_minutes = workout['pedaling_duration'] / 60
        wstr = '%s,%s,%s,%s,%s\n' % (
            original_air_time, title,
            instructor, length_in_minutes, class_type)
        filehandle_dict[fitness_discipline].write(wstr)
    return wlist


if __name__ == '__main__':
    url = 'https://api.onepeloton.com/api/v2/ride/archived?limit=500&page=%s'
    conn = common.get_connection()

    fetch_url = url % '0'
    resp = conn.GetUrl(fetch_url)
    page_count = resp['page_count']

    # Generate a dictionary of file handles. One file per fitness_discipline
    # All init the files with the headers that will get written
    header_string = 'Original Air Date,Title,Instructor,Length,Type\n'
    for i in resp['fitness_disciplines']:
        i = i['id']
        filename = 'workouts/%s.csv' % i
        filehandle_dict[i] = open(filename, 'w')
        filehandle_dict[i].write(header_string)

    # class id dictionary
    for i in resp['class_types']:
        class_type_dict[i['id']] = i['name']

    lines = WriteWorkoutData(resp['data'])

    for p in range(1, page_count):
        fetch_url = url % p
        resp = conn.GetUrl(fetch_url)
        lines = WriteWorkoutData(resp['data'])

    for i in filehandle_dict:
        filehandle_dict[i].close()
    print('Finished Fetching Workouts')
