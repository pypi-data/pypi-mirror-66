
## 简介
基于 Python 的新浪微博图床实现。


## 安装
```
pip install pyweibo-picbed
```




## 使用

示例1：
```python
>>> from pyweibo_picbed import weibo_picbed
# 在剪切板没有截图的情况下
>>> weibo_picbed.upload_screenshot_to_weibo()
(False, 'no imgs in clipboard!')

# 手动截图且截图保存在剪切板后
>>> weibo_picbed.upload_screenshot_to_weibo()
(True, 'http://ww2.sinaimg.cn/large/aac28c44gy1ge5bq4tzzej30u00l4aei.jpg')
```

示例2：
```python
from pyweibo_picbed import weibo_picbed
state, msg = weibo_picbed.upload_screenshot_to_weibo()
if state:       # 截图成功
    print(weibo_picbed.get_html_type_img_url(msg))
    print(weibo_picbed.get_markdown_type_img_url(msg))
else:           # 获得错误信息
    print("error: %s" % msg)
'''
<img src="http://ww2.sinaimg.cn/large/aac28c44gy1ge5bq4tzzej20u00l4aei.jpg"/>'
<img src="http://wx3.sinaimg.cn/large/aac28c44gy1ge5c1yqu4cj20u00l4q3c.j
pg"/>
![img](http://wx3.sinaimg.cn/large/aac28c44gy1ge5c1yqu4cj20u00l4q3c.jpg)
'''
```




## 参考
- https://github.com/suxiaogang/WeiboPicBed



