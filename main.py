import requests
import json
from colorama import Fore, Style
import art
from console import utils
print(f'{Fore.LIGHTRED_EX}')
art.tprint('CAPTCHA')
print(f'{Fore.LIGHTCYAN_EX}By @TURAN_KMT{Style.RESET_ALL}')

def get_csrf():
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
        'X-Requested-With': 'XMLHttpRequest', 
        'Referer': 'https://eu.wargaming.net/id/signin/',
    }
    
    response = requests.get('https://eu.wargaming.net/id/state.json', headers=headers)
    return response.json()['Request']['CSRF_TOKEN']

pon = 0 
work = True 

while work:
    csrf_token = get_csrf()
    url = "https://eu.wargaming.net/id/signin/challenge/?type=captcha"
    
    headers = { 
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Language": "ru",
        "Referer": "https://eu.wargaming.net/id/signin/",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    }

    cookies = { 
        "wgni_language": "ru",
        "wgni_csrftoken": csrf_token,
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    wgni_sessionid = response.cookies.get('wgni_sessionid')
    json_response = response.json()
    token = json_response.get("captcha", {}).get("token")

    print(f'{Fore.LIGHTGREEN_EX}Captcha URL: {Fore.LIGHTBLUE_EX}https://eu.wargaming.net/id/captcha/{token}{Style.RESET_ALL}') 

    captcha_response = requests.get(f"https://eu.wargaming.net/id/captcha/{token}")
    
    if captcha_response.status_code == 200:
        with open('page.png', 'wb') as file:
            file.write(captcha_response.content)
            print(f'{Fore.LIGHTCYAN_EX} Captcha успешно сохранена в файл!{Style.RESET_ALL}') 
            pon += 1
            utils.set_title(f'Всего создано капч: {pon}. Soft by @TURAN_KMT')
            input(f'{Fore.LIGHTMAGENTA_EX}Нажмите Enter, чтобы заново генерировать капчу{Style.RESET_ALL}')
