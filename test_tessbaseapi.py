# -*- coding: utf-8 -*-
from tesserocr import PyTessBaseAPI,RIL,iterate_level
from PIL import Image



with PyTessBaseAPI(lang='chi_sim',psm=7, oem=1) as api:
        level = RIL.TEXTLINE #以标题为主
        img = Image.open("C:\\Users\\Wrench\\Nox_share\\ImageShare\\Screenshots\\12121.png")
        api.SetImage(img)
        api.Recognize()
        ri = api.GetIterator()
        
        for r in iterate_level(ri, level):
            symbol = r.GetUTF8Text(level)  # r == ri
            conf = r.Confidence(level)
            if symbol:
                pass
                print('symbol {0}  conf: {1}'.format(symbol, conf))
            indent = False
            ci = r.GetChoiceIterator()
            boxes = r.BoundingBox(level)
            print(boxes)
            # for c in ci:
            #     if indent:
            #         print('\t\t ', end='')
            #     # print('\t- ', end='')
            #     choice = c.GetUTF8Text()  # c == ci
            #     print(u'{} conf: {}'.format(choice, c.Confidence()))
            #     indent = True
            