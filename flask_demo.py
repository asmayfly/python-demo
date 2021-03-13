from flask import Flask,render_template,request,redirect,url_for,make_response,session,flash
import requests,json,time
from lxml import etree

app = Flask(__name__)
app.secret_key="\x088\xdb\x14\xc9p&\xb8\x06A\xdf\x12\x8am\xd3\xef"
users = {"admin":"123"}

@app.route("/")
def index():
    username = None
    if "username" in session:
        username = session["username"]
        print("找到用户名",username)
    else:
        print("未找到")
    if username:
        return  render_template("index.html",username=username)
    else:
        return redirect( url_for("login", next = "/" ) )

@app.route("/list")
def list():

    # 从数据库获取数据
    news = [{
        "id":101,
        "name":"开盘暴涨245%！揭秘中芯国际资本膨胀史"
    },{
        "id":102,
        "name":"中芯国际上市，是泥菩萨还是金菩萨？"
    },{
        "id":103,
        "name":"推特现史诗级漏洞，马斯克盖茨账号被盗"
    },{
        "id":104,
        "name":"互联网巨头围猎信用卡"
    },{
        "id":105,
        "name":"到三、四线开店！蔚来、特斯拉们打响地面战"
    }]
    return render_template("list.html", news=news)

@app.route("/detail/<id>")
def detail(id):
    # 根据id去数据库中查看 id所对应的新闻的详情
    return render_template("detail.html",id=id)

@app.route("/login", methods =["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        # 只要注册过的用户都可以登陆
        if username in users and users[username]==password:
            next = request.args.get("next",None)
            if next:
                res = redirect(next)
                session["username"] = username
                return res
            else:
                res = redirect("/")
                session["username"] = username
                return res
        elif not username or not password:
            flash("数据不完整")
        else:
            flash("账号密码不匹配")
        return redirect( url_for("login") )

@app.route("/logout")
def logout():
    res = redirect( url_for("index") )
    session.pop("username")
    return res

@app.route("/regist", methods=["GET", "POST"])
# 注册的账户数据做一个持久化记录
def regist():
    if request.method == "GET":
        return render_template("regist.html")
    elif request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        password2 = request.form.get("password2", None)
        print(username,password,password2)
        if not username or  not password or not password2:
            flash("数据不完整")
            return redirect( url_for("regist") )
        elif password2!=password:
            flash("密码不一致")
            return redirect(url_for("regist"))
        else:
            users[username] = password
            return redirect( url_for("login") )

@app.route("/spider")
def spider():
    # 网易新闻的
    response = requests.get("https://temp.163.com/special/00804KVA/cm_yaowen20200213.js?callback=data_callback")
    json_str = response.content.decode("gbk")
    py_dic_list = json.loads(json_str[14:-1])
    return render_template("spider.html", news=py_dic_list)

def send_requests(url,headers=None):
    retry_count = 0
    while retry_count < 5:
        try:
            return requests.get(url,headers=headers).content
        except Exception as e:
            print(e)
            retry_count += 1
            print(f"重新尝试次数：{retry_count}")
            time.sleep(2)
    else:
        print(f"请求{url}异常")
        return None


@app.route("/img")
def img():
    data_list = []
    headers = {
        "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
    }
    url = f"https://www.yeitu.com/tag/cosplay?page=1"
    # 一级界面
    index = send_requests(url,headers)
    if index:
        html_str = index.decode()
        root = etree.HTML(html_str)
        div_list = root.xpath('//div[@id="tag_box"]/div[@class="tag_list"]')
        for item in div_list:
            cover_img_url = item.xpath('.//img/@src')[0]
            title = item.xpath('./div[@class="title"]/a/text()')[0]
            first_html_href = item.xpath('./div[@class="title"]/a/@href')[0]
            data_list.append({"title":title,"first_html_href":first_html_href,"cover_img_url":cover_img_url})
    return render_template("img.html", data_list=data_list)

if __name__ == '__main__':
    app.run(debug=True)