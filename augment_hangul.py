from xml.etree.ElementTree import parse
import os
import argparse
import random
from PIL import ImageFont, ImageDraw, Image, ImageFilter


def main(opt):
    index, rootPath, endCount = 1, opt.path, opt.count
    templatePath = rootPath + '/template'
    juminTemplatePath = templatePath + '/jumin'
    driverTemplatePath = templatePath + '/driver'
    # juminFileList = os.listdir(juminTemplatePath)
    # driverFileList = os.listdir(driverTemplatePath)
    filelist = os.listdir(templatePath)

    while index <= endCount:
        for file in filelist:
            if file.split('.')[1] == 'jpg':
                fileName = file.split('.')[0]
                augment(rootPath, templatePath, fileName, index)
                index = index + 1
                if index > endCount: break
    # index = 1
    # while index <= endCount:
    #     for file in driverFileList:
    #         if file.split('.')[1] == 'jpg':
    #             fileName = file.split('.')[0]
    #             augment(rootPath, driverTemplatePath, fileName, index, 'gulim')
    #             index = index + 1
    #             if index > endCount: break


def augment(rootPath, templatePath, fileName, index):
    image = Image.open(templatePath + '/' + fileName + '.jpg')
    tree = parse(templatePath + '/' + fileName + '.xml')
    root = tree.getroot()

    # # 한글 리스트 불러오기
    # f, hangul = open('hangul591_list.txt', 'r', encoding='UTF8'), []
    # while True:
    #     line = f.readline().replace("\n", "").strip()
    #     if not line: break
    #     hangul.append(line)
    # f.close()

    hangul = ['안', '도', '경']

    for tag in root.iter("object"):
        x, y = int(tag.find("bndbox").findtext("xmin")), int(tag.find("bndbox").findtext("ymin"))
        w, h = int(tag.find("bndbox").findtext("xmax")) - x, int(tag.find("bndbox").findtext("ymax")) - y
        ranNum = random.randrange(0, len(hangul))
        ranHangul = hangul[ranNum]

        tag.find("name").text = ranHangul

        # fontList = ['batang', 'gulim']
        # fontRandom = random.randrange(0, len(fontList))
        fillList = [(33, 33, 33, 0),(23, 23, 23, 0),(37, 37, 37, 0),(46, 46, 46, 0),(58, 58, 58, 0),(66, 66, 66, 0)]
        fillRandom = random.randrange(0, len(fillList))

        # fontList = ['batang', 'gulim']
        # fontType = 'fonts/batang.ttc' if fontName == 'batang' else 'fonts/gulim.ttc'
        # fontpath = "fonts/gulim.ttc"
        # font = ImageFont.truetype(fontpath, w)
        font = ImageFont.truetype('font/GulimChe-02.ttf', w)
        draw = ImageDraw.Draw(image)
        draw.text((x, y), ranHangul, font=font, fill=fillList[fillRandom])

    # image = blur(image)

    image.save(rootPath + f'/result/_' + str(index) + '.jpg', 'jpeg')
    tree.write(rootPath + f'/result/_' + str(index) + '.xml', encoding='utf-8')
    print(f'생성: -', str(index) + '.jpg')


def blur(image):
    ranNum = random.randrange(0, 5)
    if ranNum == 0: image = image.filter(ImageFilter.BLUR)
    elif ranNum == 1: image = image.filter(ImageFilter.GaussianBlur)
    elif ranNum == 2: image = image.filter(ImageFilter.BoxBlur(3))
    elif ranNum == 3: image = image.filter(ImageFilter.BoxBlur(5))
    else: pass

    return image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='C:/Users/home/Desktop/work/ko_en_dg')
    parser.add_argument('--count', type=int, default=100)
    option = parser.parse_args()
    main(opt=option)
