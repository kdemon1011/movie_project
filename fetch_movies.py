from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

# Download IMDB's Top 250 data
url = 'http://www.imdb.com/chart/top' # IMDb Top 250 list link
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser') # Get data from the HTML. Alternative is 'lxml'. I prefer 'html.parser'

# As above page soup will contain on ly title, rating and poster information. We need to make request to each movie page to extract the name of the director(s), and the genre information of the movie.

# Get the title links for all the pages
movie_links = [a.find("td",{"class":"titleColumn"}).a.attrs.get('href') for a in soup.find("tbody", {"class":"lister-list"}).findAll("tr")]

prefix = "https://www.imdb.com%s" # href in the above result contains only postfix component. We need to add prefix to access full url

movie_links = [prefix % link for link in movie_links]

# Store required info i.e., diractors' name and genres using followinf function. SCrping will be done using multiprocessing

def scrape_data(movie_page_url):
    print(movie_page_url)
    response = requests.get(movie_page_url)
    page_soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraactin json data which contains all info
    json_data = json.loads(page_soup.find_all("script",type="application/ld+json")[0].text)
    print(json_data)
    title = json_data.get("name",None) # Getting title, if "name" key not found alloating default value None
    genre_list = json_data.get("genre",[]) # Getting genere_list, if "genere" key not found alloating default value empty list
    director = json_data.get("director",[{"name":None}])[0].get("name") # Getting director info, if "director" key not found alloating an array with default name to None
    
    movie_dict = {
        "title":title,
        "genres": genre_list,
        "director": director
    }

    return movie_dict

pool = Pool(cpu_count() * 2) # Creating pool based on cores available on machine
movie_list = pool.map(scrape_data,movie_links[:1])
# print(movie_list)

# df_columns = [ 'title','genres','director']
# df = pd.DataFrame(movie_list, columns=df_columns)
# df.to_csv("./utils/disha_movies.csv",index=False) # Removing index

prefix = "https://www.imdb.com/"
postfix = "/bio?ref_=nm_ov_bio_sm"

url = "name/nm0001104"

final_url = prefix + url + postfix