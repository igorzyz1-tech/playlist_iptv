import requests

OAUTH_TOKEN = 'y0_AgAAAAAKSG8jAAw1TwAAAAEMhPSJAABD0B3UlfdMiooGaWG0E1k1QDV-YQ'
FILE_PATH = 'disk:/playlist.m3u'

channels = {
    "Русский Роман": "https://ser2.meningilovam.uz/rus_roman_web/tracks-v1a1/mono.m3u8?remote=94.25.231.197&token=f5193c542e5176ac3dfb935f41e31f1c4d478c13-76c5f56f3f837de0b380d0d17d751125-1722731887-1722721087",
    "Золотая Колекция": "https://ser2.meningilovam.uz/mos-film_web/tracks-v1a1/mono.m3u8?remote=94.25.231.197&token=6f9955f7d0bfb3ee3312fe07a8a752766727fd96-2cc3bbe755fd854061fcf2e7a116a0b3-1722732243-1722721443",
    "Дом кино Премиум": "https://ser2.meningilovam.uz/dom-kino-premium_web/tracks-v1a1/mono.m3u8?remote=94.25.231.197&token=953c62321d60e6bde18d9652aa0ce75a525414b1-50a2110e0119283c5369c0eb533d6bb4-1722732509-1722721709"
}

def get_updated_links():
    return channels

def update_playlist(channels):
    content = "#EXTM3U\n"
    for name, link in channels.items():
        content += f"#EXTINF:-1, {name}\n"
        content += f"{link}\n"

    headers = {
        "Authorization": f"OAuth {OAUTH_TOKEN}",
        "Content-Type": "application/octet-stream"
    }

    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    params = {"path": FILE_PATH, "overwrite": "true"}
    upload_response = requests.get(upload_url, headers=headers, params=params)
    upload_link = upload_response.json().get("href")

    if upload_link:
        upload_response = requests.put(upload_link, data=content.encode('utf-8'))
        if upload_response.status_code == 201:
            print("Плейлист успешно обновлен")
        else:
            print("Ошибка при обновлении плейлиста", upload_response.text)
    else:
        print("Не удалось получить ссылку для загрузки")

if __name__ == "__main__":
    updated_channels = get_updated_links()
    update_playlist(updated_channels)
