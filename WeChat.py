import urllib.request

import aggdraw as aggdraw
import requests
from bs4 import BeautifulSoup
import re
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# 查找标题的正则表达式
findTitle = re.compile(r"var msg_title = '(.*?)'")
# 查找图片链接的正则表达式
findJpg = re.compile(r'var msg_cdn_url = "(.*?)";')


# 向url发起get
def ask_url(url):
    try:
        print('自动获取封面标题中\n Tars\n')
        head = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
        request = urllib.request.Request(url=url, headers=head)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print(html)
        return html
    except urllib.error.URLError as e:
        print('出现异常')
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reson'):
            print(e.reson)


# 解析html获得标题与封面
def get_data(html):
    title = re.findall(findTitle, html)  # 获取分享题目
    print(title[0])
    jpg = re.findall(findJpg, html)  # 获取封面图片链接
    # print(jpg[0])
    file_name = "face.jpg"
    res = requests.get(jpg[0])
    with open(file_name, 'wb') as f:
        f.write(res.content)
    return title[0]


# 为图片添加题目
def set_title(text):
    img_opencv = cv2.imread(r'screen.jpg')
    # cv2.imshow('test', img)
    # print(type(img))
    # 357,377
    # cv2.putText(img, text, (357, 377), )
    font = ImageFont.truetype('font_def.ttf', int(configs['title_size']))
    fill_color = (0, 0, 0)
    title_position = (int(configs['title_position'].split(',')[0]), int(configs['title_position'].split(',')[1]))
    img_pil = Image.fromarray(cv2.cvtColor(img_opencv, cv2.COLOR_BGR2RGB))
    if not isinstance(text, np.unicode):
        text = text.decode('utf8')
    draw = ImageDraw.Draw(img_pil)
    draw.text(title_position, text, font=font, fill=fill_color, spacing=11)

    time = input("输入截图时间\n")
    time_font = ImageFont.truetype('font_def.ttf', int(configs['time_size']))
    time_position = (int(configs['time_position'].split(',')[0]), int(configs['time_position'].split(',')[1]))
    time_color = (78, 78, 78)
    # time_color = (255, 0, 0)
    draw.text(time_position, time, font=time_font, fill=time_color)

    time_out = input('输入朋友圈发送时间\n')
    time_out_font = ImageFont.truetype('font_def.ttf', int(configs['time_out_size']))
    time_out_position = (
        int(configs['time_out_position'].split(',')[0]), int(configs['time_out_position'].split(',')[1]))
    time_out_color = (126, 126, 126)
    # time_out_color = (255, 0, 0)
    draw.text(time_out_position, time_out, font=time_out_font, fill=time_out_color)

    name = get_name()
    name_font = ImageFont.truetype('font_def.ttf', int(configs['name_size']))
    name_position = (int(configs['name_position'].split(',')[0]), int(configs['name_position'].split(',')[1]))
    name_color = (87, 106, 150)
    draw.text(name_position, name, font=name_font, fill=name_color, stroke_width=0)
    img_pil.save('demo.jpg', 'jpeg')


# 为图片添加封面
def set_face():
    demo = Image.open('demo.jpg')
    face = Image.open('face.jpg')
    face = face.resize((int(configs['face_size'].split(',')[0]), int(configs['face_size'].split(',')[1])))
    demo.paste(face, (int(configs['face_position'].split(',')[0]), int(configs['face_position'].split(',')[1])))
    demo.save('demo.jpg', 'jpeg')


def set_head():
    head = Image.open('head.jpg')
    head = head.resize((int(configs['head_size'].split(',')[0]), int(configs['head_size'].split(',')[1])))
    # head = round_corner_jpg(head, 30)
    demo = Image.open('demo.jpg')
    demo.paste(head, (int(configs['head_position'].split(',')[0]), int(configs['head_position'].split(',')[1])))
    demo.save('朋友圈截图.jpg', 'jpeg')


def read_config():
    try:
        file = open('config.txt', 'r')
        file = file.read()
    except:
        input('读取配置信息出错，建议尝试重新下载，按任意键退出')
    find_config = re.compile(r"[0-9]{1,2}\.(.*?):")
    find_data = re.compile(r":(.*?);")
    config = re.findall(find_config, file)
    data = re.findall(find_data, file)
    # print(data)
    config_list = {}
    for item in range(len(config)):
        config_list[config[item]] = data[item]
    # print(config_list)
    return config_list


# 圆角函数来源https://www.pyget.cn/p/185266    这个真的带佬T_T
def circle_corner(img, radii):
    """
    圆角处理
    :param img: 源图象。
    :param radii: 半径，如：30。
    :return: 返回一个圆角处理后的图象。
    """

    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形

    # 原图
    img = img.convert("RGBA")
    w, h = img.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    # alpha.show()

    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return img


def round_corner_jpg(image, radius):
    """generate round corner for image"""
    mask = Image.new('L', image.size)  # filled with black by default
    draw = aggdraw.Draw(mask)
    brush = aggdraw.Brush('white')
    width, height = mask.size
    # upper-left corner
    draw.pieslice((0, 0, radius * 2, radius * 2), 90, 180, None, brush)
    # upper-right corner
    draw.pieslice((width - radius * 2, 0, width, radius * 2), 0, 90, None, brush)
    # bottom-left corner
    draw.pieslice((0, height - radius * 2, radius * 2, height), 180, 270, None, brush)
    # bottom-right corner
    draw.pieslice((width - radius * 2, height - radius * 2, width, height), 270, 360, None, brush)
    # center rectangle
    draw.rectangle((radius, radius, width - radius, height - radius), brush)
    # four edge rectangle
    draw.rectangle((radius, 0, width - radius, radius), brush)
    draw.rectangle((0, radius, radius, height - radius), brush)
    draw.rectangle((radius, height - radius, width - radius, height), brush)
    draw.rectangle((width - radius, radius, width, height - radius), brush)
    draw.flush()
    image = image.convert('RGBA')
    image.putalpha(mask)
    return image


def get_name():
    file = open('name.txt', 'r')
    try:
        name = file.read()
    finally:
        file.close()
    return name


if __name__ == '__main__':
    url = input("输入待转发的公众号文章链接\n")
    # url = 'https://mp.weixin.qq.com/s/sx_zfsqAeOpNtOxsBWzxdw'
    text = get_data(ask_url(url))
    # print(text[0:17] + text[18:])
    global configs
    configs = read_config()
    set_title(text[0:19] + '\n' + text[19:])
    set_face()
    set_head()
    input("生成完毕，任意键退出")
