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
    juminFileList = os.listdir(juminTemplatePath)
    driverFileList = os.listdir(driverTemplatePath)

    while index <= endCount:
        for file in juminFileList:
            if file.split('.')[1] == 'jpg':
                fileName = file.split('.')[0]
                augment_img_font(rootPath, juminTemplatePath, fileName, index, 'jumin')
                index = index + 1
                if index > endCount: break
    index = 1
    while index <= endCount:
        for file in driverFileList:
            if file.split('.')[1] == 'jpg':
                fileName = file.split('.')[0]
                augment_img_font(rootPath, driverTemplatePath, fileName, index, 'driver')
                index = index + 1
                if index > endCount: break


def augment(rootPath, templatePath, fileName, index, typeName):
    image = Image.open(templatePath + '/' + fileName + '.jpg')
    tree = parse(templatePath + '/' + fileName + '.xml')
    root = tree.getroot()

    # 한글 리스트 불러오기
    f, hangul = open('hangul520_list.txt', 'r', encoding='UTF8'), []
    while True:
        line = f.readline().replace("\n", "").strip()
        if not line: break
        hangul.append(line)
    f.close()

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

        fontName = 'batang' if typeName == 'jumin' else 'gulim'
        # fontpath = "fonts/gulim.ttc"
        # font = ImageFont.truetype(fontpath, w)
        font = ImageFont.truetype(fontName, w)
        draw = ImageDraw.Draw(image)
        draw.text((x, y), ranHangul, font=font, fill=fillList[fillRandom])

    image = blur(image)

    image.save(rootPath + f'/result/{typeName}_' + str(index) + '.jpg', 'jpeg')
    tree.write(rootPath + f'/result/{typeName}_' + str(index) + '.xml')
    print(f'생성:{typeName}_', str(index) + '.jpg')


def augment_img_font(rootPath, templatePath, fileName, index, typeName):
    # 한글 리스트 불러오기
    f, hangul = open('hangul520_list.txt', 'r', encoding='UTF8'), []
    while True:
        line = f.readline().replace("\n", "").strip()
        if not line: break
        hangul.append(line)
    f.close()

    image = Image.open(templatePath + '/' + fileName + '.jpg')
    tree = parse(templatePath + '/' + fileName + '.xml')
    root = tree.getroot()

    for tag in root.iter("object"):
        x, y = int(tag.find("bndbox").findtext("xmin")), int(tag.find("bndbox").findtext("ymin"))
        w, h = int(tag.find("bndbox").findtext("xmax")) - x, int(tag.find("bndbox").findtext("ymax")) - y

        ranNum = random.randrange(0, len(hangul) + 1)
        ranHangul = hangul[ranNum]
        tag.find("name").text = ranHangul

        cropPath = rootPath + '/crop' + f'/{typeName}_crop' + f'/{ranHangul}'
        isDir = os.path.isdir(cropPath)
        if isDir:
            cropDir = os.listdir(cropPath)
            cropNum = random.randrange(0, len(cropDir) + 1)
            if cropNum == len(cropDir):
                addImage = False
            else:
                ranCrop = cropDir[cropNum]
                addImage = True
        else:
            addImage = False

        if addImage:
            image_crop = Image.open(cropPath + '/' + ranCrop)
            image_crop = image_crop.resize((w, h))
            image.paste(im=image_crop, box=(x, y))
        else:
            fillList = [(33, 33, 33, 0), (23, 23, 23, 0), (37, 37, 37, 0), (46, 46, 46, 0), (58, 58, 58, 0),
                        (66, 66, 66, 0)]
            fillRandom = random.randrange(0, len(fillList))
            fontName = 'batang' if typeName == 'jumin' else 'gulim'
            font = ImageFont.truetype(fontName, w)
            draw = ImageDraw.Draw(image)
            draw.text((x, y), ranHangul, font=font, fill=fillList[fillRandom])

    image = blur(image)

    image.save(rootPath + f'/result/{typeName}_' + str(index) + '.jpg', 'jpeg')
    tree.write(rootPath + f'/result/{typeName}_' + str(index) + '.xml')
    print(f'생성:{typeName}_', str(index) + '.jpg')


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
    parser.add_argument('--path', type=str, default='C:\\Users\\home\\Desktop\\work\\hangul\\hangul')
    parser.add_argument('--count', type=int, default=100)
    option = parser.parse_args()
    main(opt=option)