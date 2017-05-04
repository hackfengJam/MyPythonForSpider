# -*- coding:utf-8 -*-
import os
import sys
import time
import threading
import requests
from lxml import etree
import urllib

reload(sys)
sys.setdefaultencoding('utf-8')

global flag
flag = 1


tag_list = ["热歌","新歌"]

# 写dict
def writedict(dict):
    with open('dict.txt','w') as f:
        f.write(str(dict))
# 读dict
def readdict():
    if not os.path.exists('dict.txt'):
        return {}
    with open('dict.txt','r') as f:
        dict = f.readline()
    return eval(dict)

# 去除文件名非法字符
def del_illegal_char(str):
    illegal_char = ["\\", "/", ":", "*", "?", '"', "'", "<", ">", "|"]
    for i in illegal_char:
        str = str.replace(i,"")
    return str

#去除空格 换行 制表符
def trim(str):
    return str.replace('\t', '').replace('\n', '').replace(' ', '')

#判断是否是404页面
def is_404(html):
    soup = etree.HTML(html)
    div = soup.xpath('//div[@class="state-404 c9"]')
    if div:
        return True
    return False

def urlcode_tr(str):
    return urllib.unquote(str).decode('utf-8')

def create_dir(name):
    if not os.path.exists(name):
        os.mkdir(name)
        print u'创建文件夹{}成功'.format(name)
        time.sleep(5)
    return name
def write_content_file(path_and_name,content,op='wb'):
    if not content:
        print u'写入的{}文件为空，请确认文件内容.....'.format(path_and_name)
        return
    with open(path_and_name,op) as f:
        f.write(content)

def write_text_file(path_and_name,text,op='a+'):
    global flag
    # print flag
    if not text:
        #print u'写入的{}文件为空，请确认文件内容.....'.format(path_and_name)
        return
    if os.path.exists(path_and_name) and flag==1:
        flag = 0
        os.remove(path_and_name)
    with open(path_and_name,op) as f:
        f.write(str(text))

def get_html(url):
    '''
    headers = {"Host":"music.baidu.com",
        "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    "Cookie":"__cfduid=d535414b37ab0e1f5e1a454ee1ac9283b1491409826; BAIDUID=B50E57EBDC27E3EA584EAB69D3C0569B:FG=1; BIDUPSID=99F61AC7C2C1D1C488471259D1FAA7B4; PSTM=1492784961; BDUSS=d4blV4azVNRjJ5aFlLZzNMTmtFR3Y4MVF1ZzJWSnVFYVUydEFnZXhVNVNpU3RaSVFBQUFBJCQAAAAAAAAAAAEAAACnjSlYyOXRxbXEssvE8c~It8kAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFL8A1lS~ANZUl; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[mlS6V4LF-w_]=mbxnW11j9Dfmh7GuZR8mvqV; PSINO=1; H_PS_PSSID=1451_21124; Hm_lvt_d0ad46e4afeacf34cd12de4c9b553aa6=1493603710,1493710963,1493729853,1493769596; Hm_lpvt_d0ad46e4afeacf34cd12de4c9b553aa6="+str(time.time()).split('.')[0]+"; checkStatus=true; tracesrc=-1%7C%7C-1; u_lo=0; u_id=; u_t="
               }
    '''
    headers = {"Host":"music.baidu.com",
        "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    "Cookie":"__cfduid=d535414b37ab0e1f5e1a454ee1ac9283b1491409826; BAIDUID=B50E57EBDC27E3EA584EAB69D3C0569B:FG=1; BIDUPSID=99F61AC7C2C1D1C488471259D1FAA7B4; PSTM=1492784961; BDUSS=d4blV4azVNRjJ5aFlLZzNMTmtFR3Y4MVF1ZzJWSnVFYVUydEFnZXhVNVNpU3RaSVFBQUFBJCQAAAAAAAAAAAEAAACnjSlYyOXRxbXEssvE8c~It8kAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFL8A1lS~ANZUl; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; checkStatus=true; BDRCVFR[mlS6V4LF-w_]=8Za7a4opMO6pydEUvn8mvqV; PSINO=1; H_PS_PSSID=1451_21124; Hm_lvt_d0ad46e4afeacf34cd12de4c9b553aa6=1493603710,1493710963,1493729853,1493769596; Hm_lpvt_d0ad46e4afeacf34cd12de4c9b553aa6=1493813422; tracesrc=-1%7C%7C-1; u_lo=0; u_id=; u_t="
               }
    request = requests.get(url=url,headers=headers)
    response = request.content
    # print response
    return response

