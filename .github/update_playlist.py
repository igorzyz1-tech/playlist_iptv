import requests
from bs4 import BeautifulSoup

def fetch_dynamic_url(channel_url):
    try:
        response = requests.get(channel_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Пример: Поиск ссылки на потоковое видео в HTML.
        # Это нужно адаптировать под конкретный сайт.
        script_tag = soup.find('script', text=lambda t: 'source:' in t if t else False)
        if script_tag:
            # Извлечение ссылки из текста скрипта
            text = script_tag.string
            start = text.find('source: "') + len('source: "')
            end = text.find('"', start)
            if start != -1 and end != -1:
                return text[start:end]
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
