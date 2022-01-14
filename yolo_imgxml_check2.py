import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import os


path = r"/home/code1system/workspace/data/1"

anno_set = set()
anno_dict = dict()

for ld in os.listdir(path):
    if ld.split(".")[1] == "xml":
        tree = parse(f'{path}/{ld}')
        root = tree.getroot()

        for tag in root.iter("object"):
            anno_set.add(tag.find("name").text)

            if tag.find("name").text in anno_dict:
                anno_dict[tag.find("name").text] = anno_dict[tag.find("name").text] + 1
            else:
                anno_dict[tag.find("name").text] = 1


print(len(anno_set),  anno_set)
print(anno_dict)