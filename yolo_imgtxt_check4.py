import os

anno_set = set()
anno_dict = dict()

path = r"/home/code1system/workspace/data/gas_test"

dir_list = os.listdir(path)


for value in dir_list:
    if value.split(".")[1] == 'txt':
        f = open(f"{path}/{value}", "r")
        n = f.readlines()
        for l in n:
            if l.split(" ")[0] == "11":
                print(value)

            anno_set.add(l.split(" ")[0])

            if l.split(" ")[0] in anno_dict:
                anno_dict[l.split(" ")[0]] = anno_dict[l.split(" ")[0]] + 1
            else:
                anno_dict[l.split(" ")[0]] = 1

        f.close()

print(anno_set)
print(anno_dict)