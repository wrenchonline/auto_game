from  utils  import *
import cv2

test = "000011000000000000000000000011000000000000000000000011000001111111110000000011000111100000000000000011101100000000000000000011111000000000000000000011110000000000000000000001000000000000000000$24$8"

items = test.split("$")
featrue = items[0]
height = int(items[1])
wight = int(items[2])
ont = hex(int(featrue,2))[2:]
onecomp = height*wight - len(hexstr_16_to_hexstr_2(ont)) #补码
featrue = featrue[:]
print(hex(int(featrue,2)))
binarry = hexstr_16_to_hexstr_2(hex(int(featrue,2))[2:])
print(len(binarry))
c = "0000"
c += binarry
binarry = c
display(binarry,8,24,"")
ns = binstr_to_nparray(binarry,8,24)
cv2.namedWindow("Image")
cv2.startWindowThread()
cv2.imshow("Image",ns)
cv2.waitKey(0) 
cv2.destroyAllWindows()