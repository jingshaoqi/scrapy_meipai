'''
参考网址：
https://www.52pojie.cn/thread-1068403-1-1.html
https://www.52pojie.cn/thread-1074085-1-1.html
https://www.jianshu.com/p/446e57544f57
'''

import js2py

# 用python运行js代码进行解密
def get_video_url(str):
    context = js2py.EvalJs()
    with open("meipai.js", "r", encoding="utf-8") as f:
        context.execute(f.read())
        result = context.decodeVideo(str)
        if not result[:4] == 'http':
            result = 'http:' + result
    return result

orgstr = 'f571Ly9tdUMbDfNgKjnZpZGVvMTEubWVpdHVkYXRhLmNvbS81ZjQ5YzgyNzI2N2Nia2FmemdzNTdnMjc3M19IMjY0XzFfMmI0YzI2MzI4ZWEw6MfYzMubXA0'
video_url = get_video_url(orgstr)
# http://mvvideo11.meitudata.com/5f49c827267cbkafzgs57g2773_H264_1_2b4c26328ea0c3.mp4
print(video_url)
