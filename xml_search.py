from xml.etree.ElementTree import parse

import os

def watchDir(path):
    output = os.listdir(path)
    filelist = []

    for i in output:
        if os.path.isdir(path + "/" + i):
            filelist.extend(watchDir(path + "/" + i))
        elif os.path.isfile(path + "/" + i):
            filelist.append(path + "/" + i)

    return filelist


if __name__ == "__main__":
    img_path = 'C:/Users/home/Desktop/temp'

    result = set()

    fileList = watchDir(img_path)
    for file in fileList:
        tree = parse(file)
        root = tree.getroot()

        for tag in root.iter("object"):
            result.add(tag.find("name").text)

    result = sorted(result)

    print(result)


