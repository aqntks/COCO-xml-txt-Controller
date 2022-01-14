

import os
import random
path = r"/home/code1system/workspace/data/gas_all_no_serial/image"

dir_list = os.listdir(path)
img_list = []


f = open("gas_all_no_serial_train.txt", 'a')
vf = open("gas_all_no_serial_valid.txt", 'a')

for ddd in dir_list:
   if ddd.split('.')[1].lower() == "jpg" or ddd.split('.')[1].lower() == "png" or ddd.split('.')[1].lower() == "jpeg":
       img_list.append(ddd)

val_list = random.sample(img_list, 2282)

for val in val_list:
    img_list.remove(val)

for img in img_list:
    f.write(f'{path}/{img}\n')

for img in val_list:
    vf.write(f'{path}/{img}\n')

f.close()
vf.close()


