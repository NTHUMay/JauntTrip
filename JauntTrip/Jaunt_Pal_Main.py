# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 03:03:09 2021
"""

# get user date and check for correct format
from datetime import datetime as dt
from datetime import date
# get city and state from zipcode 
from pyzipcode import ZipCodeDatabase
# for regular expressions
import re
import def_dd
import def_weather
import Yelp_data_scrape
import Tripadvisor

print("\n")
print("Welcome to JauntPal. Let's plan for a jaunt trip.")


#gets the userdate from user
d = True
while d:
    try:
        inputdate = input("When do you want to start the trip? (Month/Day/Year) \n")
        dateformat = "%m/%d/%Y"
        startdate =  dt.strptime(inputdate,dateformat)  
        # check if the input date is in the future  
        if date.today() > startdate.date():
            print("\nSorry, we cannot travel back in time at this stage. Please give me a future date for now.")   
            inputdate = input("When do you want to start the trip? (Month/Day/Year) \n")
    except:
        print("Wrong format. Please type in your start date as Month/Day/Year (ex. 10/20/2021)") 
    else:
        d = False
        #changesuserdate to URL format yyyy-mm-dd to pass into webscrape
        startdate = str(startdate.date())
 
#get zipcode from user        
zipcode_db = ZipCodeDatabase()    
z_start = True
while z_start:
     start_zipcode = input("Please type in the 5 digit zipcode of your original city: \n")
     #check if user enters valid pincode.A valid pincode is of length 5 digits.  
     if not re.search(r'^[0-9][0-9][0-9][0-9][0-9]$', start_zipcode) != None:
         print("Invalid zipcode.")
     #check if the zipcode exists in the database  
     if not zipcode_db[start_zipcode] != None:
         print("Oops! It seems like we did not get your input.")       
     else:
         z_start = False
         start_city = zipcode_db[start_zipcode].city
         start_state = zipcode_db[start_zipcode].state
        
#get zipcode of the destination from user
z_des = True
while z_des:
    des_zipcode = input("Please type in the 5 digit zipcode of your destination city: \n")
    #check if user enters valid pincode.A valid pincode is of length 5 digits.  
    if not re.search(r'^[0-9][0-9][0-9][0-9][0-9]$', des_zipcode) != None:
        print("Invalid zipcode.")
    #check if the zipcode exists in the database  
    if not zipcode_db[des_zipcode] != None:
        print("Oops! It seems like we did not get your input.")       
    else:
        z_des = False
        des_city = zipcode_db[des_zipcode].city
        des_state = zipcode_db[des_zipcode].state
        
       
# define the function blocks
def distance():
    dd_data = []

    dd_data = def_dd.get_distance_duration (start_zipcode , des_zipcode)
    print('\n')
    print("Your jaunt trip from " + start_city +" "+start_state)
    print("to "+des_city+" "+des_state+" will take "+dd_data[3][0]+" of drive.")
    print("The distance between these two places is: "+dd_data[2][0])

    print('\n')
    

def weather():
    def_weather.get_weather_data(des_city, startdate)
    def_weather.get_historical_data(des_city,startdate)
    print('\n')

def restaurants():
    Yelp_data_scrape.askAgain = 0
    valid_price = False

    while(not valid_price):
        priceRange = input("Food is vital for a jaunt. What is your budget today? Enter $, $$, $$$ or $$$$: \n")
        if priceRange not in('$','$$', '$$$', '$$$$'):
            print('Sorry, please only enter in prescribed form.')
        else:
            valid_price = True
            Yelp_data_scrape.metrics_df = Yelp_data_scrape.collectRestaurant(des_zipcode)
            Yelp_data_scrape.displayRestaurant(des_zipcode, priceRange)
    
    askMore = True

    while(askMore):
        answer = input("Not satisfied? Do you want to look at other restaurants? Type Y or N: \n")
        if answer.upper() == 'Y':
            Yelp_data_scrape.askAgain += 5
            # Reached the end of all restaurants
            if Yelp_data_scrape.displayRestaurant(des_zipcode, priceRange) == -1:
                askMore = False 
                break
        else:
            print('\n')
            print("Seems like you've picked your favorite. Great choice!")
            askMore = False
            break
    
    print('\n')
   
   
def tourism():
    count = 1
    checkAgain = True

    destinationList = Tripadvisor.attraction(des_city)
    Tripadvisor.displayAttraction(destinationList, count)
    while(checkAgain):
        answer = input("Not satisfied? Do you want to look at other attractions? Type Y or N: \n")
        if answer.upper() == 'Y':
            count += 1
            Tripadvisor.displayAttraction(destinationList, count)
        else:
            print("Seems like you know where to go! Have a nice one!")
            checkAgain = False
        
while True:
    print("\n")
    print("1. Distance & Commute Information")
    print("2. Weather Forecast")
    print("3. Restaurant Recommendation")
    print("4. Tourist Spots Recommendation")
    print("5. Exit")
    inputoption = input("Please enter your choice \n")
    inputoption=int(inputoption)

    if(inputoption==1):
        distance()
    elif(inputoption==2):
        weather()
    elif(inputoption==3):
        restaurants()
    elif(inputoption==4):
        tourism()
    elif(inputoption==5):
        print("\nThank you for using JauntPal! We hope you enjoy your jaunt trip! \n")
        break
    else:
        print("You've entered an invalid choice. Please try again")
   


