python开发

运行程序前需要pip安装拓展库jieba和bs4

对苏州大学网页进行爬虫和倒排索引

由于网站总体内容太大，程序默认访问100个网页，使用时可在for循环中调整访问网页的数量，或者取消while循环的注释使代码访问全部网页。

默认设置间隔时间，防止被屏蔽，可以手动进行调整。

网站爬取完毕后程序会给出提示，此时可以输入查询内容，程序调用jieba库，计算结果。查询格式为以空格分隔的单词，结果格式为网页加相似度。





方案思路：首先想到要使用工具将网页爬取，使用Python自带的urllib库，通过request向网站发送请求获得源代码。接着选择BeautifulSoup库进行html源代码的解析，获得锚链接和正文。正文保存到磁盘，锚链接放入内存的队列等待之后的调用。tf-idf排序则改写之前已经完成的实验代码，通过jieba分词库进行分词。





获取源代码的代码如下：

```py
def get_html(url):
    req = urllib.request.Request(url=url, headers={'User-Agent': random.choice(user_agents)})
    link = urllib.request.urlopen(req, timeout=1)
    return link.read()
```

获取锚链接和正文的代码如下：

```python
def getSave(url):
    soup = BeautifulSoup(get_html(url), 'html.parser')  # 初始化BeautifulSoup库,并设置解析器
    # 提取超链接
    for a in soup.findAll('a', href=True):
        u = a.get("href")
        ……（省略）
    # 提取正文
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    soup.prettify()
    ……（省略）
```





遇到问题：苏大网站相互嵌套有很多重复，使得爬取速度很慢。

解决方法：在获得锚链接时就利用集合进行查重，之前未出现的网站放入队列。

遇到问题：许多网站的锚链接是相对路径，不能直接使用相对路径访问网页。

解决办法：寻找规律用正则表达式将部分相对路径改写为绝对路径。

遇到问题：在爬虫过程中被网站封禁。

解决方法：改变request的header模仿不同浏览器的请求，设置间隔时间