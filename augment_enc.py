from xml.etree.ElementTree import parse
import os
import cv2
import numpy as np
import argparse
import random
from PIL import ImageFont, ImageDraw, Image, ImageFilter


def fileRandom(path):
    isDir = os.path.isdir(path)
    if isDir:
        cropDir = os.listdir(path)
        ran = random.randrange(0, len(cropDir))
        return cropDir[ran]
    else:
        return -1


def dirDiscovery(cropPath):
    isDir = os.path.isdir(cropPath)
    if isDir:
        cropDir = os.listdir(cropPath)
        cropNum = random.randrange(0, len(cropDir))
        if cropNum == -1:
            addImage = False
        else:
            ranCrop = cropDir[cropNum]
            addImage = True
    else:
        addImage = False

    if addImage:
        return ranCrop
    else:
        return -1


def folderSplit(rootPath):
    template = rootPath + '/template'
    jumin_template = template + '/jumin'
    driver_template = template + '/driver'
    crop = rootPath + '/crop'
    result = rootPath + '/result'

    return template, jumin_template, driver_template, crop, result


def main(opt):
    index, rootPath, endCount = 1, opt.path, opt.count

    template = rootPath + '/template'
    crop = rootPath + '/crop'
    result = rootPath + '/result'
    tempList = os.listdir(template)

    while index <= endCount:
        for file in tempList:
            if file.split('.')[1] == 'jpg':
                fileName = file.split('.')[0]
                image, tree = encnum_only_img(template, fileName, crop, index)
                image.save(result + f'/enc_' + str(index) + '.jpg', 'jpeg')
                tree.write(result + f'/enc_' + str(index) + '.xml', encoding='utf-8')
                print(f'생성: enc_{str(index)}.jpg')
                index = index + 1
                if index > endCount: break


def addFont(fontType, value, img, rect):
    x, y, w, h = rect
    fillList = [(33, 33, 33, 0), (23, 23, 23, 0), (37, 37, 37, 0), (46, 46, 46, 0), (58, 58, 58, 0),
                (66, 66, 66, 0)]
    fillRandom = random.randrange(0, len(fillList))

    # if fontType == 'consolas':
    #     fontName = 'font/CONSOLAB.TTF'
    # if fontType == 'gulim':
    #     fontName = 'font/GulimChe-02.ttf'

    size = w if w > h else h
    font = ImageFont.truetype(fontType, size)
    draw = ImageDraw.Draw(img)

    draw.text((x + (0.25 * w), y), str(value), font=font, fill=fillList[fillRandom])

    return img


def addImage(img, crop, rect):
    x, y, w, h = rect
    image_crop = Image.open(crop).convert('RGBA')
    image_crop = image_crop.resize((w, h))
    img.paste(im=image_crop, box=(x, y), mask=image_crop)
    return img


def loadHangul():
    # 한글 리스트 불러오기
    f, hangul = open('hangul591_list.txt', 'r', encoding='UTF8'), []
    while True:
        line = f.readline().replace("\n", "").strip()
        if not line: break
        hangul.append(line)
    f.close()

    return hangul


def encnum_only_img(templatePath, fileName, cropPath, index):
    image = Image.open(templatePath + '/' + fileName + '.jpg')
    tree = parse(templatePath + '/' + fileName + '.xml')
    root = tree.getroot()

    if index % 2 == 0:
        crop_font_path = cropPath + '/arial'
    else:
        crop_font_path = cropPath + '/consolas'

    for tag in root.iter("object"):
        x, y = int(tag.find("bndbox").findtext("xmin")), int(tag.find("bndbox").findtext("ymin"))
        w, h = int(tag.find("bndbox").findtext("xmax")) - x, int(tag.find("bndbox").findtext("ymax")) - y
        rect = (x, y, w, h)

        dg_en_ran = random.randrange(0, 3)
        if dg_en_ran == 0:
            dg_en_crop = crop_font_path + '/dg'
        else:
            dg_en_crop = crop_font_path + '/en'

        value = dirDiscovery(dg_en_crop)
        filePath = dg_en_crop + f'/{value}'
        tag.find("name").text = str(value)
        ran = fileRandom(filePath)
        crop = filePath + f'/{ran}'
        image = addImage(image, crop, rect)

    image = blur(image)

    return image, tree


