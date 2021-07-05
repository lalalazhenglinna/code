import csv,requests,math,json,re,os,time,datetime
from lxml import etree


class Mycsv:
    def __init__(self, file_name):
        self.file_exist = 0
        
        if file_name == '':
            file_name = '新建文件.csv'
        else:
            file_name = file_name

        self.file_name = file_name
        
        try:
            with open(file_name, 'x') as outfile:
                print(file_name, '文件创建成功')

        except FileExistsError:
            self.file_exist = 1
            print(file_name, '文件已存在')
            

        except OSError:
            print(file_name, '文件创建失败')

    def save(self,rowdata):
        with open(self.file_name,'a+',newline='',encoding='utf-8-sig')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(rowdata)

            
class Req():
    @staticmethod
    def get(url,headers):
        count_requests = 10
        while count_requests > 0:
            try:
                res = requests.get(url=url,headers=headers)
                if res.status_code == 200:
                    break
            except:
               time.sleep(1)
            count_requests = count_requests - 1
            print ('请求失败，正在重新连接')
            time.sleep(10)
        if res:
            return res
        else:
            print ('请求失败，请检查网络连接')

req = Req()

cookie = '''
bid=8FK0b3F9RW4; douban-fav-remind=1; ll="118183"; _vwo_uuid_v2=D12B08A908C11EA166485F1E1BFC844BE|c35ab225d862ca04e3885728b4e357eb; push_doumail_num=0; push_noty_num=0; __utmv=30149280.24076; ct=y; _ga=GA1.2.470713175.1600161891; dbcl2="240765286:Pj3p39ZcKpg"; __gads=ID=5e094adbd11c6759:T=1625020413:R:S=ALNI_MYQ8VBb3lr-XjpaxbNtbimLrg4Zng; __utmz=30149280.1625110553.22.16.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1625110553.15.10.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ck=PmUF; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1625116106%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DM8_RrLPliezL27zvIs7dUVvgiV03CoCr7iIukbEQW60deqKBbPEQKtbSoKKna7-L%26wd%3D%26eqid%3Da1d7739200007f430000000660dd3814%22%5D; _pk_id.100001.4cf6=80ca9f2a721040f5.1624762757.19.1625116106.1625110553.; _pk_ses.100001.4cf6=*; __utma=30149280.470713175.1600161891.1625110553.1625116106.23; __utmb=30149280.0.10.1625116106; __utmc=30149280; __utma=223695111.1124146416.1624849558.1625110553.1625116106.16; __utmb=223695111.0.10.1625116106; __utmc=223695111; ap_v=0,6.0

'''

    
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
##'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Cookie':cookie.strip(),
'Host': 'movie.douban.com',
##'Referer': 'https://movie.douban.com/subject/30206311/reviews?start=0',
'Upgrade-Insecure-Requests': '1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}


f_csv = Mycsv('pl.csv')
if f_csv.file_exist == 0:
    f_csv.save(['name','rating','title','ftime','h2','link','tips','shortContent','useful','useless'])


with open('movie_urls','r',encoding='utf8') as f:
    aa = f.readlines()
task = [a.strip().replace('https://movie.douban.com/subject/','').replace('\t','').split('/') for a in aa]

try:
    with open('mark.txt','r') as f:
        ii = json.loads(f.read())
    page = ii['p_index']
    t_index= ii['t_index']
except:
    page = 1
    t_index = 0



for t in task[t_index:]:
    print (t)
    page = 1
    with open('mark.txt','w') as f:
        f.write(json.dumps({'t_index':task.index(t),'p_index':1}))
        
    while True:
        url ="https://movie.douban.com/subject/{0}/reviews?start={1}".format(t[0],str((page-1)*20))
        # print (url)
        res = requests.get(url = url, headers = headers)
        # res.encoding='utf8'
        if res.status_code == 200:   # 网页请求成功
            tree = etree.HTML(res.text)
        else:
            break
        
        clist = tree.xpath('//div[@class="main review-item"]')
        if len(clist) > 0:
            for c in clist:
                name = "".join(c.xpath('.//a[@class="name"]/text()'))
                rating = "".join(c.xpath('.//header/span[1]/@class'))
                title = "".join(c.xpath('.//header/span[1]/@title'))
                ftime = "".join(c.xpath('.//header/span[2]/text()'))
                h2 = "".join(c.xpath('.//div[@class="main-bd"]/h2/a/text()'))
                link = "".join(c.xpath('.//div[@class="main-bd"]/h2/a/@href'))
                tips = "".join(c.xpath('.//div[@class="short-content"]/p/text()'))
                shortContent = "".join(c.xpath('.//div[@class="short-content"]/text()')).replace('\xa0()','').strip()
                useful = "".join(c.xpath('.//span[contains(@id,"r-useful_count")]/text()')).strip()
                useless = "".join(c.xpath('.//span[contains(@id,"r-useless_coun")]/text()')).strip()
                rowdata =[t[0],t[1],name,rating,title,ftime,h2,link,tips,shortContent,useful,useless]
                print(task.index(t),rowdata)
                f_csv.save(rowdata)
        else:
            break

        page = page + 1
        with open('mark.txt','w') as f:
            f.write(json.dumps({'t_index':task.index(t),'p_index':page}))
        time.sleep(5)

            
            





