import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, parse_qs

def fetch_dynamic_url(channel_url, debug_file):
    try:
        # Настройка Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Запуск в фоновом режиме
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(channel_url)
        debug_file.write(f'Fetched main page for {channel_url}\n')
        time.sleep(5)  # Ждем загрузки страницы и выполнения скриптов

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Поиск тега <div class="page__player video-inside"> и внутри него тега <video> с атрибутом src
        player_div = soup.find('div', class_='page__player video-inside')
        if player_div:
            video_tag = player_div.find('video')
            if video_tag:
                source_tag = video_tag.find('source', src=True)
                if source_tag and '.m3u8' in source_tag['src']:
                    stream_url = source_tag['src']
                    debug_file.write(f'Found stream URL: {stream_url}\n')

                    # Проверка доступности URL
                    response = requests.get(stream_url, stream=True)
                    if response.status_code == 200:
                        parsed_url = urlparse(stream_url)
                        params = parse_qs(parsed_url.query)
                        
                        token = params.get('token', [None])[0]
                        if token:
                            expiry_time = int(token.split('-')[2])
                            current_time = int(time.time())
                            
                            if current_time < expiry_time:
                                debug_file.write(f'URL is accessible and valid: {stream_url}\n')
                                driver.quit()
                                return stream_url
                            else:
                                debug_file.write(f'Token has expired: {stream_url}\n')
                        else:
                            debug_file.write(f'No token found in URL: {stream_url}\n')
                    else:
                        debug_file.write(f'URL is not accessible, status code: {response.status_code}\n')

        driver.quit()
        return None
    except Exception as e:
        debug_file.write(f'Error fetching URL for {channel_url}: {e}\n')
        return None

def update_playlist():
    channels = [
        {"name": "Русский Роман", "url": "https://onlinetv.su/tv/kino/122-russkij-roman.html"},
        {"name": "Золотая Колекция", "url": "https://onlinetv.su/tv/kino/122-russkij-roman.html"},
        {"name": "Дом кино Премиум", "url": "https://onlinetv.su/tv/kino/112-dom-kino-premium.html"},
        {"name": "Дом кино", "url": "https://onlinetv.su/tv/kino/110-dom-kino.html"}
    ]
    
    with open('playlist.m3u', 'w') as playlist_file, open('debug_log.txt', 'w') as debug_file:
        playlist_file.write('#EXTM3U\n')
        for channel in channels:
            debug_file.write(f'Fetching dynamic URL for {channel["name"]}\n')
            dynamic_url = fetch_dynamic_url(channel["url"], debug_file)
            if dynamic_url:
                playlist_file.write(f'#EXTINF:-1 tvg-name="{channel["name"]}",{channel["name"]}\n{dynamic_url}\n')
                debug_file.write(f'Successfully fetched URL for {channel["name"]}\n')
            else:
                playlist_file.write(f'#EXTINF:-1 tvg-name="{channel["name"]}",{channel["name"]} - URL not found\n')
                debug_file.write(f'Failed to fetch dynamic URL for {channel["name"]}\n')
            time.sleep(2)  # Задержка между запросами для предотвращения блокировки
        debug_file.write('Playlist updated successfully.\n')

if __name__ == "__main__":
    update_playlist()
