import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def fetch_dynamic_url(channel_url, debug_file):
    try:
        # Настройка Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Запуск в фоновом режиме
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(channel_url)
        debug_file.write(f'Fetched main page for {channel_url}\n')
        time.sleep(5)  # Ждем загрузки страницы и выполнения скриптов

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Поиск ссылок, содержащих '.m3u8'
        for link in soup.find_all('a', href=True):
            debug_file.write(f'Checking link: {link["href"]}\n')
            if '.m3u8' in link['href']:
                debug_file.write(f'Found stream URL: {link["href"]}\n')
                driver.quit()
                return link['href']

        # Альтернативный поиск в тегах <iframe>
        iframe_tag = soup.find('iframe')
        if (iframe_tag and 'src' in iframe_tag.attrs):
            iframe_url = iframe_tag['src']
            if iframe_url.startswith('//'):
                iframe_url = 'https:' + iframe_url
            debug_file.write(f'Found iframe URL: {iframe_url}\n')

            driver.get(iframe_url)
            time.sleep(5)  # Ждем загрузки страницы и выполнения скриптов

            iframe_soup = BeautifulSoup(driver.page_source, 'html.parser')
            debug_file.write(f'Fetched iframe page for {iframe_url}\n')

            for link in iframe_soup.find_all('a', href=True):
                debug_file.write(f'Checking link in iframe: {link["href"]}\n')
                if '.m3u8' in link['href']:
                    debug_file.write(f'Found stream URL in iframe: {link["href"]}\n')
                    driver.quit()
                    return link['href']

        # Поиск в скриптах
        for script in soup.find_all('script'):
            script_content = script.string
            if script_content:
                debug_file.write(f'Checking script content\n')
                m3u8_urls = re.findall(r'https?://[^"]+\.m3u8', script_content)
                if m3u8_urls:
                    for url in m3u8_urls:
                        debug_file.write(f'Found stream URL in script: {url}\n')
                    driver.quit()
                    return m3u8_urls[0]

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