#获得所有标签对应的url,以及分类
def get_tag_url_list(html):
    # html = re.search(r'<div class="mod-tag clearfix">(.*?)</div>',html,re.S).group(1)
    # print html
    soup = etree.HTML(html)
    dl = soup.xpath('//div[@class="tag-main"]/div/dl')
    # div = soup.xpath('//div[normalize-space(@class)="mod-tag clearfix"]/text()')
    tag_url_list = {}  #所有标签

    clazz = []  #所有分类
    for d in dl:
        title = d.xpath('dt/text()')
        # print title[0]
        items = d.xpath('dd/span/a/text()')
        url_list = d.xpath('dd/span/a/@href')
        items_url_list = {}
        m = 0
        for i in items:

            # print i
            items_url_list[i] = url_list[m]
            m+=1
        clazz.append(urlcode_tr(title[0]))
        tag_url_list[urlcode_tr(title[0])] = items_url_list
    return tag_url_list,clazz

#获取该标签的总音乐数
def get_music_totalpage(musiclist_html):
    soup = etree.HTML(musiclist_html)
    # span = soup.xpath('//div[@class="main-body-cont"]/div[@class="target-tag"]/span[@class="total"]/span/text()')
    # total = span[0]
    totalpage = soup.xpath('//div[@class="page-cont"]/div[@class="page-inner"]/a/text()')
    if not totalpage:
        totalpage = 1
        return int(totalpage)
    else:
        return int(totalpage[-2])

#获取音乐url
def get_music_url(musiclist_html):
    soup = etree.HTML(musiclist_html)
    li = soup.xpath('//div[@class="main-body-cont"]/div[@class="tag-main"]/div[@data-listdata]/ul/li')
    music_url_list = []
    for l in li:
        href = l.xpath('div/span[@class="song-title"]/a[1]/@href')
        music_url_list.append(href)
    return music_url_list

#获取音乐信息
def save_one_music_information(music_html,tag_dir,filename):
    soup = etree.HTML(music_html)
    li = []
    title = []
    songname = soup.xpath('//div[@class="mod-song-info"]/div[@class="song-info"]/div[@class="play-holder clearfix"]/div/h2/span[@class="name"]/text()') #歌曲名
    li.append(soup.xpath('//div[@class="mod-song-info"]/div[@class="song-info"]//ul[@class="base-info c6"]/li[not(@class)]'))  # 歌手
    li.append(soup.xpath('//div[@class="mod-song-info"]/div[@class="song-info"]//ul[@class="base-info c6"]/li[@class="clearfix"]'))  # 所属专辑
    li.append(soup.xpath('//div[@class="mod-song-info"]/div[@class="song-info"]//ul[@class="base-info c6"]/li[@class="clearfix tag"]'))  # 歌曲标签
    lyric = soup.xpath('//div[@class="mod-song-info"]/div[@class="module song-lyric clicklog-lyric clearfix"]/div[@class="body "]/div[@class="lyric-content"]/@data-lrclink')  # 歌词
    dict = {}

    #歌曲名
    # dict[u'歌曲名：'] = songname[0]
    i = 0
    # 歌手
    if len(li[i]) >= 1:
        title.append(li[i][0].xpath('text()'))
        span = li[i][0].xpath('span[@class="author_list"]/a/text()')
        dict[title[i][0]] = span
        i += 1
    # 所属专辑
    if len(li[i]) >= 1:
        title.append(li[i][0].xpath('text()'))
        span = li[i][0].xpath('a/text()')
        dict[title[i][0]] = span
        i += 1

    # 歌曲标签
    if len(li[i]) >= 1:
        title.append(li[i][0].xpath('span/text()'))
        span = li[i][0].xpath('a/text()')
        dict[title[i][0]] = span
        i += 1
    str = ''

    for k in dict.keys():
        str = str + ''.join(k + '|'.join(dict[k]) + '-')
        # print str
        # print dict[k]
    print tag_dir+'\\'+filename,u"歌曲名:"+del_illegal_char(songname[0])+"-"+(trim(str) + '\n').replace(u'：', ':')
    write_text_file(tag_dir+'\\'+filename,u"歌曲名:"+del_illegal_char(songname[0])+"-"+(trim(str) + '\n').replace(u'：', ':'))

    #写歌词
    if lyric:
        write_content_file(tag_dir+'\\'+del_illegal_char(songname[0])+'.lrc',get_html(lyric[0]))



