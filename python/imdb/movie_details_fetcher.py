import os
import requests
from bs4 import BeautifulSoup
import re
import json

def read_movie_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return urls

def read_and_sort_average_ratings(file_path):
    avg_ratings = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                try:
                    url = parts[0].split('/usercomments')[0]
                    avg_rating = float(parts[1])
                    movie_id = int(re.search(r'tt(\d+)', url).group(1))
                    avg_ratings.append((movie_id, avg_rating, url))
                except (ValueError, AttributeError):
                    print(f'Advertencia: línea ignorada debido a formato incorrecto: {line.strip()}')
    avg_ratings.sort(key=lambda x: x[1], reverse=True)
    return avg_ratings

def get_top_bottom_movies(avg_ratings, top_n=10):
    top_movies = avg_ratings[:top_n]
    bottom_movies = avg_ratings[-top_n:]
    return top_movies, bottom_movies

def get_movie_details_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.text
            match = re.search(r'(.*)\s+\((\d{4})\)', title_text)
            if match:
                return match.group(1).strip(), int(match.group(2))

        script_tags = soup.find_all('script', type='application/ld+json')
        for script in script_tags:
            try:
                data = script.string
                movie_data = json.loads(data)
                if movie_data.get('@type') == 'Movie':
                    name = movie_data.get('name', 'Unknown')
                    date_published = movie_data.get('datePublished', 'Unknown')
                    return name, int(date_published[:4]) if date_published != 'Unknown' and date_published[:4].isdigit() else 'Unknown'
            except json.JSONDecodeError:
                continue
    except requests.RequestException as e:
        print(f'Error al acceder a {url}: {e}')

    return 'Unknown', 'Unknown'