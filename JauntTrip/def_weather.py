#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 13:40:41 2021

@author: sheshaliwarik
"""


# The objective of this method is to obtain weather information for the destination city 
# for the date added by the user. It makes an API call to a weather API that forecasts the data for the mentioned day

#Importing Libraries

from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

def get_weather_data (city_name, date_of_travel):
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+city_name+'/'+str(date_of_travel)+'?unitGroup=us&key=5WZNK4UQVFR2B9WLDNMMZ3C82'
    page = requests.get(url)
    soup = BeautifulSoup (page.content, 'html.parser')
    data = json.loads(soup.text)
    print("\n")
    print("Weather Information for " + city_name + " on " + str(date_of_travel))
    
    for key, values in data.items():
        if(key == 'days'):
            temp = values                                          #temp is a list with 1 element which is a dict
            for i,j in temp[0].items():
                if(i=='tempmax'):
                    temp_max=j
                if(i=='tempmin'):
                    temp_min=j
                if(i=='humidity'):
                    humidity=j
                if(i=='windspeed'):
                    windspeed=j
                if(i=='conditions'):
                    condition =j

   
    print("\n")
    print("Maximum Temperature:   " + str(temp_max)+"f")
    print("Minimum Temperature:   " + str(temp_min)+"f")
    print("Wind Speed         :   " + str(windspeed)+" mph")
    print("Humidity           :   " + str(humidity))
    print("Weather Condition - " + condition) 
    print("\n")

       
       
def get_historical_data(city_name, date_of_travel):
    
    temp_date= date_of_travel.replace('-', " ")
    date_object = datetime.strptime(temp_date, '%Y %m %d').date()
    new_date = date_object - relativedelta(months=12)
    
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+city_name+'/'+str(new_date)+'?unitGroup=us&key=5WZNK4UQVFR2B9WLDNMMZ3C82'
    page = requests.get(url) 
    soup = BeautifulSoup (page.content, 'html.parser')
    data = json.loads(soup.text)

    temp_arr = np.zeros(23)
    hum_arr = np.zeros(23)


    for i, j in data.items():
     if(i=='days'):
        for a, b in j[0].items(): 
              if(a=='description'):
                  weather_cond=b  
              if(a=='hours'):
                   for i in range(len(b)-1):
                     for key, value in b[i].items():
                         if(key=='temp'):
                             temp_arr= np.insert(temp_arr,i, value)
                             temp_arr=np.trim_zeros(temp_arr, 'b')
                     for key, value in b[i].items():
                         if(key=='humidity'):
                             hum_arr=np.insert(hum_arr, i, value)
                             hum_arr=np.trim_zeros(hum_arr, 'b')
       
    
    print("Last year THIS DAY - " + str(new_date) )   
    print(weather_cond)
    
    y=[i for i in range(23)]
    # plotting
    plt.title("Historical Data for this day last year " + str(new_date))
    plt.xlabel("Hours of the day ")
    plt.ylabel("Temperature (in f) ")
    plt.plot( y, temp_arr, label='Temperature')
    plt.plot( y, hum_arr,  label='Humidity')
    plt.margins(x=0, y=0)
    plt.xticks(y)
    plt.legend()
    plt.show()      
       
    
    
    
    
       
       
       
       