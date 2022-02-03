from unittest import expectedFailure
from urllib import request
from bs4 import BeautifulSoup
import xml.dom.minidom

#会津大学 イベント 在学生向け一覧
#https://www.u-aizu.ac.jp/events/students/
def Get_RSS(url,title_data):
    res = request.urlopen(url)

    soup = BeautifulSoup(res, 'html.parser')

    A = soup.find_all('div', class_='event-content')

    rss_dom = xml.dom.minidom.Document()

    rss = rss_dom.createElement('rss')
    rss_version_attr = rss_dom.createAttribute('version')
    rss_version_attr.value = '2.0'
    rss.setAttributeNode(rss_version_attr)

    channel = rss_dom.createElement('channel')
    #rss_version_attr = rss_dom.createAttribute('version')
    #rss_version_attr.value = '2.0'
    #rss.setAttributeNode(rss_version_attr)
    title = rss_dom.createElement('title')
    title.appendChild(rss_dom.createTextNode(title_data))
    link = rss_dom.createElement('link')
    link.appendChild(rss_dom.createTextNode(url))
    description = rss_dom.createElement('description')
    description.appendChild(rss_dom.createTextNode(title_data))

    channel.appendChild(title)
    channel.appendChild(link)
    channel.appendChild(description)

    rss.appendChild(channel)

    rss_dom.appendChild(rss)

    for e in A:
        try:
            item = rss_dom.createElement('item')

            title_data=e.select('p.post-title')[0].a.text
            link_data=e.select('p.post-title')[0].select('a')[0].attrs['href']

            date_elem=e.select('.date')[0]
            where_elem=e.select('.date')[1]

            date_data="{0}".format(date_elem.get_text(separator=' '))
            where_data="{0}".format(where_elem.get_text(separator=' '))

            """
            print("----------")
            print(title_data)
            print(link_data)
            print(date_data)
            print(where_data)
            """

            item_title = rss_dom.createElement('title')
            item_description = rss_dom.createElement('description')
            item_pubDate = rss_dom.createElement('pubDate')

            item_title.appendChild(rss_dom.createTextNode(title_data))
            item_description.appendChild(rss_dom.createTextNode(date_data))
            item_description.appendChild(rss_dom.createElement("br"))
            item_description.appendChild(rss_dom.createTextNode(where_data))
            item_description.appendChild(rss_dom.createElement("br"))
            item_description.appendChild(rss_dom.createTextNode(link_data))
            item_description.appendChild(rss_dom.createElement("br"))
            item_pubDate.appendChild(rss_dom.createTextNode(""))

            item.appendChild(item_title)
            item.appendChild(item_description)
            item.appendChild(item_pubDate)
            
            channel.appendChild(item)
        except IndexError:
            pass



    return rss_dom.toprettyxml()

import http.server
import socketserver
import threading
import time

def search_RSS():
    while True:
        with open("./RSS/events_for_student.xml","w",encoding="utf-8") as f:
            f.write(Get_RSS("https://www.u-aizu.ac.jp/events/students/","会津大学 イベント 在学生向け一覧"))
        with open("./RSS/events_for_visitorst.xml","w",encoding="utf-8") as f:
            f.write(Get_RSS("https://www.u-aizu.ac.jp/events/visitors/","会津大学 イベント 一般向け一覧"))
        with open("./RSS/events_for_parents.xml","w",encoding="utf-8") as f:
            f.write(Get_RSS("https://www.u-aizu.ac.jp/events/parents/","会津大学 イベント 保護者向け一覧"))
        with open("./RSS/events_for_alumni.xml","w",encoding="utf-8") as f:
            f.write(Get_RSS("https://www.u-aizu.ac.jp/events/alumni/","会津大学 イベント 卒業生向け一覧"))
        print("クローリング...")
        time.sleep(1)

        with open("./RSS/info_news.xml","w",encoding="utf-8") as f:
            f.write(Get_RSS("https://www.u-aizu.ac.jp/information/news/","会津大学 ニュース"))
        with open("./RSS/info_admissions.xml","w",encoding="utf-8") as f:
            f.write(Get_RSS("https://www.u-aizu.ac.jp/information/admissions/","会津大学 入試情報"))
        with open("./RSS/info_uarc.xml","w",encoding="utf-8") as f:
            f.write(Get_RSS("https://www.u-aizu.ac.jp/information/uarc/","会津大学 復興支援センター情報"))
        with open("./RSS/info_employment_faculty.xml","w",encoding="utf-8") as f:
            f.write(Get_RSS("https://www.u-aizu.ac.jp/information/employment-faculty/","会津大学 教員採用情報一覧"))

        print("クローリング...")
        time.sleep(60*60)

t1 = threading.Thread(target=search_RSS)
t1.start()

PORT = 80
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="./RSS", **kwargs)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()