def encnum(templatePath, fileName, cropPath):

    image = Image.open(templatePath + '/' + fileName + '.jpg')
    tree = parse(templatePath + '/' + fileName + '.xml')
    root = tree.getroot()

    for tag in root.iter("object"):
        x, y = int(tag.find("bndbox").findtext("xmin")), int(tag.find("bndbox").findtext("ymin"))
        w, h = int(tag.find("bndbox").findtext("xmax")) - x, int(tag.find("bndbox").findtext("ymax")) - y
        rect = (x, y, w, h)

        img_font_ran = random.randrange(0, 2)
        if img_font_ran == 0:
            crop_font_path = cropPath + '/arial'
        else:
            crop_font_path = cropPath + '/consolas'

        if tag.findtext("name") == 'enc':
            if font_img_ran == 0:  # ###### 이미지 합성
                dg_en_ran = random.randrange(0, 3)
                if dg_en_ran == 0:
                    dg_en_crop = crop_font_path + '/dg'
                else:
                    dg_en_crop = crop_font_path + '/en'

                value = dirDiscovery(dg_en_crop)
                filePath = dg_en_crop + f'/{value}'
                tag.find("name").text = str(value)
                ran = fileRandom(filePath)
                crop = filePath + f'/{ran}'
                image = addImage(image, crop, rect)

        # font_img_ran = random.randrange(0, 2)
        font_img_ran = 0
        font_ran = -1
        if tag.findtext("name") == 'enc':
            if font_img_ran == 0:  # ###### 이미지 합성
                dg_en_ran = random.randrange(0, 3)
                if dg_en_ran == 0:
                    dg_en_crop = crop_font_path + '/dg'
                else:
                    dg_en_crop = crop_font_path + '/en'

                value = dirDiscovery(dg_en_crop)
                filePath = dg_en_crop + f'/{value}'
                tag.find("name").text = str(value)
                ran = fileRandom(filePath)
                crop = filePath + f'/{ran}'
                image = addImage(image, crop, rect)
            else:
                if dg_en_ran == 0:  # 숫자 폰트 합성
                    dg_ran = random.randrange(0, 10)
                    tag.find("name").text = str(dg_ran)
                    font_ran = random.randrange(0, 2)
                    if font_ran == 0:  # 숫자 consolas 합성
                        addFont('consolas', dg_ran, image, rect)
                    else:              # 숫자 gulim 합성
                        addFont('gulim', dg_ran, image, rect)
                else:      # 영어 폰트 합성
                    en_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                    dg_ran = random.randrange(0, 26)
                    value = en_list[dg_ran]
                    tag.find("name").text = value
                    font_ran = random.randrange(0, 2)
                    if font_ran == 0:  # 영어 consolas 합성
                        addFont('consolas', value, image, rect)
                    else:  # 영어 gulim 합성
                        addFont('gulim', value, image, rect)

    image = blur(image)

    return image, tree, font_ran


def char(templatePath, fileName):
    image = Image.open(templatePath + '/' + fileName + '.jpg')
    tree = parse(templatePath + '/' + fileName + '.xml')
    root = tree.getroot()

    han = loadHangul()
    en = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
          'W', 'X', 'Y', 'Z']
    dg = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    name = han + en + dg
    fontList = ['font/BatangChe-02.ttf', 'font/GulimChe-02.ttf']

    for tag in root.iter("object"):
        x, y = int(tag.find("bndbox").findtext("xmin")), int(tag.find("bndbox").findtext("ymin"))
        w, h = int(tag.find("bndbox").findtext("xmax")) - x, int(tag.find("bndbox").findtext("ymax")) - y
        rect = (x, y, w, h)

        if tag.findtext("name") == 'char':
            ran = random.randrange(0, len(name))
            value = name[ran]
            tag.find("name").text = value

            font_ran = random.randrange(0, len(fontList))
            ttf = fontList[font_ran]

            addFont(ttf, value, image, rect)

    image = blur(image)

    return image, tree


def blur(image):
    ranNum = random.randrange(0, 12)
    if ranNum == 0: image = image.filter(ImageFilter.BLUR)
    elif ranNum == 1: image = image.filter(ImageFilter.GaussianBlur)
    elif ranNum == 2: image = image.filter(ImageFilter.BoxBlur(1))
    elif ranNum == 3: image = image.filter(ImageFilter.BoxBlur(2))
    elif ranNum == 4: image = image.filter(ImageFilter.BoxBlur(3))
    elif ranNum == 5: image = image.filter(ImageFilter.BoxBlur(4))
    elif ranNum == 6: image = image.filter(ImageFilter.BoxBlur(5))
    else: pass

    return image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='C:/Users/home/Desktop/work/encnum_aug')
    parser.add_argument('--count', type=int, default=100)
    option = parser.parse_args()
    main(opt=option)



