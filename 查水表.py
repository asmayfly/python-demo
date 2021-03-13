import requests

url = "http://www.ajxxgk.jcy.gov.cn/getFileListByPage"

with open("./水表账单.csv", "w", encoding="utf-8") as f:
    f.write("法院名,正文标题,正文Url链接,日期\n")
    for index in range(1, 10):
        data = {"codeId": "", "page": index, "size": 15, "fileType": "重要案件信息", "channelWebPath": "",
                "channelLevels": ""}
        result = requests.post(url, data=data).json()['results']['hits']['hits']
        print(result)
        for item in result:
            title = item['title']
            channel = item['channel'][-2]['displayName']
            item_url = item['url']
            date = item['publishedTimeStr']
            line = f"{channel},{title},{item_url},{date}\n"
            f.write(line)
