import requests
from bs4 import BeautifulSoup

def fetch_dynamic_url(channel_url):
    print(f'Fetching dynamic URL for {channel_url}')
    response = requests.get(channel_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Предположим, что поток находится в теге <iframe>
    iframe_tag = soup.find('iframe')
    if iframe_tag and 'src' in iframe_tag.attrs:
        print(f'Found URL: {iframe_tag["src"]}')
        return iframe_tag['src']
    print('No URL found')
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
    
    with open('playlist.m3u', 'w') as file:
        file.write(playlist)
    print('Playlist updated successfully.')

if __name__ == "__main__":
    update_playlist()
