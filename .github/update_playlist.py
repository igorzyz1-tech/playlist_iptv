import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def fetch_dynamic_url(channel_url, debug_file):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(channel_url)
        debug_file.write(f'Fetched main page for {channel_url}\n')
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        player_div = soup.find('div', class_='page__player video-inside')
        if player_div:
            video_tag = player_div.find('video')
            if video_tag:
                source_tag = video_tag.find('source', src=True)
                if source_tag and '.m3u8' in source_tag['src']:
                    stream_url = source_tag['src']
                    debug_file.write(f'Found stream URL: {stream_url}\n')
                    driver.quit()
                    return stream_url

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
    
    with open('playlist.m3u', 'w') as file:
        file.write('#EXTM3U\n')
        for channel in channels:
            file.write(f'Fetching dynamic URL for {channel["name"]}\n')
            dynamic_url = fetch_dynamic_url(channel["url"], file)
            if dynamic_url:
                file.write(f'#EXTINF:-1 tvg-name="{channel["name"]}",{channel["name"]}\n{dynamic_url}\n')
            else:
                file.write(f'Failed to fetch dynamic URL for {channel["name"]}\n')
        file.write('Playlist updated successfully.\n')

if __name__ == "__main__":
    update_playlist()
