import requests
from bs4 import BeautifulSoup
import time
import random
import csv
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin
##  添加可能需要的不同的库
##  类相当于汽车蓝图，实例相当于用这个蓝图造出一辆汽车
##  下面的头请求部分，一般在document类型请求里，点击他就可以看到了

class DoubanCrawler:   ## 定义一个类   ##主要更改部分，
    def __init__(self):
        self.base_url = 'https://movie.douban.com/top250' ## self代表类的实例，表示对base_url进行赋值   ## 目标地址，可根据需要，更换想要爬取的网站（需按网站不同修改）
        self.headers = {  ##该实例是一为了防止爬虫失败而建立的
            ## User-Agent是必须更换的，如何找到？打开想爬取的网站→按F12打开开发者工具→找到Network，找到任意请求，一般是第一个，，点击→在request headers中关键字段（需按网站不同修改）
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/115 SLBVPV/64-bit',
            'Referer': 'https://www.douban.com/', ##通常是需要的（要注意，直接使用链接打开的网站是不包含referer的，使用需要在上一页再次进入目标网站）查找方法同上（需按网站不同修改）
            'Accept-Language': 'zh-CN,zh;q=0.9'  ##同样按照User-Agent的方式寻找，即可找到（需按网站不同修改）
            ##当网站需要登录时，就得添加'cookie',查找方式同上（需按网站不同修改）
        }
        self.robot_parser = RobotFileParser()  ##创建一个实例，其中RobotFileParser是为了解析robots文件，并判断完整是否运行爬虫的
        self.movie_data = []  ## 建立一个空列表，用来存储电影数据  ##可以根据需要，修改名称
        self.check_robots_txt()  ##check_robots_txt同样是为了确定爬虫是否被允许访问目标页面

    def check_robots_txt(self):  ## 定义一个名为check_robots_txt的实例方法，其实self为参数名，可更改，但不建议这么做，因为self是约定俗成的  ##这个可以保留，是用来检查robots协议的，即是否让人爬取
        self.robot_parser.set_url(urljoin(self.base_url, '/robots.txt'))  ##其中，robot_parser是之前设定的RobotFileParser()实例，set_url是RobotFileParser()里的一个方法，设定要解析的robots.txt文件url;urljoin是为了把两个url组合成完整url，其中self.base_url为目标基础url，和/robots.txt组合起来，获取robots文件的完整url
        try:  ##用try捕获可能出现的异常
            self.robot_parser.read()  ##尝试读取robots文件
            if not self.robot_parser.can_fetch('*', self.base_url):  ##检查是否允许名为*（代表所有爬虫）的爬虫访问基础URL
                raise Exception("当前网站禁止爬取")  ##如果不行，就返回这个错误
        except Exception as e:  ## except用来捕获try块的异常，并把异常给予变量e
            print(f"Robots.txt检查失败: {e}")  ##打印错误
            exit()  ##终止程序运行

    def fetch_page(self, url):   ## 其中，self表示类的实例本身，可以通过它访问类的其他属性与方法，url表示该方法接收的一个参数，表示要请求的页面的url  ##也可以保留
        try:   ## 用try块捕获异常
            time.sleep(random.uniform(1.5, 3.5))  ## 随机生成一个介于1.5到3.5间的浮点数，time.sleep会暂停执行该随机时长，模拟人类浏览行为
            response = requests.get(url, headers=self.headers, timeout=15)  ##requests.get是发送http get请求的方法，headers=self.headers用这里面的属性作为请求头，模拟服务器请求，timeout为设置请求的超时时间为15秒
            response.raise_for_status()  ##一个方法，用于检查状态码是否正常，如果不是200，则抛出异常

            # 验证是否返回正常页面
            if 'text/html' not in response.headers.get('Content-Type', '') or '检测到有异常请求' in response.text:
                print("触发反爬机制，请更新请求头或使用代理")
                return None

            return response.text  ##返回响应内容
        except Exception as e:
            print(f"请求失败: {url} - {str(e)}")
            return None

    def parse_page(self, html):  ##主要修改的类
        soup = BeautifulSoup(html, 'lxml')  ##使用 BeautifulSoup 库来解析传入的HTML代码
        movie_list = soup.find_all('div', class_='item') ##打开目标网站，使用Ctrl+Shift+C，找到你想要爬取的内容的位置，以这个网站为例，打开元素选择工具，移向电影的地方，观察最外层盒子的名字，在这里，每一个电影的最外层盒子名字相同，所以用find.all

        for item in movie_list: ##遍历item，即获取每一个盒子里的不同的消息，或者可根据需要，只遍历直接需要的部分（需按网站不同修改）
            try:
                # 电影标题（强化容错处理）首先，获取盒子里的不同的标题，寻找方式同上，其中最前面的例如title_elem为变量名，可随意更改（需按网站不同修改）
                title_elem = item.find('span', class_='title')
                title = title_elem.text.strip() if title_elem else "未知标题"   ## 表示如果找到，则提取其文本内容，并去除首尾空白字符，否则设置为未知标题 ##添加万一没有标题时，报的信息，即容错
                other_title = item.find('span', class_='other').text.strip() if item.find('span',class_='other') else ""  ## 同理，找到这个盒子，并通过text.strip()来提取文本，否则输出空字符

                # 评分信息（新版定位方式）其次，寻找盒子里的评分系统（需按网站不同修改）
                rating_tag = item.find('span', class_='rating_num')    ##同上
                rating = rating_tag.text.strip() if rating_tag else "无评分" ##同上 ##同理，增加容错

                # 评价人数（精确匹配）原理同上（需按网站不同修改）
                rating_count_tag = item.find('span', string=lambda t: t and t.endswith('人评价'))  ##前面同理，到了string=lambda t: t and t.endswith('人评价')，其中，lambda为匿名函数，通常用来定义简单函数，t: t and t.endswith('人评价')，第一个t，首先检查文本内容t是否为真值（不为空和none和0即为真值），如果t为真，后面的为调用endswith方法，检查t是否以“人评价结尾”
                rating_count = rating_count_tag.text.strip() if rating_count_tag else "0人评价"

                # 导演与演员信息（稳健解析）原理同上（需按网站不同修改）
                info = item.find('div', class_='bd').p.get_text(" ", strip=True).split('\n')  ##在当前电影信息容器中找到 class 属性为 bd 的 div 元素，再找到其中的 p 元素，提取其文本内容，使用空格连接并去除首尾空白字符，然后按换行符 \n 分割成列表 info。
                director = info[0].replace("导演:", "").strip() if len(info) > 0 else ""  ##从info列表提取第一个元素（即导演信息），去除“导演”字样，并去掉首尾空白符，如果列表为空，则设置为“”
                actors = info[1].replace("主演:", "").strip() if len(info) > 1 else ""  ## 从info列表提取第二个元素，其它同理

                ##（需按网站不同修改）## 把得到的整理成一个字典，并放到这个列表中
                self.movie_data.append({
                    'title': f"{title} {other_title}".strip(),  ##这个f"{}{}"即是把两个内容串连起来，连成一整句话，后面.strip()为去掉多余的空白
                    'rating': rating,
                    'rating_count': rating_count,
                    'director': director,
                    'actors': actors
                })

            except Exception as e:  ##异常处理
                print(f"解析电影条目时出错: {str(e)}")
                continue    ##跳过异常部分

    def save_to_csv(self):
        with open('Crawler-Result-2.csv', 'w', newline='', encoding='utf-8-sig') as f:   ##使用open函数，打开一个名为Crawler-Result-2.csv的文件，“w”表示写入模式打开文件，如何文件不存在就创建它，如果存在则清空原有内容；newline=''：是为了避免写入csv文件时，出现多余的空行；encoding='utf-8-sig'：指定文件的编码格式为 UTF-8 ; with是为了确保文件使用完后能被正确关闭
            writer = csv.DictWriter(f, fieldnames=['title', 'rating', 'rating_count', 'director', 'actors'])  ##csv.DictWriter用于将字典形式数据写入csv文件;f为前面打开的文件对象，代表要写入数据的文件;fieldnames=['title', 'rating', 'rating_count', 'director', 'actors']：指定 CSV 文件的列名
            writer.writeheader()  ##将 fieldnames 列表中的列名写入 CSV 文件的第一行，作为表头。
            writer.writerows(self.movie_data)  ##将 self.movie_data 列表中的每个字典写入 CSV 文件，每个字典代表一行数据。字典中的键必须与 fieldnames 中的列名相对应，这样数据才能正确地写入对应的列。
        print("数据已保存至 Crawler-Result-2.csv")

    def run(self):
        for page in range(0, 250, 25):   ##从0开始到250结束，步长为25的整数序列即，0，25，50.。。。（这是因为该页面中，每一页有25条电影记录）（需按网站不同修改）
            url = f"{self.base_url}?start={page}"  ##将网站基础url和start=page联系起来，即当page为0时，显示： https://movie.douban.com/top250?start=0
            print(f"正在爬取: {url}")

            html = self.fetch_page(url)   ##调用前面fetch_page方法，传入当前页面的url
            if html:     ##如何html不为none，说明页面内容获取成功，并把html的内容，通过调用方法parse_page,把电影信息写入列表，否则跳过该页面，停止后续页面的爬取
                self.parse_page(html)
            else:
                print(f"跳过无效页面: {url}")
                break  # 遇到反爬时停止

        self.save_to_csv()   ##爬取完成后，将数据存储到csv内容中


if __name__ == '__main__':
    crawler = DoubanCrawler() ##调用前面定义完成的类（即蓝图，里面的不同的def为功能）
    crawler.run()
    print("爬取完成！")