import os

from PIL import Image
from wxpy import *


# 创建头像存储位置
def get_curr_dir():
    curr_dir = os.getcwd() + "/avatars/"
    if not os.path.exists(curr_dir):
        os.mkdir(curr_dir)
    return curr_dir


# 登录并获取好友列表
def login_get_friends():
    bot = Bot()
    return bot.friends()


# 下载好友头像
def down_avatars():
    n = 1
    for friend in login_get_friends():
        friend.get_avatar(get_curr_dir() + str(n) + ".jpg")
        n = n + 1


# 根据好友数量计算每一行排多少个
def cal_pic_size(ls):
    return round(pow(len(ls), 0.5))


# 生成微信头像墙图片
def generate_pic():
    ls = os.listdir(get_curr_dir())
    row_count = cal_pic_size(ls)
    image = Image.new("RGB", (50 * row_count, 50 * row_count))
    x = 0
    y = 0
    for file_names in ls:
        try:
            img = Image.open(get_curr_dir() + file_names)
        except IOError:
            continue
        else:
            # 重新设置图片的大小
            img = img.resize((50, 50), Image.ANTIALIAS)
            # 将图片粘贴到最终的照片墙上
            image.paste(img, (x * 50, y * 50))
            # 设置每一行排row_count个图像
            x += 1
            if x == row_count:
                x = 0
                y += 1
    # 保存头像
    image.save(get_curr_dir() + "friends.jpg")


if __name__ == "__main__":
    down_avatars()
    generate_pic()
    sys.exit()