def save_all_music_information(first_url,tag_url_list,clazz):
    global start,flag
    start = 0
    size = 20
    start = start - size
    third_type = 0

    for c in clazz:
        if c==u'乐播':
            continue
        url_dict = tag_url_list[c]
        tag_mod_dir = create_dir(file_root_dir + '\\' + c)  # 分类文件夹

        url_list = []
        dict = readdict() #存放标签是否被爬过的字典
        for k in url_dict.keys():
            d_flag = 0 #判断此标签有没有被爬过
            flag = 1
            for d in dict:
                if k == d and dict[d] != 0:
                    d_flag = 1
                    print k+' '+u'已被爬取过...'
                    break
            if d_flag == 1:
                continue
            v = url_dict[k]

            foldername = urlcode_tr(v.rsplit('/', 1)[-1])
            tag_dir = create_dir(tag_mod_dir + '\\' + foldername) #标签文件夹

            filename = 'all_'+foldername+'.txt'#该文件存储所有歌曲信息
            totalpage = get_music_totalpage(get_html(first_url + v))
            start = 0 - size
            total = totalpage * size
            # totalpage = 1
            music_url_list = []

            print 'start spider...'
            while True:
                start += size
                end = total / (start+size)
                if end<1:
                    break
                musiclist_html = get_html(first_url+v+'?'+'start={start}&size=20&third_type=0'.format(start=start))

                music_url_list.extend(get_music_url(musiclist_html))

                # print music_url_list
            for music_url in music_url_list:
                music_html = get_html(index+music_url[0])
                #print u'正在索引'
                #print u'正在向{}写入{}文件'.format(tag_dir,filename)
                if is_404(music_html):
                    continue
                # th = threading.Thread(target=save_one_music_information,args=(music_html,tag_dir,filename))
                # th.start()
                save_one_music_information(music_html,tag_dir,filename)
            # break #正式工作时注释
            dict[k] = 1
            writedict(dict)
            url_list.append('http://music.baidu.com/tag' + '/' + foldername)

        # time.sleep(6)  # 爬取一个类别之后停顿一段时间，以免被服务器发现爬虫行为
        write_text_file(tag_mod_dir + '\\' + 'url_list.txt', url_list)#存储各个分类下各个标签的url
        # break #正式工作时注释






# 热门/新歌
# tag_mod_dir+'\\'+tag_dir
# music_information.txt

def main():
    global file_root_dir
    file_root_dir = 'file'
    create_dir(file_root_dir)
    global index,flag
    index = 'http://music.baidu.com'
    tag_url = "http://music.baidu.com/tag"
    tag_html = get_html(tag_url)
    tag_url_list,clazz = get_tag_url_list(tag_html)
    save_all_music_information(index,tag_url_list,clazz)


if __name__=="__main__":
    main()