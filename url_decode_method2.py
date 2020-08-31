'''
参考网址：
https://www.52pojie.cn/thread-1068403-1-1.html
https://www.52pojie.cn/thread-1074085-1-1.html
https://www.jianshu.com/p/446e57544f57
'''

import base64

# 解密美拍视频真实地址
def decode(encoded_string):
    def getHex(param1):
        return {
            'str': param1[4:],
            'hex': ''.join(list(param1[:4])[::-1]),
        }

    def getDec(param1):
        loc2 = str(int(param1, 16))
        return {
            'pre': list(loc2[:2]),
            'tail': list(loc2[2:]),
        }

    def substr(param1, param2):
        loc3 = param1[0: int(param2[0])]
        loc4 = param1[int(param2[0]): int(param2[0]) + int(param2[1])]
        return loc3 + param1[int(param2[0]):].replace(loc4, "")

    def getPos(param1, param2):
        param2[0] = len(param1) - int(param2[0]) - int(param2[1])
        return param2

    dict2 = getHex(encoded_string)
    dict3 = getDec(dict2['hex'])
    str4 = substr(dict2['str'], dict3['pre'])
    return base64.b64decode(substr(str4, getPos(str4, dict3['tail'])))

orgstr = 'f571Ly9tdUMbDfNgKjnZpZGVvMTEubWVpdHVkYXRhLmNvbS81ZjQ5YzgyNzI2N2Nia2FmemdzNTdnMjc3M19IMjY0XzFfMmI0YzI2MzI4ZWEw6MfYzMubXA0'
video_url = decode(orgstr)
# b'//mvvideo11.meitudata.com/5f49c827267cbkafzgs57g2773_H264_1_2b4c26328ea0c3.mp4'
print(video_url)
