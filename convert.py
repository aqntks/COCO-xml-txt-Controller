#-*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

from os import listdir
from os.path import isfile, join

# classes = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q",
#            "R","S","T","U","V","W","X","Y","Z","<","mrz",".","-","~",
#            "title_jumin", "name", "regnum", "addr", "issuedate", "issueplace",
#            "title_driver", "local", "licensenum", "encnum", "period", "condition", "drivetype",
#            "title_welfare", "gradetype", "expire",
#            "kor", "sex", "nationality", "visatype"]

classes = ["odometer"]

cnt_lst = []
for i in range(len(classes)):
    cnt_lst.append(0)


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


def convert_annotation(image_path, yolo_label_path):
    file_name = os.path.split(image_path)[-1]
    #save_file = os.path.join(yolo_label_path,(file_name.split('.xml')[0]+'.txt'))
    save_file = image_path.split('.xml')[0]+'.txt'
    #out_file = open(save_file, 'w')
    out_file = open(save_file, 'w', newline='\n')

    tree = ET.parse(image_path)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    
    for obj in root.iter('object'):
        cls = obj.find('name').text
        print("클래스 명:  " + cls)
        if cls =='gasmeter':
            cls = 'meter'
        if cls == 'exc2' or cls == 'exc3':
            cls = 'exc1'
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
#       cnt_lst[cls_id] = cnt_lst[cls_id] + 1
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        # out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    
    #전체를 label로인식
    #b2 = (float(1), float(w-1), float(1), float(h-1))
    #bb2 = convert((w,h), b2)
    #out_file.write(str(46) + " " + " ".join([str(a) for a in bb2]) + '\n')
    
xml_label_path = r'C:\Users\home\Desktop\jjj'
yolo_label_path = '123'

total_paths = [join(xml_label_path, f) for f in listdir(xml_label_path) if isfile(join(xml_label_path, f))]
#root_path = [join(xml_label_path, f) for f in listdir(xml_label_path)]
#for sub in root_path:
#    total_paths = [join(sub, f) for f in listdir(sub) if isfile(join(sub, f))]

cnt = 0
total_width = 0
total_height = 0

for temp_path in total_paths:
    if not temp_path.endswith('.xml'):
        continue
    print(temp_path)
    
    tree = ET.parse(temp_path)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    total_width = total_width + w
    total_height = total_height + h
    
    #convert_annotation(temp_path,yolo_label_path)
    convert_annotation(temp_path,temp_path)
    cnt = cnt + 1

print(cnt, 'files')

print("avg w : " + str(total_width/cnt))
print("avg h : " + str(total_height/cnt))
for i in range(len(classes)):
    print(classes[i] + ' : ' + str(cnt_lst[i]))