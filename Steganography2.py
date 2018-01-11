#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

'''基于rgb分量最低位的隐写术：以红色分量为例，即是操纵“红色亮度”字节最后一个比特位。譬如我们想把’A’隐藏进来的话，
就可以把A转成16进制的0x61再转成二进制的01100001，再修改为红色通道的最低位为这些二进制串。'''


def f(pixel):
    # 显示处理
    if pixel % 2 == 1:
        return pixel
    return 0


def showImage(image):
    # 解码隐写术
    image.getdata()
    r, g, b = image.split()
    showimage = Image.eval(r, f)  # 解密图层通道,有（r,g,b)
    showimage.show()


def drawtext(size, text):
    # 获取写入数据的图像信息
    im2 = Image.new(im.mode, size, color="white")
    draw = ImageDraw.Draw(im2)
    span = size[0] // (3 * len(text))  # 字体大小
    font = ImageFont.truetype("msyh.ttf", size=span)
    # print(len(text))
    draw.text(((size[0] - len(text) * span) / 2, (size[1] - span) / 2), text, fill="black", font=font)

    return im2


def encodeRGB(image, text):
    # 隐写术加密
    txtimage = drawtext(image.size, text)

    pixels = list(image.getdata())  # 获取俩图的像素信息
    pixels2 = list(txtimage.getdata())

    evenpixels = []  # 加密后像素列表
    index = 0
    for [r2, g2, b2] in pixels2:
        r, g, b = pixels[index]
        if r2 % 256 == 0:  # 加密图层通道（r2,g2,b2）
            evenpixels.append(((r >> 1 << 1) + 1, g >> 1 << 1, b >> 1 << 1))
        else:
            evenpixels.append((r >> 1 << 1, g >> 1 << 1, b >> 1 << 1))
        index += 1

    evenimage = Image.new(im.mode, im.size)
    evenimage.putdata(evenpixels)
    # evenimage.show()
    return evenimage


def openimg(imgname):
    # 打开图片
    image = Image.open(imgname, 'r')
    image = image.convert("RGB")
    return image


if __name__ == "__main__":
    imagename = "demo2.png"  # 图片路径
    im = openimg(imagename)
    encodeim = encodeRGB(im, "你好")
    encodeim.save("new" + imagename)
    showImage(encodeim)
