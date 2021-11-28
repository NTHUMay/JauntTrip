# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 23:25:53 2021

@author: Evelyn
"""

#This package helps get restaurant data from Yelp's page and returns recommended restaurants based on user's budget and Yelp ratings.

import requests
import bs4
import json
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


#This method crawls data from Yelp's page based on a given zip code. It will return a cleaned DataFrame including all restaurants' information.
def collectRestaurant(des_zipcode):
    
    print('Wait while we load data from Yelp... It may take up to 1 min\n')

    name_per_page = []
    price_per_page = []
    reviewNum_per_page = []
    rating_per_page = []
    businessUrl_per_page = []
    
    
    headers = {
    'Connection': 'keep-alive',   
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded'  
    }
    
    is_valid_page = True
    pageTurner = 0
    
    while (is_valid_page):
        url = "https://www.yelp.com/search/snippet?find_desc=Restaurants&find_loc={}&start={}&parent_request_id=2da3413f8d0610c1&request_origin=user".format(des_zipcode, pageTurner)
    
        # Submit GET request
        r = requests.get(url=url, headers=headers, verify=False)
        content = bs4.BeautifulSoup(r.text, 'lxml')
        result = json.loads(content.text)
        
        # Invalid page
        try:
            uncleaned_dict = result['searchPageProps']['mainContentComponentsListProps'][4:21]
        except:
            is_valid_page = False
            break
        
        # End of restaurant list in search result
        if len(uncleaned_dict) < 17:
            is_valid_page = False
            break 
        
        for restaurant in uncleaned_dict:
            if restaurant.get('searchResultBusiness') != None:
                info_dict = restaurant.get('searchResultBusiness')
                name_per_page.append(info_dict['name'])
                price_per_page.append(info_dict['priceRange'])
                reviewNum_per_page.append(info_dict['reviewCount'])
                rating_per_page.append(info_dict['rating'])
                businessUrl_per_page.append('yelp.com{}'.format(info_dict['businessUrl']))
        pageTurner += 10
    
    metrics_dict = {'Name':name_per_page, 'Price range':price_per_page, 'Review count':reviewNum_per_page, 
                    'Rating':rating_per_page, 'Business url':businessUrl_per_page}
    metrics_df = pd.DataFrame(metrics_dict)
    return metrics_df


# Initialize restaurant DataFrame
metrics_df = 0
# Track restaurant to display if user asks more than once
askAgain = 0

#This method extracts price, review counts, rating and business website information from the DataFrame returned by collectRestaurant method. Then a max of 5 restaurants will be displayed each time.
def displayRestaurant(des_zipcode, price):
    
    # Gid rid of restaurants that have <100 reviews (average rating have not stablized)
    # Referrence: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0252157
    valid_df = metrics_df[metrics_df['Review count'] > 100]
    price_df = valid_df[valid_df['Price range'] == price]
    sorted_by_rating = price_df.sort_values('Rating', ascending=False)
    pd.set_option('display.max_colwidth', None)
    target_restaurant = sorted_by_rating.iloc[askAgain:askAgain+5, [0,4]]
    if not target_restaurant.empty:
        print("We've found the following restaurants near {}. Enjoy!\n\n".format(des_zipcode))
        print(target_restaurant)
    else:
        print("You've reached the end of restaurant list. You must pick!")
        return -1

