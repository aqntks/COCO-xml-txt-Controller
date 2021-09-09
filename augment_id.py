from xml_search.etree.ElementTree import parse
import os
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
    index, rootPath, jumin_count, driver_count = 1, opt.path, opt.jumin_count, opt.driver_count

    template, jumin_template, driver_template, crop, result = folderSplit(rootPath)

    juminFileList = os.listdir(jumin_template)
    driverFileList = os.listdir(driver_template)

    img_font_ran = random.randrange(0, 2)
    if img_font_ran == 0:
        crop_font_path = crop + '/encnum/arial'
    else:
        crop_font_path = crop + '/encnum/consolas'

    #
    # while index <= jumin_count:
    #     for file in juminFileList:
    #         if file.split('.')[1].lower() == 'jpg':
    #             fileName = file.split('.')[0]
    #             image, tree = jumin(template + '/jumin', fileName, crop)
    #             image.save(result + '/jumin/jumin_' + str(index) + '.jpg', 'jpeg')
    #             tree.write(result + '/jumin/jumin_' + str(index) + '.xml')
    #             print(f'생성: jumin_{str(index)}.jpg')
    #             index = index + 1
    #             if index > jumin_count: break

    index = 1
    while index <= driver_count:
        for file in driverFileList:
            if file.split('.')[1].lower() == 'jpg':
                fileName = file.split('.')[0]
                image, tree = driver(template + '/driver', fileName, crop, crop_font_path)
                image.save(result + '/driver/driver_' + str(index) + '.jpg', 'jpeg')
                tree.write(result + '/driver/driver_' + str(index) + '.xml')
                print(f'생성: driver_{str(index)}.jpg')
                index = index + 1
                if index > driver_count: break


def addFont(fontType, value, img, rect):
    x, y, w, h = rect
    fillList = [(33, 33, 33, 0), (23, 23, 23, 0), (37, 37, 37, 0), (46, 46, 46, 0), (58, 58, 58, 0),
                (66, 66, 66, 0)]
    fillRandom = random.randrange(0, len(fillList))
    if fontType == 'somang':
        fontType = 'batang'

    size = w if w > h else h
    font = ImageFont.truetype(fontType, size)
    draw = ImageDraw.Draw(img)

    draw.text((x, y), str(value), font=font, fill=fillList[fillRandom])

    return img


def addImage(img, crop, rect):
    x, y, w, h = rect
    image_crop = Image.open(crop)
    image_crop = image_crop.resize((w, h))
    img.paste(im=image_crop, box=(x, y))
    return img


def addImageA(img, crop, rect):
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


def jumin(templatePath, fileName, cropPath):
    hangul = loadHangul()

    image = Image.open(templatePath + '/' + fileName + '.jpg')
    tree = parse(templatePath + '/' + fileName + '.xml')
    root = tree.getroot()

    for tag in root.iter("object"):
        x, y = int(tag.find("bndbox").findtext("xmin")), int(tag.find("bndbox").findtext("ymin"))
        w, h = int(tag.find("bndbox").findtext("xmax")) - x, int(tag.find("bndbox").findtext("ymax")) - y
        rect = (x, y, w, h)

        if tag.findtext("name").split('_')[-1] == 'ko' or tag.findtext("name").split('_')[-1] == 'kor':
            if tag.findtext("name") == 'name_ko' or tag.findtext("name") == 'jumin_kor':
                fontType = 'batang'
            if tag.findtext("name") == 'addr_ko':
                fontType = 'batang'
            if tag.findtext("name") == 'issueplace_ko' or tag.findtext("name") == 'issue_kor':
                fontType = 'somang'
            ranNum = random.randrange(0, len(hangul))
            value = hangul[ranNum]
            tag.find("name").text = str(value)
            image = addFont(fontType, value, image, rect)
        if tag.findtext("name") == 'regnum_dg' or tag.findtext("name") == 'addr_dg':
            if tag.findtext("name") == 'regnum_dg':
                fontType = 'gulim'
            if tag.findtext("name") == 'addr_dg':
                fontType = 'batang'
            value = random.randrange(0, 10)
            tag.find("name").text = str(value)
            image = addFont(fontType, value, image, rect)
        if tag.findtext("name") == 'regnum_hyp':
            value = '-'
            tag.find("name").text = str(value)
            image = addFont('gulim', value, image, rect)
        if tag.findtext("name") == 'issuedate_dot':
            value = '.'
            tag.find("name").text = str(value)
            image = addFont('somang', value, image, rect)
        if tag.findtext("name") == 'issuedate_dg':  # ###### 이미지 합성
            folderPath = cropPath + '/jumin_issue'
            value = dirDiscovery(folderPath)
            filePath = folderPath + f'/{value}'
            tag.find("name").text = str(value)
            ran = fileRandom(filePath)
            crop = filePath + f'/{ran}'
            image = addImage(image, crop, rect)
        if tag.findtext("name") == 'title_jumin' or tag.findtext("name") == 'title-jumin':  # ###### 이미지 합성
            folderPath = cropPath + '/title_jumin'
            ran = fileRandom(folderPath)
            crop = folderPath + f'/{ran}'
            image = addImage(image, crop, rect)

    # image = blur(image)

    return image, tree


