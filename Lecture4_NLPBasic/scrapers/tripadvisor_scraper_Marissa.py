import requests
import csv
import bs4
from pygeocoder import Geocoder
from pygeocoder import GeocoderError

hotel_page = 'http://www.tripadvisor.com/Hotels-g190391-Andorra-Hotels.html'
attraction_page = "http://www.tripadvisor.com/Attractions-g190391-Activities-Andorra.html"
food_page = "http://www.tripadvisor.com/Restaurants-g190391-Andorra.html"
places =[]
def get_hotel_urls():
    
    response = requests.get(hotel_page)
    hotel_urls = [];
    soup = bs4.BeautifulSoup(response.text)
    for x in soup.findAll("div", {"id": "INLINE_COUNT"}):
        print x
    for a in soup.select('div.listing_title a.property_title'):
        hotel_urls.append(a.get('href'))
    for url in hotel_urls[0:3]:
        get_info('http://www.tripadvisor.com'+url, "hotel")
    wirte_results()

  #  get_attraction_urls()
def get_attraction_urls():
    
    response = requests.get(attraction_page)
    urls = [];
    soup = bs4.BeautifulSoup(response.text)
    for a in soup.select('.property_title a'):
        urls.append(a.get('href'))
    for url in urls:
       get_info('http://www.tripadvisor.com'+url, "attraction")
    get_food_urls()

def get_food_urls():
    
    response = requests.get(food_page)
    locs = [];
    soup = bs4.BeautifulSoup(response.text)
    for a in soup.select('.geo_name a'):
        locs.append(a.get('href'))
    for loc in locs:
        urls =[]
        response2 = requests.get('http://www.tripadvisor.com'+loc)
        soup2 = bs4.BeautifulSoup(response2.text)
        for y in soup2.select('a.property_title'):
            urls.append(y.get('href'))
        for url in urls:
            get_info('http://www.tripadvisor.com'+url, "restaurant")
  
    write_results()

def get_info(url, type):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)
    lats=''
    longs =''
    try:
        name = soup.select('div.heading_name_wrapper h1.heading_name')[0].get_text().encode('utf-8')
        rating = soup.select('img.sprite-rating_rr_fill')[0].get('content').encode('utf-8')
        street = soup.select('span.format_address')[0].get_text().encode('utf-8')
        try:
            results = Geocoder.geocode(street)
            longs = str(results[0].longitude).encode('utf-8')
            lats = str(results[0].latitude).encode('utf-8')
        except GeocoderError:
            print "bad geo"
        place = {"place":name, "type":type, "rating":rating, "address" : street, "long":longs, "lat":lats}
        places.append(place);
    except IndexError:
        print "bad result"

def write_results():
    keys = places[0].keys()
    with open('places.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(places)

get_hotel_urls()

