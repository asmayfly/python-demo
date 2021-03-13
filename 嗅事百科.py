import requests
from lxml import etree

# 声明csv文件对象 进行数据存储
f = open("./嗅事百科.csv", "w", encoding="utf-8")
f.write("标题,url,点赞数,评论数,发帖人\n")
for p in range(1, 2):
    # 正常的requests请求
    url = f"https://www.qiushibaike.com/8hr/page/{p}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
    }
    root = etree.HTML(requests.get(url, headers=headers).content)
    # 找到所有的包含岗位信息的div列表
    div_list = root.xpath('//div[@class="recmd-right"]')
    # 遍历 按行处理每一条信息
    for div in div_list:
        title = div.xpath('.//a/text()')[0]
        data_url = "https://www.qiushibaike.com" + div.xpath("./a[@class='recmd-content']/@href")[0]
        recmd_num = div.xpath(".//div[@class='recmd-num']/span/text()")
        like_num = recmd_num[0]
        if len(recmd_num) == 2:
            commit_num = 0
        else:
            commit_num = recmd_num[3]
        author = div.xpath(".//a[@class='recmd-user']/img/@alt")[0]
        print(f"{title},{data_url},{like_num},{commit_num},{author}")
        f.write(f"{title},{data_url},{like_num},{commit_num},{author}\n")
f.close()
