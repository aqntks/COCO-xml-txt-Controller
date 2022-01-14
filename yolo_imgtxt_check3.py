import os


path = r"/home/code1system/workspace/data/gas_test"

dir_list = os.listdir(path)
jpg_list, xml_list, other_list, result_list = [], [], [], []

for value in dir_list:
    if value.split(".")[1].lower() == 'jpg' or value.split(".")[1].lower() == 'png' or value.split(".")[1].lower() == 'jpeg':
        jpg_list.append(value)
        result_list.append(value)
    elif value.split(".")[1].lower() == 'txt':
        xml_list.append(value)
    else:
        other_list.append(value)

print("이미지", len(jpg_list), jpg_list)
print("XML", len(xml_list), xml_list)
print("기타", len(other_list), other_list)

for ddd in jpg_list:
    for xxx in xml_list:
        if ddd.split(".")[0] == xxx.split(".")[0]:
            result_list.remove(ddd)

print("안맞음", len(result_list), result_list)

# for de in result_list:
#     os.remove(f'{path}/{de}')
#     print(de, "삭제")