import requests
from bs4 import BeautifulSoup
import time
from .models import Artist, Festival, FestivalArtist

def scrape_page(url):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <h2> elements containing an <a> tag with the specified href attribute
    h2_elements = soup.find_all('h2')

    # Extract the text from each <a> tag within the <h2> elements
    for h2 in h2_elements:
        a_tag = h2.find('a')
        if a_tag:
            festival_name = a_tag.text.strip()
            website_link = a_tag['href']
            festival, _ = Festival.objects.get_or_create(name=festival_name)
            time.sleep(1)
            
            response = requests.get(website_link, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            div_section = soup.find('div', class_='hublineup')
            
            if div_section:
                artist_elements = div_section.find_all('li')
                artists = []
                for element in artist_elements:
                    artist_name = element.get_text(strip=True).upper()
                    artists.append(artist_name)
                     
                for name in artists:
                    artist, created = Artist.objects.get_or_create(name=name)
                    if created or not FestivalArtist.objects.filter(artist=artist, festival=festival).exists():
                        FestivalArtist.objects.create(festival=festival, artist=artist)


            print(f"Successfully added lineup to database for festival: {festival_name}")            
            time.sleep(5)

