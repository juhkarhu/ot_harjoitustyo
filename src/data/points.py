'''
Module for writing and reading scores to file in order to maintain highscore list.
'''

import csv

def write_points(username, points):
    '''
    Checks if the file already exists and eppends to it.
    Parameters are username and points.
    '''
    try:
        with open('score.txt', mode='a') as score_file:
            writer = csv.writer(score_file)
            writer.writerow([username, points])
    except FileNotFoundError:
        with open('score.txt', mode='w') as score_file:
            writer = csv.writer(score_file)
            writer.writerow([username, points])


def read_points():
    '''
    Reads from the file and returns high score list in an ascending order.
    '''
    with open('score.txt', 'r') as score_file:
        reader = csv.reader(score_file)
        high_score = []
        for row in reader:
            high_score.append((row[0], int(row[1])))
        high_score.sort(key=lambda tup: tup[1], reverse=True)
        # for x in high_score:
        #     print(x)
    return high_score
