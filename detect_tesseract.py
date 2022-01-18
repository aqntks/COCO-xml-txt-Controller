import argparse
import time
from pathlib import Path

from PIL import Image     #pip install pillow
from pytesseract import * #pip install pytesseract
import configparser
import os

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

# colab에서만 적용
from google.colab.patches import cv2_imshow

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

def ocrToStr(imgNumpy, outTxtPath, fileName, lang='eng'): #디폴트는 영어로 추출
    #이미지 경로
    #이미지 file read 방식 1) Image.open(path) , 2) cv2.imread(Path)
    img = imgNumpy

    txtName = os.path.join(outTxtPath,fileName.split('.')[0])

    #추출(이미지파일, 추출언어, 옵션)
    #preserve_interword_spaces : 단어 간격 옵션을 조절하면서 추출 정확도를 확인한다.
    #psm(페이지 세그먼트 모드 : 이미지 영역안에서 텍스트 추출 범위 모드)
    #psm 모드 : https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage
    outText = image_to_string(img, lang=lang, config='')
    print('+++ OCT Extract Result +++')
    print('Extract FileName ->>> : ', fileName, ' : <<<-')
    print('\n\n')
    #출력
    print(outText.replace(" ","")) # 단어 사이 공백 제거
    #추출 문자 텍스트 파일 쓰기
    strToTxt(txtName, outText)

#문자열 -> 텍스트파일 개별 저장
def strToTxt(txtName, outText):
    with open(txtName + '.txt', 'w', encoding='UTF-8') as f:
        f.write(outText)
        f.write("\n\n\n")
        f.write(outText.replace(" ", ""))

def detect(save_img=False):
    # opt = parser.parse_args()

# source, weights, view_img, save_txt, imgsz = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size
    
# 디렉토리
#     save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # increment run
#     (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    save_dir = Path("save")
    source = "data/images"
    weights = "weights/best.pt"
    imgsz = 640
    conf_thres = 0.25
    iou_thres = 0.45

    save_txt = False

   # 초기화
    set_logging()
    device = select_device("0") # 첫번째 gpu 사용
    half = device.type != 'cpu'  # gpu + cpu 섞어서 사용

   # 모델 로드
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    # 데이터 세팅
    vid_path, vid_writer = None, None
    save_img = True
    dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

     # 추론 실행
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # 추론
        t1 = time_synchronized()
        pred = model(img, augment = False)[0]

        # NMS 적용
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes = None, agnostic = False)
        t2 = time_synchronized()

        # 검출 값 처리
        for i, det in enumerate(pred):
            p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # Path
            save_path = str(save_dir / p.name)  # 이미지 Path
            txt_path = str(save_dir / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # 이미지 텍스트
            s += '%gx%g ' % img.shape[2:]  # 출력 스트링 값
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # 정규화
            if len(det):
                # img_size 에서 im0 사이즈로 조정
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # 결과 출력
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # 클래스 별 탐지
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # 문자열 추가

                # 결과 작성
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if opt.save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or view_img:  # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        # plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)   # 검출 상자 그리기

                        # mrz일때만 크롭
                        if names[int(cls)] == "mrz":
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                            
                            x = int(xyxy[0])
                            y = int(xyxy[1])
                            w = int(xyxy[2])
                            h = int(xyxy[3])

                            # 자른 이미지 넘파이 저장
                            img_crop = im0s[y:y+h, x:x+w]
                            
                            # 크롭 이미지 저장 -> 검출 이미지 확인용
                            cv2.imwrite(save_path, img_crop)
                           
                           # 크롭 이미지 테서텍트 검출
                            ocrToStr(img_crop, "save", p.name ,'eng')    
                            
                          
            # 추론 시간 (추론 + NMS 시간)
            # print(f'{s}Done. ({t2 - t1:.3f}s)')

detect()
