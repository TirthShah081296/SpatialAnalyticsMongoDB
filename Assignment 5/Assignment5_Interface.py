#!/usr/bin/python2.7
#
# Assignment5 Interface
# Name: 
#

from pymongo import MongoClient
import os
import sys
import re
import math
import json

def FindBusinessBasedOnCity(cityToSearch, saveLocation1, collection):
    my_query = {'city': re.compile(cityToSearch, re.IGNORECASE)}
    my_locations = collection.find(my_query)
    file = open(saveLocation1, 'w')
    for business in my_locations:
        file.writelines((business['name']).upper() + '$' + (business['full_address']).upper() +
                        '$' + (business['city']).upper() + '$' + (business['state']).upper() + '\n' )
    file.close()

def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, maxDistance, saveLocation2, collection):
    my_businesses = collection.find()
    file = open(saveLocation2,'w')
    for business in my_businesses:
        count = 0
        for category in categoriesToSearch:
            if category in business['categories']:
                count+=1
        if count==len(categoriesToSearch):
            q_lat = float(business['latitude'])
            q_long = float(business['longitude'])
            given_lat = float(myLocation[0])
            given_long = float(myLocation[1])
            calc_dist = DistanceFunction(q_lat, q_long, given_lat, given_long)
            if calc_dist<=maxDistance:
                file.writelines((business['name']).upper() + '\n')
            else:
                continue
    file.close()

def DistanceFunction(q_lat, q_long, given_lat, given_long):
    R = 3959 # in miles 
    phi_1= math.radians(q_lat)
    phi_2= math.radians(given_lat)
    phi_change = math.radians(given_lat - q_lat)
    lambda_change = math.radians(given_long - q_long)
    a = math.sin(phi_change / 2) * math.sin(phi_change / 2) + math.cos(phi_1) * math.cos(phi_2) *\
                                                              math.sin(lambda_change / 2) * math.sin(lambda_change / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d



