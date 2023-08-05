import json
import requests
def geturl(date:str):
    rep = requests.get("http://rdpstudio.utools.club/bingpan/devloperapi.php?date=" + date) # 请求接口
    content = rep.text # 获取返回结果
    user_dic = json.loads(content) # 解析json
    d2 = json.loads(json.dumps(user_dic['content'])) # 解析需要的部分
    imgurl = d2[0]['imgurl'] # 获取图片地址
    return imgurl
