import math
import random
import time
import re
from queue import Queue
import urllib.request
import urllib.error
import jieba
from bs4 import BeautifulSoup

urlSet = set()
urlList = []
doc = 0
que = Queue()

user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
]
ipList = ["112.85.129.100:9999", "112.85.175.4:9999", "112.87.70.92:9999"]
# proxy_support = urllib.request.ProxyHandler({"http": random.choice(ipList)})
# opener = urllib.request.build_opener(proxy_support)
# urllib.request.install_opener(opener)

def get_html(url):
    req = urllib.request.Request(url=url, headers={'User-Agent': random.choice(user_agents)})
    link = urllib.request.urlopen(req, timeout=1)
    return link.read()

def getSave(url):
    soup = BeautifulSoup(get_html(url), 'html.parser')  # 初始化BeautifulSoup库,并设置解析器
    # 提取超链接
    for a in soup.findAll('a', href=True):
        u = a.get("href")
        if u and ('@suda.edu.cn' not in u) and ("javascript" not in u):
            if u[0:4] == "http" and "suda" not in u:
                break
            if u[0:4] != "http":
                if u[0] == '/':
                    u = re.findall("http.*edu.cn", url)[0]+u
                else:
                    site = re.findall("http.*/", url)[0]
                    if site[-2] == '/':
                        site = re.findall("http.*/", url+'/')[0]
                    u = site+u

            if u[-1] == '/':
                u = u[0:len(u)-1]
            if u not in urlSet:
                que.put(u)
                urlSet.add(u)

    # 提取正文
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    soup.prettify()
    content = re.sub("<[^>]*>", '', soup.prettify())
    content = re.sub("\s{2,}", "\n", content)
    with open("{}".format(doc), "w", encoding='utf-8') as f:
        f.write(content)

def search():
    query = input("网站爬取完毕，请输入查询：").split()  # 输入查询
    queryDict = {}  # 单词在查询中的出现次数
    for i in query:
        if i in queryDict:
            queryDict[i] += 1
        else:
            queryDict[i] = 1
    queryDf = {i: 0 for i in queryDict}  # 用来之后记录查询词的df值，默认不存在为0

    fenciDict = []  # 各个文档分词结果的单词计数
    for i in range(len(urlList)):
        with open("{}".format(i), "r", encoding='utf-8') as f:
            s = f.read()
            fenci = jieba.lcut_for_search(s)
            fenciSet = set(fenci)
            fenciDict.append({i: fenci.count(i) for i in fenciSet})
            # 与上面对query的处理类似
            for word in queryDf:
                if word in fenciDict[i]:
                    queryDf[word] += 1
                    # 若关键词在文档中出现，则df加1

    similarList = []
    for i in range(len(urlList)):
        sum_qd = 0.0  # 作分子
        sum_q2 = 0.0
        sum_d2 = 0.0  # sum_q2*sum_d2的平方根作分母
        for word in queryDict:
            w_query = 1.0 + math.log10(queryDict[word])  # word在query中的tf-idf权重
            w_doc = 0  # word在第i个文档中的tf-idf权重
            if word in fenciDict[i]:
                w_doc = (1.0 + math.log10(fenciDict[i][word])) * math.log10(10000.0 / queryDf[word])
            sum_qd += w_query * w_doc
            sum_q2 += w_query ** 2
            sum_d2 += w_doc ** 2
        similar = 0.0  # 余弦相似度
        len_q2d2 = math.sqrt(sum_q2 * sum_d2)
        if math.fabs(len_q2d2) > 1e-5:
            similar = sum_qd / len_q2d2
        similarList.append((i, similar))  # 文档编号和余弦相似度的元祖

    similarList.sort(key=lambda x: x[1], reverse=True)

    for i in range(min(10,len(similarList))):
        d = similarList[i][0]
        print(urlList[d], similarList[i][1])


if __name__ == "__main__":
    que.put("http://www.suda.edu.cn")
    #while not que.empty():
    for i in range(100):            #可以选择for控制循环次数进行测试
        url = que.get()
        urlList.append(url)

        #print(url)                     #打印出访问的网站
        flag = False
        for i in range(3):      # 超时超过三次即认为访问失败
            try:
                getSave(url)
                flag = True
                break
            except:
                pass
        if flag:
            doc += 1
        else:
            #print("false")         # 可体现出什么网站访问失败
            pass

        # 控制访问时间间隔，可调整
        time.sleep(0.2)
        if doc % 10 == 0:
            time.sleep(1.5)
    search()
