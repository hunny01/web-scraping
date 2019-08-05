#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://in.bookmyshow.com/national-capital-region-ncr/movies/nowshowing'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html')
movieList = []

count = -1
for i in soup.find_all('div', {'class' : 'card-container wow fadeIn movie-card-container'}):
    for j in i.find_all('a'):
        count += 1
        movieList.append(dict(name = j.attrs['title'], link = 'https://in.bookmyshow.com'+j.attrs['href']))

headerList = ['Movie Name', 'Release Date', 'Duration', 'Heart Rating', 'Votes', 'Book Tickets']

with open('NowShowing.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(headerList)

staticURL = r'https://in.bookmyshow.com/buytickets/'
for i in range(0, len(movieList)):
    completeList = []
    
    #Get Movie Details URL
    movieURL = movieList[i].get('link')
    
    #Opening Movie Page
    response = requests.get(movieURL)
    nestedSoup = BeautifulSoup(response.content, 'html')    

    #Splitting Movie URL
    movieURL = movieURL.split('/')
    
    #Get Movie Name
    movieName = movieURL[-2]
    completeList.append(movieName)
    
    #Release Date
    try:
        releaseDate = nestedSoup.find_all("span",{"class":"__release-date"})[0].string
        completeList.append(releaseDate)
    except IndexError:
        completeList.append('-')

    #Time Duration
    try:
        timeDuration = nestedSoup.find_all("span",{"class":"__time"})[0].string
        completeList.append(timeDuration)
    except IndexError:
        completeList.append('-')

    #Heart Rating
    try:
        heartRating = nestedSoup.find_all("span",{"class":"__percentage"})[0].string
        completeList.append(heartRating)
    except IndexError:
        completeList.append('-')

    #Votes
    try:
        votes = str(nestedSoup.find_all("div",{"class":"__votes"}))
        votes = votes.replace('	', '')
        votes = votes.replace('\n', '')
        votes = votes[votes.find('>')+1:votes.find('votes',votes.find('>'))-1]
        completeList.append(votes)
    except IndexError:
        completeList.append('-')    
            
    #Get Booking URL
    bookMovieURL = staticURL + movieName + '-' + movieURL[-4] + '/movie-ncr-' + movieURL[-1] + '-MT/' + datetime.today().strftime('%Y%m%d')
    completeList.append(bookMovieURL)

    with open('NowShowing.csv', 'a', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(completeList)

