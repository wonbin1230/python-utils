import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from tqdm.auto import tqdm

def get_memes_images(pages):
    for i in range(pages):
        try:
            url = "https://memes.tw/all-images" if i <= 0 else f"https://memes.tw/all-images?page={i + 1}"
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("log-level=3")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

            driver = webdriver.Chrome(options=options)
            print("等待網頁載入完成...")
            driver.get(url)
            html = driver.page_source
            driver.close()

            soup = bs(html, "html.parser")
            images = soup.find("div", class_="flexbin flexbin-margin mt-2").find_all("div", class_=None)

            print(f"------------------------------開始下載第{i + 1}頁梗圖倉庫梗圖----------------------------------")
            os.makedirs("memes", exist_ok=True)
            for j in tqdm(range(len(images))):
                try:
                    image_url = images[j].find("img")["data-src"]
                    file_name = f"{images[j].find('b').get_text()}.{image_url.split('.')[-1]}"
                    if os.path.isfile(f"memes/{file_name}") == True:
                        continue
                    else:
                        res = requests.get(image_url)
                        image = res.content
                        with open(f"memes/{file_name}", "wb") as f:
                            f.write(image)
                except Exception as e:
                    print(e)
                    pass
            print(f"------------------------------完成下載第{i + 1}頁梗圖倉庫梗圖-----------------------------------")
        except Exception as e:
            print(f"下載第{i + 1}頁時發生錯誤並跳過此頁，錯誤為{e}")
            pass
    print("已完成所有梗圖下載")

custom_pages = 0
while custom_pages <= 0:
    try:
        custom_pages = int(input("請輸入欲下載頁數(若要直接結束請按Ctrl + C)："))
        if custom_pages <= 0:
            print("請輸入大於0的數字")
    except ValueError as e:
        print(f"輸入格式錯誤：{e}")
get_memes_images(custom_pages)