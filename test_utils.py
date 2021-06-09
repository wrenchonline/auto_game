from  utils  import *
import cv2

test = "0001100000000000000000011100000000000000001111111111111110000111111111111111100000000000000000000000$20$5"

items = test.split("$")
featrue = items[0]
height = int(items[1])
wight = int(items[2])
ont = hex(int(featrue,2))[2:]
onecomp = height*wight - len(hexstr_16_to_hexstr_2(ont)) #补码
print("补码：{0}".format(onecomp))
featrue = featrue[:]
print(hex(int(featrue,2)))
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