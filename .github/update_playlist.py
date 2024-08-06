import requests
from bs4 import BeautifulSoup
import re

def fetch_dynamic_url(channel_url):
    try:
        response = requests.get(channel_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Поиск ссылок, содержащих '.m3u8'
        for link in soup.find_all('a', href=True):
            if re.search(r'\.m3u8', link['href']):
                return link['href']

        # Альтернативный поиск в тегах <iframe>
        iframe_tag = soup.find('iframe')
        if iframe_tag and 'src' in iframe_tag.attrs:
            iframe_url = iframe_tag['src']
            if iframe_url.startswith('//'):
                iframe_url = 'https:' + iframe_url

            iframe_response = requests.get(iframe_url)
            iframe_soup = BeautifulSoup(iframe_response.content, 'html.parser')
            for link in iframe_soup.find_all('a', href=True):
                if re.search(r'\.m3u8', link['href']):
                    return link['href']
        return None
    except Exception as e:
        print(f'Error fetching URL for {channel_url}: {e}')
        return None

def update_playlist():
    channels = [
        {"name": "Русский Роман", "url": "https://onlinetv.su/tv/kino/122-russkij-roman.html"},
        {"name": "Золотая Колекция", "url": "https://onlinetv.su/tv/kino/122-russkij-roman.html"},
        {"name": "Дом кино Премиум", "url": "https://onlinetv.su/tv/kino/112-dom-kino-premium.html"},
        {"name": "Дом кино", "url": "https://onlinetv.su/tv/kino/110-dom-kino.html"}
    ]
    
    playlist = '#EXTM3U\n'
    
    for channel in channels:
        dynamic_url = fetch_dynamic_url(channel["url"])
        if dynamic_url:
            playlist += f'#EXTINF:-1 tvg-name="{channel["name"]}",{channel["name"]}\n{dynamic_url}\n'
        else:
            print(f'Failed to fetch dynamic URL for {channel["name"]}')
    
    with open('playlist.m3u', 'w') as file:
        file.write(playlist)
    print('Playlist updated successfully.')

if __name__ == "__main__":
    update_playlist()

import requests
from bs4 import BeautifulSoup
import re

def fetch_dynamic_url(channel_url):
    try:
        response = requests.get(channel_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Поиск ссылок, содержащих '.m3u8'
        for link in soup.find_all('a', href=True):
            if re.search(r'\.m3u8', link['href']):
                return link['href']

        # Альтернативный поиск в тегах <iframe>
        iframe_tag = soup.find('iframe')
        if iframe_tag and 'src' in iframe_tag.attrs:
            iframe_url = iframe_tag['src']
            if iframe_url.startswith('//'):
                iframe_url = 'https:' + iframe_url

            iframe_response = requests.get(iframe_url)
            iframe_soup = BeautifulSoup(iframe_response.content, 'html.parser')
            for link in iframe_soup.find_all('a', href=True):
                if re.search(r'\.m3u8', link['href']):
                    return link['href']
        return None
    except Exception as e:
        print(f'Error fetching URL for {channel_url}: {e}')
        return None

def update_playlist():
    channels = [
        {"name": "Русский Роман", "url": "https://onlinetv.su/tv/kino/122-russkij-roman.html"},
        {"name": "Золотая Колекция", "url": "https://onlinetv.su/tv/kino/122-russkij-roman.html"},
        {"name": "Дом кино Премиум", "url": "https://onlinetv.su/tv/kino/112-dom-kino-premium.html"},
        {"name": "Дом кино", "url": "https://onlinetv.su/tv/kino/110-dom-kino.html"}
    ]
    
    playlist = '#EXTM3U\n'
    
    for channel in channels:
        dynamic_url = fetch_dynamic_url(channel["url"])
        if dynamic_url:
            playlist += f'#EXTINF:-1 tvg-name="{channel["name"]}",{channel["name"]}\n{dynamic_url}\n'
        else:
            print(f'Failed to fetch dynamic URL for {channel["name"]}')
    
    with open('playlist.m3u', 'w') as file:
        file.write(playlist)
    print('Playlist updated successfully.')

if __name__ == "__main__":
    update_playlist()
