from xml.etree.ElementTree import parse
import os
import argparse
from PIL import Image


def main(opt):
    mode, rootPath, cropTxt = opt.mode, opt.path, opt.crop_txt
    folderList = os.listdir(rootPath)

    if mode == 'crop':
        rectDic = txt_split(cropTxt)

    print("\n선택 모드: " + mode)
    print("\n----------XML 변환 시작----------\n")

    for folder in folderList:
        print('폴더: ' + folder)
        folderPath = os.path.join(folder, 'Template')
        filePath = rootPath + '/' + folderPath
        files = os.listdir(filePath)
        for file in files:
            if file.split('.')[1] == 'jpg':
                fileName = file.split('.')[0]
                if mode == 'crop':
                    xml_crop(filePath, fileName, rectDic[fileName])
                elif mode == 'resize':
                    print(filePath)
                    print(fileName)
                    print(type(fileName))
                    print(type(filePath))
                    # xml_resize(filePath, fileName)
                else:
                    print('mode 선택 실패')

    print("\n----------XML 변환 완료----------")


def xml_crop(path, fileName, cropRect):
    if cropRect == -1: return

    tree = parse(path + '/' + fileName + '.xml')
    root = tree.getroot()
    root.find("filename").text = fileName + '.jpg'
    root.find("size").find("width").text = cropRect[2]
    root.find("size").find("height").text = cropRect[3]

    for tag in root.iter("object"):
        minX = int(tag.find("bndbox").findtext("xmin"))
        minX_new = minX - int(cropRect[0])
        tag.find("bndbox").find("xmin").text = str(minX_new if minX_new > 0 else 0)

        minY = int(tag.find("bndbox").findtext("ymin"))
        minY_new = minY - int(cropRect[1])
        tag.find("bndbox").find("ymin").text = str(minY_new if minY_new > 0 else 0)

        maxX = int(tag.find("bndbox").findtext("xmax"))
        maxX_new = maxX - int(cropRect[0])
        tag.find("bndbox").find("xmax").text = str(maxX_new if maxX_new < int(cropRect[2]) else cropRect[2])

        maxY = int(tag.find("bndbox").findtext("ymax"))
        maxY_new = maxY - int(cropRect[1])
        tag.find("bndbox").find("ymax").text = str(maxY_new if maxY_new < int(cropRect[3]) else cropRect[3])

    tree.write(path + '/' + fileName + '.xml')

    print(fileName + '.jpg --crop--> (x:' + cropRect[0] + ' y:' + cropRect[1] + ' w:' + cropRect[2] + ' h:' + cropRect[3] + ')')


def x2_change(path, fileName, cropRect):
    if cropRect == -1: return

    tree = parse(path + '/' + fileName + '.xml')
    root = tree.getroot()
    root.find("filename").text = fileName + '.jpg'
    root.find("size").find("width").text = cropRect[2]
    root.find("size").find("height").text = cropRect[3]

    for tag in root.iter("object"):
        if tag.find("name").text is 'address':
            minX = int(tag.find("bndbox").findtext("xmin"))
            maxX = int(tag.find("bndbox").findtext("xmax"))
            maxX_new = round((maxX - minX) / 2) + minX
            tag.find("bndbox").find("xmax").text = maxX_new

    tree.write(path + '/' + fileName + '.xml')


def xml_resize(path, fileName):
    image = Image.open(path + '/' + fileName + '.jpg')
    w, h = image.size[0], image.size[1]

    tree = parse(path + '/' + fileName + '.xml')
    root = tree.getroot()
    size = root.find("size")
    originalWidth = int(size.find("width").text)
    originalHeight = int(size.find("height").text)
    widthRatio = w / originalWidth
    heightRatio = h / originalHeight
    root.find("size").find("width").text = str(w)
    root.find("size").find("height").text = str(h)

    for tag in root.iter("object"):
        minX = int(tag.find("bndbox").findtext("xmin"))
        minX_new = round(minX * widthRatio)
        tag.find("bndbox").find("xmin").text = str(minX_new if minX_new > 0 else 0)

        minY = int(tag.find("bndbox").findtext("ymin"))
        minY_new = round(minY * heightRatio)
        tag.find("bndbox").find("ymin").text = str(minY_new if minY_new > 0 else 0)

        maxX = int(tag.find("bndbox").findtext("xmax"))
        maxX_new = round(maxX * widthRatio)
        tag.find("bndbox").find("xmax").text = str(maxX_new if maxX_new < w else w)

        maxY = int(tag.find("bndbox").findtext("ymax"))
        maxY_new = round(maxY * heightRatio)
        tag.find("bndbox").find("ymax").text = str(maxY_new if maxY_new < h else h)

    tree.write(path + '/' + fileName + '.xml')

    print(fileName + '.jpg (' + str(originalWidth) + ', ' + str(originalHeight) + ') --> (' + str(w) + ', ' + str(h) + ')')


def txt_split(txt):
    f, rectDic = open(txt, 'r'), {}
    while True:
        line = f.readline()
        if not line: break
        value = line.replace("\t", "").replace("\n", "").split(' ')
        rectDic[value[0]] = (value[1], value[2], value[3], value[4]) if value[1] != '-1' else -1
    f.close()
    return rectDic


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='resize')
    parser.add_argument('--path', type=str, default='template')
    parser.add_argument('--crop-txt', type=str, default='crop_list.txt')
    option = parser.parse_args()
    main(opt=option)