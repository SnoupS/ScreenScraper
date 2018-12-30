from multiprocessing import Pool
from bs4 import BeautifulSoup
from random import choice
import requests
import time
import os


def downloaded_image(link):
    headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    html = requests.get(link, headers=headers)
    soup = BeautifulSoup(html.text, features="html.parser")
    image = soup.find('img', {'class': 'no-click screenshot-image'}).get('src')
    downloaded_images = 0

    if image.startswith('//st.') == False:
        downloaded_images += 1
        with open(f'images/{link[-6:]}.png', 'wb') as f:
            f.write(requests.get(image).content)
    return downloaded_images

def generation_link(links_amount):
    chars = 'qwertyuiopasdfghjklzxcvbnm'
    digits = '123456789'
    links = ['https://prnt.sc/' + ''.join(choice(chars + digits) for symbol in range(6)) for i in range(amount)]
    return links


if __name__ == '__main__':
    images_amount = int(input('\n\tEnter the number of images: '))
    print('\tDownloading...')
    start_time = time.time()
    os.makedirs('images', exist_ok=True)
    pool = Pool()
    downloaded_images_list = pool.map(downloaded_image, generation_link(images_amount))
    downloaded_images = sum(downloaded_images_list)
    download_errors = images_amount - downloaded_images
    pool.close()
    pool.join()
    os.system('clear')
    print(f'''\n
    Downloaded: {downloaded_images}
    Error:\t{download_errors}

    Runtime:\t{int(time.time() - start_time)} seconds.''')
    input('')
