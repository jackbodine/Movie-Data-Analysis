# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 20:23:58 2020

@author: Dell
"""
from bs4 import BeautifulSoup
import re
import time
import requests
import csv


def run(name):
    name = name.replace(" ", "_")
    name = name.replace("'", "")
    name = name.replace(",", "")
    name = name.replace(".", "")
    name = name.replace(":", "")

    print("Running Review Scraper on: ", name)
    pageNum = 3
    url_1 = 'https://www.rottentomatoes.com/m/' 
    url = url_1 + str(name) + '/reviews/'
    fw=open('reviews.csv','w',encoding='utf8') # output file

    writer=csv.writer(fw,lineterminator='\n')#create a csv writer for this file
    
    for p in range(1,pageNum+1): # for each page 

        print ('page',p)
        html=None

        if p==1: pageLink=url # url for page 1
        else: pageLink=url+'?type=&sort=&page='+str(p)# make the page url
        
        for i in range(5): # try 5 times

            #send a request to access the url
            response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
                break # we got the file, break the loop
            else:time.sleep(2) # wait 2 secs
            
   
        # all five attempts failed, return  None
        if not response: return None
        
        html=response.text# read in the text from the file
        
        soup = BeautifulSoup(html,'html') # parse the html 

        reviews=soup.findAll('div', {'class':'row review_table_row'}) # get all the review divs
        
        critic, rating, source, text, date ='NA','NA','NA','NA','NA' # initialize critic and text         
        
        for review in reviews:
            criticChunk=review.find('a',{'href':re.compile('/critic/')})
            if criticChunk: critic=criticChunk.text.strip()
    
            ratingChunk = review.find('div',{'class': re.compile('review_icon')})
            rating_Chunk = str(ratingChunk)
            if (rating_Chunk.find('rotten')>0):
                rating = 'rotten'
            if (rating_Chunk.find('fresh')>0):
                rating= 'fresh'

            sourceChunk = review.find('em',{'class': 'subtle critic-publication'})
            if sourceChunk: source = sourceChunk.text.strip() 
            
            textChunk=review.find('div',{'class':'the_review'})
            if textChunk: text=textChunk.text.strip()
        
            dateChunk = review.find('div',{'class':'review-date'})
            if dateChunk: date = dateChunk.text.strip()
            
            writer.writerow([critic, rating, source, text, date])
    fw.close()
    
#run('titanic')   