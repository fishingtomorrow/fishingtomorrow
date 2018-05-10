import requests,json,re,sys, io, os
from bs4 import BeautifulSoup

def get_chkinfo(product_id):
    url = "http://bang.360.cn/liangpin/aj_get_quality_check?product_id=" + product_id + "&callback=0"
    res = requests.get(url)
    res1 = res.text[3:len(res.text)-1]
    js = json.loads(res1)
    chkinfo = {"地址":"http://bang.360.cn/liangpin/product?product_id=" + product_id}
    chkinfo["标题"], chkinfo["价格"] = get_dev_info(product_id)
    for item in js["result"]["basic"]:
        chkinfo[item["option_name"]] = item["option_sub"]
    for item in js["result"]["exterior"]:
        chkinfo[item["option_name"]] = item["option_sub"]
    chkinfo["报告"] = js["result"]["str"]
    return chkinfo

def get_dev_info(product_id):
    url = "http://bang.360.cn/liangpin/product?product_id=" + product_id
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    price = soup.select(".m-money-num")
    h1s = soup.select("h1")
    return h1s[0].text, price[0].text

def get_device_list(dev_type):
    devlist = []
    i = 0
    while True:
        url = "http://bang.360.cn/liangpin/search?brand_id=2&chengse=1604&model_id=" + dev_type + "&pn=" + str(i)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select("a")
        aplinks = [link for link in links if "product_id" in link["href"]]
        for aplink in aplinks:
            devlist.append(re.search("(?<=\=)\d.*", aplink["href"]).group(0))
        if len(aplinks) == 0:
            break
        i = i + 1
    return devlist


def get_info_list():
    devlist = get_device_list(sys.argv[1])
    infolist = []
    for dev in devlist:
        infolist.append(get_chkinfo(dev))
    return sorted(infolist, key=lambda price:int(price["价格"]))

#__main__

try:
    os.remove(sys.argv[1] + ".txt")
except:
    pass

infolist = get_info_list()
for info in infolist:
    mode = re.search("A.{0,4}", info["报告"]).group(0)
    times = re.search("(^\d+)|(^\-\d*)", info.get("循环充电次数","-1次")).group(0)
    pinm = info["屏幕"]
    cover = info["后盖"]
    edge = info["边框"]
    report = info["报告"]
    addr = info["地址"]
    title = info["标题"]
    price = info["价格"]
    fd = open(sys.argv[1] + ".txt", "a", encoding='utf-8')
    lines = []
    if int(times) != -1 and int(times) <= 500:
        lines.append(mode+"   "+str(price)+" "+times+" "+pinm+"  "+cover+" "+edge+"\n")
        lines.append(title+"\n")
        lines.append(report+"\n")
        lines.append(addr + "\n\n")
        fd.writelines(lines)
        print(lines)
    fd.close()
