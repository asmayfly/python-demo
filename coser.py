import requests
import os
from lxml import etree
from fake_useragent import UserAgent

# 创建文件夹
os.makedirs("./cos美图", exist_ok=True)
# 随机UA
userAgent = UserAgent()
headers = {
    "User-Agent": userAgent.random,
}
# 爬取1-10页
for page in range(1, 10):
    url = f"https://www.yeitu.com/tag/cosplay/?&page={page}"
    page_first = etree.HTML(requests.get(url, headers=headers).content)
    # 页面所有小美女
    list_first = page_first.xpath("//div[@class='tag_list']")
    # 获取每页小美女的标题和URL
    for item in list_first:
        # 标题
        title = item.xpath(".//div[@class='title']/a/text()")[0]
        # 根据标题创建文件夹
        os.makedirs(f"./cos美图/{title}", exist_ok=True)
        # URL
        page_second_url = item.xpath("./a/@href")[0]
        page_second = etree.HTML(requests.get(page_second_url, headers=headers).content)
        # 获取图片数量
        img_page_count = int(page_second.xpath("//div[@id='pages']/a/text()")[-2])
        # 进入每个图片页面获取图片地址
        for img_page_index in range(1, img_page_count):
            if img_page_index == 1:
                img_page = page_second_url
            else:
                page_second_url_list = list(page_second_url)
                page_second_url_list.insert(-5, f"_{img_page_index}")
                img_page = ''.join(page_second_url_list)
            img = etree.HTML(requests.get(img_page, headers=headers).content)
            # 图片URL
            img_url = img.xpath("//div[@class='img_box']/a/img/@src")[0]
            with open(f"./cos美图/{title}/{img_page_index}.jpg", "wb") as f:
                print(img_url)
                headers = {
                    "referer": img_page,
                    "User-Agent": userAgent.random,
                }
                img_bytes = requests.get(img_url, headers=headers).content
                f.write(img_bytes)
