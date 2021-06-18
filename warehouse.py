import json

myjson = dict()
#生成格子布局坐标
start_pos = (144,206,223,285)
convert_pos = [144,206,223,285]
tu_list = list()
xi = 0
for i in range(0,5):
    convert_pos[0] = start_pos[0] + i*90
    convert_pos[2] = start_pos[2] + i*90
    for j in range(0,4):
        convert_pos[1] = start_pos[1] + j*90
        convert_pos[3] = start_pos[3] + j*90
        xi+=1
        myjson.update({str(xi):(convert_pos[0],convert_pos[1],convert_pos[2],convert_pos[3])})
        with open("cse","w+") as f :
            json.dump(myjson,f)
        print("Data Conversion ComPleted")
        print(myjson)







grids={
    "1": [144, 206, 223, 285], 
    "2": [144, 296, 223, 375], 
    "3": [144, 386, 223, 465], 
    "4": [144, 476, 223, 555], 
    "5": [234, 206, 313, 285],
    "6": [234, 296, 313, 375],
    "7": [234, 386, 313, 465], 
    "8": [234, 476, 313, 555], 
    "9": [324, 206, 403, 285], 
    "10": [324, 296, 403, 375], 
    "11": [324, 386, 403, 465], 
    "12": [324, 476, 403, 555], 
    "13": [414, 206, 493, 285], 
    "14": [414, 296, 493, 375], 
    "15": [414, 386, 493, 465], 
    "16": [414, 476, 493, 555],
    "17": [504, 206, 583, 285], 
    "18": [504, 296, 583, 375], 
    "19": [504, 386, 583, 465], 
    "20": [504, 476, 583, 555]
 }