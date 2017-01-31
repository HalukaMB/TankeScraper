
# coding: utf-8

import os
import csv
import time
import requests
import random

from datetime import datetime
from bs4 import BeautifulSoup as BS
#getting the localtime
localtime = datetime.now().strftime("%Y-%b-%d--%H-%M-%S")
print(localtime)

#naming the save file with the localtime
with open(('save_{}.csv').format(localtime), 'w') as resultsfile:
    
    resultsfileWriter = csv.writer(resultsfile)

#creating a list with all postcodes of Germany
    postcodelist = [] 
    with open('NEWplz_de.csv', 'rt') as csvfile:
        PLZ = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in PLZ:
            if len(row) > 0:
                postcodelist.append(row[0])
                
#shuffling the order of the list to make sure that areas' prices are retrieved at different times
    random.shuffle(postcodelist)

    for x in postcodelist:
        #waiting time to ensure that the server is not overrun with requests
        wait_time = random.random() * 2 
        print(wait_time)
        time.sleep(wait_time)
        #retrieving the website for each PLZ area
        petrol_url = 'http://www.clever-tanken.de/tankstelle_liste?spritsorte=5&r=10&ort={}'.format(x)
        print(petrol_url)
        petrol_page = requests.get(petrol_url).text
        #parse the HTML site
        soup = BS(petrol_page, 'html.parser')
        petrol_div = soup.find_all('div', class_='price-entry')
        #retrieve the different entries for each station such as lng, lat, name, price, id
        for station in petrol_div:
            ng_init = station['ng-init'][6:]
            ng_init = ng_init.split("'")
            if len(ng_init) >= 10:
                lat = ng_init[1]
                lon= ng_init[3]
                name= ng_init[7]
                price = ng_init[9]
                output_list=(station['id'],name, lat, lon, price, x)
                resultsfileWriter.writerow(output_list)
