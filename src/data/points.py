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
        with open('score.txt', mode='a', newline='') as score_file:
            writer = csv.writer(score_file)
            writer.writerow([username, points])
    except FileNotFoundError:
        with open('score.txt', mode='w') as score_file:
            writer = csv.writer(score_file)
            writer.writerow((username, points))


def read_points():
    '''
    Reads from the file and returns high score list in an ascending order.
    '''
    with open('score.txt', 'r') as score_file:
        reader = csv.reader(score_file)
        high_score = []
        if len(high_score) > 0:
            for row in reader:
                if (row[0] != 'testi'):
                    high_score.append((row[0], int(row[1])))
        high_score.sort(key=lambda tup: tup[1], reverse=True)
    return high_score
