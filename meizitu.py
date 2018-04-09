import requests
import time
import os
from lxml import etree
from multiprocessing import Pool

headers_1 = {
    'Host': 'www.mzitu.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

headers_2 = {
    'Host': 'www.mzitu.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://www.mzitu.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

headers_3 = {
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://i.meizitu.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36',
}


def download_gallery(gallery_url,title):
    # 得到相册 url ，设置相册 文件夹
    gallery_dir = "E:/python三阶段/高级爬虫/day03/妹子图/" + title

    # 判断目录是否存在
    if os.path.exists(gallery_dir):
        print(gallery_dir + "  -->  " + "目录已存在！！")
        return False
    else:
        try:
            # 创建新的文件夹
            os.makedirs("E:/python三阶段/高级爬虫/day03/妹子图/" + title)
            gallery_dir_new = "E:/python三阶段/高级爬虫/day03/妹子图/" + title

            print("已经创建文件夹：" + gallery_dir_new)

            gallery_response = requests.get(url=gallery_url, headers=headers_2)

            gallery_html = etree.HTML(gallery_response.text)

            max_page = gallery_html.xpath("//div[@class='pagenavi']//a//span/text()")[-2]
            # 最大页码
            print(max_page)

            # 调用下载函数
            download_img(gallery_url, max_page, title)

            print(gallery_dir + "---" + "相册文件下载完成！")

        except:
            print(gallery_dir + "下载失败！！！！！！！！！！！！！！！")

    time.sleep(8)


def download_img(gallery_url, max_page, title):
    # 根据最大页码数，循环获取相册页面
    for i in range(1, int(max_page) + 1):
        gallery_url_new = gallery_url + "/" + str(i)

        print(gallery_url_new)

        gallery_response = requests.get(url=gallery_url_new, headers=headers_2)

        gallery_html = etree.HTML(gallery_response.text)

        pic_url = gallery_html.xpath("//div[@class='main-image']//img/@src")[0]

        pic_name = pic_url.split("/")[-1]

        pic_response = requests.get(url=pic_url, headers=headers_3)
        # E:\python三阶段\高级爬虫\day03\妹子图
        with open("E:/python三阶段/高级爬虫/day03/妹子图/" + title + "/" + pic_name, "wb")as img:
            img.write(pic_response.content)
            print("E:/python三阶段/高级爬虫/day03/妹子图/" + title + "/" + pic_name + "----" + "下载完成")

        time.sleep(2)


if __name__ == '__main__':
    url_str = "http://www.mzitu.com/ "


    response = requests.get(url=url_str, headers=headers_1)

    html = etree.HTML(response.text)

    gallery_html_munber = html.xpath("//div[@class='nav-links']//a/text()")[-2]

    print(gallery_html_munber)

    for i in range(1,int(gallery_html_munber) + 1):
        url_str = "http://www.mzitu.com/page/" + str(i) + "/"

        response = requests.get(url=url_str, headers=headers_1)

        html = etree.HTML(response.text)

        gallery_url_list = html.xpath("//ul[@id='pins']//span//a/@href")
        title_list = html.xpath("//ul[@id='pins']//span//a/text()")

        print(gallery_url_list)
        print(title_list)

        pool = Pool(6)

        for gallery_url, title in zip(gallery_url_list, title_list):
            pool.apply_async(func=download_gallery, args=(gallery_url,title))

        pool.close()
        pool.join()

        time.sleep(10)
