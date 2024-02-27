import os
import requests
import re
from bs4 import BeautifulSoup as bs
from tqdm.auto import tqdm
from mongo import MongoDB

class Memes():
    def __init__(self):
        self.url = "https://memes.tw/maker"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }

    def main(self):
        page_total = self.__page_getter()
        need_pages = 0
        while need_pages <= 0:
            try:
                need_pages = int(input(f"請輸入欲下載頁數1-{page_total}(若要直接結束請按Ctrl + C)："))
                if need_pages <= 0:
                    print("請輸入大於0的數字")
            except ValueError as e:
                print(f"輸入格式錯誤：{e}")
        download_list = self.__images_downloader(need_pages)
        return download_list

    def __page_getter(self):
        try:
            maker_page = requests.get(self.url, headers=self.headers)
            page_content = bs(maker_page.content, "html.parser")
            return page_content.find_all("li", class_="page-item")[-2].get_text()
        except Exception as e:
            print(f"page_getter error: {e}")

    def __images_downloader(self, pages=1):
        try:
            print("開始下載梗圖模板")
            memes_list = []
            download_count = 0
            for i in range(pages):
                print(f"----------------------------第{i + 1}頁開始----------------------------")
                url = "https://memes.tw/maker" if i <= 0 else f"https://memes.tw/maker?page={i + 1}"
                maker_page = requests.get(url, headers=self.headers)
                page_content = bs(maker_page.content, "html.parser")
                items = page_content.find_all("div", class_="-shadow mt-3 mx-2 relative")

                os.makedirs("E:/mount/memes", exist_ok=True)
                for j in tqdm(range(len(items))):
                    image_name = re.sub('\\W+', '', items[j].find('header').find('b').get_text())
                    image_full_path = f"E:/mount/memes/{image_name}.png"
                    image_url = f"https://memeprod.ap-south-1.linodeobjects.com/user-template/{items[j].find("img")["src"].split("/")[-1].replace(".jpg", ".png")}"
                    if os.path.isfile(image_full_path) or self.__filter_is_exsist(image_name):
                        continue
                    download_res = requests.get(image_url)
                    with open(image_full_path, "wb") as f:
                        f.write(download_res.content)
                    memes_list.append({
                        "name": image_name,
                        "uri": image_full_path
                    })
                    download_count += 1
                print(f"----------------------------第{i + 1}頁結束----------------------------")
            print(f"梗圖模板下載完成，共計下載 {download_count} 個模板")
            return memes_list
        except Exception as e:
            print(f"images_downloader error: {e}")

    def __filter_is_exsist(self, image_name):
        try:
            conditions = {
                "name": image_name
            }
            client = MongoDB()
            result = len(list(client.model.find(conditions)))
            return True if result > 0 else False
        except Exception as e:
            print(f"filter_exsist error: {e}")