def driver(templatePath, fileName, cropPath, crop_font_path):
    hangul = loadHangul()

    image = Image.open(templatePath + '/' + fileName + '.jpg')
    tree = parse(templatePath + '/' + fileName + '.xml')
    root = tree.getroot()

    for tag in root.iter("object"):
        x, y = int(tag.find("bndbox").findtext("xmin")), int(tag.find("bndbox").findtext("ymin"))
        w, h = int(tag.find("bndbox").findtext("xmax")) - x, int(tag.find("bndbox").findtext("ymax")) - y
        rect = (x, y, w, h)

        if tag.findtext("name").split('_')[-1] == 'ko':
            ranNum = random.randrange(0, len(hangul))
            value = hangul[ranNum]
            tag.find("name").text = str(value)
            addFont('gulim', value, image, rect)
        if tag.findtext("name") == 'addr_dg' \
                or tag.findtext("name") == 'period_dg' \
                or tag.findtext("name") == 'issuedate_dg' \
                or tag.findtext("name") == 'drivetype_dg':
            value = random.randrange(0, 10)
            tag.find("name").text = str(value)
            addFont('gulim', value, image, rect)
        if tag.findtext("name") == 'licensenum_dg' or tag.findtext("name") == 'regnum_dg':  # ## 합성
            folderPath = cropPath + '/driver_number'
            value = dirDiscovery(folderPath)
            filePath = folderPath + f'/{value}'
            tag.find("name").text = str(value)
            ran = fileRandom(filePath)
            crop = filePath + f'/{ran}'
            image = addImage(image, crop, rect)
        if tag.findtext("name") == 'encnum_dg':   # ## 합성
            folderPath = crop_font_path + '/dg'
            value = dirDiscovery(folderPath)
            filePath = folderPath + f'/{value}'
            tag.find("name").text = str(value)
            ran = fileRandom(filePath)
            crop = filePath + f'/{ran}'
            image = addImageA(image, crop, rect)
        if tag.findtext("name") == 'addr_en':
            value = random.randrange(0, 10)
            tag.find("name").text = str(value)
            addFont('gulim', value, image, rect)
        if tag.findtext("name") == 'encnum_en':   # ## 합성
            folderPath = crop_font_path + '/en'
            value = dirDiscovery(folderPath)
            filePath = folderPath + f'/{value}'
            tag.find("name").text = str(value)
            ran = fileRandom(filePath)
            crop = filePath + f'/{ran}'
            image = addImageA(image, crop, rect)
        if tag.findtext("name") == 'licensenum_hyp' or tag.findtext("name") == 'regnum_hyp': ### 합성
            folderPath = cropPath + '/driver_hyp'
            ran = fileRandom(folderPath)
            crop = folderPath + f'/{ran}'
            image = addImage(image, crop, rect)
        if tag.findtext("name") == 'period_dot':
            value = '.'
            tag.find("name").text = str(value)
            image = addFont('gulim', value, image, rect)
        if tag.findtext("name") == 'period_wave':
            value = '~'
            tag.find("name").text = str(value)
            image = addFont('gulim', value, image, rect)
        if tag.findtext("name") == 'issuedate_dot':
            value = '.'
            tag.find("name").text = str(value)
            image = addFont('gulim', value, image, rect)
        if tag.findtext("name") == 'title_driver':  # ###### 이미지 합성
            folderPath = cropPath + '/title_driver'
            ran = fileRandom(folderPath)
            crop = folderPath + f'/{ran}'
            image = addImage(image, crop, rect)
        if tag.findtext("name") == 'local':  # ###### 이미지 합성
            folderPath = cropPath + '/region_code_25'
            value = dirDiscovery(folderPath)
            filePath = folderPath + f'/{value}'
            tag.find("name").text = str(value)
            ran = fileRandom(filePath)
            crop = filePath + f'/{ran}'
            image = addImage(image, crop, rect)
        # ## 지역   ### 합성

    # image = blur(image)

    return image, tree


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
    parser.add_argument('--path', type=str, default='C:/Users/home/Desktop/work/augment')
    parser.add_argument('--jumin_count', type=int, default=100)
    parser.add_argument('--driver_count', type=int, default=100)
    option = parser.parse_args()
    main(opt=option)