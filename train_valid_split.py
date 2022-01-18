

import os
import random
path = r"C:\Users\home\Desktop\car\jjj"

dir_list = os.listdir(path)
img_list = []


f = open(r"C:\Users\home\Desktop\car\car_train.txt", 'a')
vf = open(r"C:\Users\home\Desktop\car\car_valid.txt", 'a')

for ddd in dir_list:
   if ddd.split('.')[1].lower() == "jpg" or ddd.split('.')[1].lower() == "png" or ddd.split('.')[1].lower() == "jpeg":
       img_list.append(ddd)

val_list = random.sample(img_list, 700)

for val in val_list:
    img_list.remove(val)

for img in img_list:
    f.write(f'{path}/{img}\n')

for img in val_list:
    vf.write(f'{path}/{img}\n')

f.close()
vf.close()


