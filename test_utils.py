from  utils  import *
import cv2

test = "000000001111111100000000000000011111111111000000000001100000000001100000000001000000000000110000000011000000000000110000000011000000000000110000000011000000000000110000000001100000000001100000000000111111111111000000000000000111111000000000000000000000000000000000$24$11"
items = test.split("$")
featrue = items[0]
height = int(items[1])
wight = int(items[2])
ont = hex(int(featrue,2))[2:]
onecomp = height*wight - len(hexstr_16_to_hexstr_2(ont)) #补码
print("补码：{0} 个 0".format(onecomp))
z = "@"
for i in range(0,onecomp):
    z+="0"
#zz = featrue[:] + z
featrue = featrue[:]
print(str(hex(int(featrue,2)) + z + "$?$?$"+items[1] + "$" + items[2]))
binarry = hexstr_16_to_hexstr_2(hex(int(featrue,2))[2:])
print(len(binarry))
c = ""
for i in range (onecomp):
    c += "0"
c += binarry
binarry = c 
display(binarry,wight,height,"")
ns = binstr_to_nparray(binarry,wight,height)
cv2.namedWindow("Image")
cv2.startWindowThread()
cv2.imshow("Image",ns)
cv2.waitKey(0) 
cv2.destroyAllWindows()