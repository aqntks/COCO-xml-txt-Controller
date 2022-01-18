import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse

path = r'C:\Users\home\Desktop\car_mileage\image\trodo-v01\pascal voc 1.1\Annotations_re'
xml_list = os.listdir(path)

for xml in xml_list:
    if xml.split(".")[1] == 'xml':

        tree = parse(path + '/' + xml)
        root = tree.getroot()
        for tag in root.iter("object"):
            tag.find("bndbox").find("xmin").text = str(int(round(float(tag.find("bndbox").findtext("xmin")))))
            tag.find("bndbox").find("ymin").text = str(int(round(float(tag.find("bndbox").findtext("ymin")))))
            tag.find("bndbox").find("xmax").text = str(int(round(float(tag.find("bndbox").findtext("xmax")))))
            tag.find("bndbox").find("ymax").text = str(int(round(float(tag.find("bndbox").findtext("ymax")))))

        tree.write(f'C:/Users/home/Desktop/car_mileage/image/trodo-v01/annotation_new/{xml}')
        print(xml, '생성')