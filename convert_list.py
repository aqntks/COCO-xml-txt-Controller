#-*- coding: utf-8 -*-

import xml_search.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

from os import listdir
from os.path import isfile, join


#classes = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","<","mrz"]

#classes = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q",
#"R","S","T","U","V","W","X","Y","Z","<","mrz",".","-", "title_jumin", "name", "regnum", "issuedate",
#"title_driver", "local_busan", "local_cb", "local_cn", "local_daegu", "local_daejeon", "local_incheon", "local_jb", "local_jeju", "local_jn", "local_kangwon", "local_kb", "local_kn", "local_kyounggi", "local_seoul", "local_ulsan", 
#"licensenum", "encnum", "title_welfare", "expire", "kor", "nationality", "visatype"]


classes = []


# 문서에서 클래스 받아오는 경우
f, hangul = open('hangul520_list.txt', 'r', encoding='utf-8'), []
while True:
    line = f.readline().replace("\n", "").strip()
    if not line: break
    classes.append(line)
f.close()


# classes = ["가","간","갈","감","강","개","거","건","걸","검","겨","견","결","겸","경","계","고","곤","곱","공","과","곽","관","광","굉","교","구","국","군","궁","권","귀","규","균","귤","그","근","글","금","긍","기","긴","길","김","까","꼴","꽃","끄","끌","끼","나","낙","난","날","남","내","낸","너","네","넬","넷","녀","년","녕","녜","노","녹","누","눅","눈","눌","눔","뉴","느","늘","능","늬","니","님","다","단","달","닮","담","당","닻","대","더","덕","던","데","덴","델","도","돈","동","두","둘","드","득","든","들","듬","듭","디","딜","딸","뜰","뜸","띠","라","락","란","람","랑","래","랜","량","런","럿","레","렉","렌","렘","렙","려","력","련","렬","렴","령","례","로","록","론","롤","롬","롭","롱","료","룡","루","룩","룬","룰","룸","룻","류","륜","률","륭","르","른","를","름","릉","리","릭","린","릴","림","립","링","마","막","만","말","맑","망","매","맥","맹","머","메","멜","면","명","모","목","몬","몽","묘","무","묵","문","물","미","민","믿","밀","바","박","반","발","밝","방","배","백","버","범","법","베","벤","벧","벨","벼","벽","변","별","병","보","복","본","봄","봉","부","분","붕","브","블","비","빅","빈","빌","빗","빛","쁘","쁨","사","삭","산","살","삼","삽","상","새","샘","샛","생","샤","샨","샬","섀","서","석","선","설","섬","섭","성","세","센","셀","셈","셉","션","셜","셸","소","손","솔","솜","솝","송","숀","수","숙","순","술","숲","쉴","슈","슐","스","슨","슬","승","시","식","신","실","심","쌍","써","썸","씨","아","안","알","암","압","앙","애","앤","앨","앰","앵","야","약","얀","양","어","억","언","얼","엄","업","에","엔","엘","엠","여","역","연","열","염","엽","영","예","옌","오","옥","온","올","옴","옹","와","완","왕","요","욤","욥","용","우","욱","운","울","움","웅","원","월","위","윈","윌","윗","유","육","윤","율","윰","융","으","은","을","음","응","의","이","익","인","일","임","잎","자","잔","잘","장","재","잭","쟈","저","적","전","절","정","제","젤","조","존","종","좌","죠","주","준","줄","중","쥬","쥴","즈","지","직","진","집","징","차","찬","찰","참","창","채","처","천","철","첫","청","체","첼","초","총","최","추","축","춘","충","취","츠","치","칙","칠","카","칸","칼","캐","캘","커","컨","케","켄","켈","코","콜","쿠","크","클","키","타","탁","탄","탈","탐","태","택","터","테","텔","토","통","튀","튜","트","특","튼","티","틸","파","판","팔","패","팽","퍼","페","편","평","포","폴","표","푸","풀","풍","프","플","피","핀","필","하","학","한","할","함","합","항","해","햇","행","향","허","헌","헤","헨","헬","헵","혁","현","협","형","혜","호","홀","홍","화","환","활","황","회","효","후","훈","훔","훤","휘","휴","휼","흔","흘","흠","흥","희","흰","히","힘"]



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


    tree=ET.parse(image_path)
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
#        cnt_lst[cls_id] = cnt_lst[cls_id] + 1
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        # out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    
    #전체를 label로인식
    #b2 = (float(1), float(w-1), float(1), float(h-1))
    #bb2 = convert((w,h), b2)
    #out_file.write(str(46) + " " + " ".join([str(a) for a in bb2]) + '\n')
    
xml_label_path = '/home/code1system/workspace/data/hangul/result'
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
   
    tree=ET.parse(temp_path)
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
