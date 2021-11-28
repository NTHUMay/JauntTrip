# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 01:47:15 2021

@author: hp
"""

#This package returns the distance and duration information based on user's input of start city and destination city zip code. 
#It will also print out the city name and state abbreviation for both start and destination city.

# Import required library
import requests
import json
from pyzipcode import ZipCodeDatabase
import pandas as pd
import numpy as np
import csv

def get_distance_duration (origin_z , destination_z):
    dd_output_json = []
    dd_output_clean = []
    o_zipcode = origin_z
    d_zipcode = destination_z
    ori_city = []
    des_city = []
    rows = []
    elements = []
    distance = []
    duration = []
    i = 0
    #Place your google map API_KEY to a variable
    apiKey = 'AIzaSyAfm0NA2F5GeZeZY7Oo6pOclWTiNTsQ92Y'
     #Store google maps api url in a variable
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    # call get method of request module and store respose object
    r = requests.get(url + 'origins=' + o_zipcode + '&destinations=' + d_zipcode + '&key=' + apiKey)
    #Get json format result from the above response object
    res = r.json()
    dd_output_json.append(res)
    
    for line in dd_output_json:
        ori_city.append(line['origin_addresses'][0])
        des_city.append(line['destination_addresses'][0])
        rows.append(line['rows'])
        elements.append(rows[i][0]['elements'])
        distance.append(elements[0][0]['distance']['text'])
        duration.append(elements[0][0]['duration']['text'])
        
    dd_output_clean.append(ori_city)
    dd_output_clean.append(des_city)
    dd_output_clean.append(distance)
    dd_output_clean.append(duration)
   
    
    return dd_output_clean