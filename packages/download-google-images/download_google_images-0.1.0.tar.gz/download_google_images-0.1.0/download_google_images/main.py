from selenium import webdriver
import typer
import requests
import time
import io
import os
from PIL import Image
from selenium.webdriver.chrome.options import Options
import sys
import argparse

import hashlib
from selenium.webdriver.common.keys import Keys


options = Options()
options.add_argument("--headless")
# options.add_argument("--window-size=1920x1080")

wd = webdriver.Chrome('./chromedriver.exe',options=options)
# wd.get('https://google.com')
#
# search_box = wd.find_element_by_css_selector('input.gLFyf')
# search_box.send_keys('Dogs')
# print(wd.title)

app = typer.Typer()
def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    def scroll_to_end(wd):
        # to scroll down the page till last element
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

        # build the google query

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd") #this has to be replaced
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)
            print(image_count)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
            else:
                print("Found:", len(image_urls), "image links, looking for more ...")
            if len(image_urls) >= 200:
                print('in 200')
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")

                    # move the result startpoint further down
                    results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')



        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


@app.command()
def search_and_download(keyword: str =typer.Option(...) , chromedriver : str=typer.Option(...), target_path:str=typer.Option('./images'), number_images:int=typer.Option(5)):
    target_folder = os.path.join(target_path, '_'.join(keyword.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    t0 = time.time()
    try:
        with webdriver.Chrome(executable_path=chromedriver,options=options) as wd:
            res = fetch_image_urls(keyword, number_images, wd=wd, sleep_between_interactions=0.5)
    except Exception as e:
        print("Looks like we cannot locate the path the 'chromedriver' (use the '--chromedriver' "
              "argument to specify the path to the executable.) or google chrome browser is not "
              "installed on your machine (exception: %s)" % e)
        sys.exit()

    for elem in res:
        persist_image(target_folder, elem)
    t1 = time.time()
    total_time = t1 - t0
    print("Total time taken: " + str(total_time) + " Seconds")



# if __name__ == "__main__":

#     # search_and_download('pokemon','./chromedriver.exe',number_images=250)
#     app()
