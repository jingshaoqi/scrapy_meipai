# 美拍的视频地址解析网址 https://meipai.iiilab.com/
'''
带有blob:http的视频地址如何下载，参考如下网址：
https://blog.csdn.net/angry_mills/article/details/82705595?utm_medium=distribute.pc_relevant.none-task-blog-title-8&spm=1001.2101.3001.4242
https://superuser.com/questions/1033563/how-to-download-video-with-blob-url?answertab=votes

'''
import scrapy
import uuid
import js2py
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
from scrapy.spiders import CrawlSpider, Rule, Spider
from meipai.items import MeipaiItem


# 用python运行js代码进行解密
def get_video_url(str):
    context = js2py.EvalJs()
    with open("meipai.js", "r", encoding="utf-8") as f:
        context.execute(f.read())
        result = context.decodeVideo(str)
        if not result[:4] == 'http':
            result = 'http:' + result
    return result


class MeipaiSpider(Spider):
    name = 'meipai'
    allowed_domains = ['www.meipai.com', 'mvvideo10.meitudata.com', 'mvvideo11.meitudata.com', ]
    # url = 'http://www.tu11.com/xingganmeinvxiezhen/list_1_'
    # offset = 1
    # crawl meipai hot video
    start_urls = ['http://www.meipai.com/medias/hot', ]

    def parse(self, response):
        items = response.xpath('//ul[@id="mediasList"]/li/div/a[@class="content-l-p pa"]')
        for i in items:
            video_link = i.xpath('.//@href').extract()[0]
            # http://www.meipai.com/media/1039574971
            video_link_full = urljoin(response.url, video_link)
            print('video_link_full"{}'.format(video_link_full))
            yield scrapy.Request(url=video_link_full, callback=self.content)

        # next_page = response.xpath('//dl[@class="list-left public-box"]/dd[@class="page"]//a[last()-1]/text()')
        # if "下一页" == next_page.extract()[0]:
        # next_page_url = response.xpath('//dl[@class="list-left public-box"]/dd[@class="page"]//a[last()-1]/@href').extract()[0]
        #     yield response.follow(next_page_url, callback=self.parse)

    def content(self, response):
        with open('res.html','w') as f:
            f.write(response.text)
        # 现在的美拍的视频url地址是经过加密的，可以查看
        # https://www.jianshu.com/p/446e57544f57
        # https://www.52pojie.cn/thread-1074085-1-1.html
        # https://www.52pojie.cn/thread-1068403-1-1.html
        # 中的方法
        # 执行的函数为 playPicsVideo
        # 'c191Ly9tdn5bZUZpZGVvMTEubWVpdHVkYXRhLmNvbS81ZjExZDI1MDlmMjNlOGhqYzRmbTFhOTYyOF9IMjY0XzFfMWZlZTI5Y2U0YmVmZTgubXZwZSACBFA0'
        video_src_data = response.xpath('//div[@id="detailVideo"]/@data-video').get()
        # http://mvvideo11.meitudata.com/5f11d2509f23e8hjc4fm1a9628_H264_1_1fee29ce4befe8.mp4
        video_url = get_video_url(video_src_data)
        url = urljoin(response.url, video_url)
        name = video_url.split('/')[-1]
        print('url:{}'.format(url))
        item = MeipaiItem()
        item['name'] = name
        item['url'] = url
        yield item
        return

        #注意下面的代码在safari和chrome浏览器下是有vido标签的，而在firefox浏览器中没有
        '''
        <div class="mp-h5-player-layer-video">
                  <video id="videoV3aaGyiPJ5JNou1v" src="//mvvideo10.meitudata.com/5f10196aa974e3e2w2k1o73839_H264_1_1dde15d27180d8.mp4"></video>
                </div>
        '''
        chrome_options = Options()

        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 2,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 2,

        }
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option('prefs', prefs)

        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(response.url)
        time.sleep(3)
        url = browser.find_element_by_class_name('mp-h5-player-layer-video').find_element_by_tag_name('video')\
            .get_attribute('src')
        item = MeipaiItem()

        # item['name'] = str(uuid.uuid1())

        item['url'] = url
        yield item












