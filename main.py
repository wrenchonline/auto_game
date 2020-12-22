# -*- coding: utf-8 -*-
from os import error

from numba.cuda.decorators import convert_types
import Robot as rb
import time
import pytesseract as pytes
from utils import *
from tesserocr import RIL
import math

'''
    while True:
        x,y = blRobot.findMultiColorInRegionFuzzy("0x202020","2|2|0x202020", 90, 52, 1131, 1024 ,1406)
        if x!=-1:
            print("posx:{0},posy:{1}".format(x,y))
            blRobot.click(x+1,y+1)
        else:
            print("not found")
'''



ditu = (
		"0007000000070000000700000007000000078000000fc0007ffffffe7fffffff7fffffff0007800e0007000e0007000e007f801c006780180067800000e7c00001c7f00001c7fc0001879e0003878700070707800e0701c01e0700e01c07007038070078780700387007001c0007001c0007000e00070006000300060000000000000000000000000000000000000000000e01c0100e03c0198e0780198e0700198e1e00198e3c00198e7800198ff80019dff80019fff80019ff99003ffe1980fffe1980fffe19c0f98e18e0198e1860198e1826198e1806198e1807198e1807198e1807198e1807198e1807198e7c0f198ffffe198e7ff8198e7c00198e1800188e1800000e1800000c100000000000000000000000000000000000000000001801e0061807c00e181f801c187e003819f80078180060e0380071e0f8003f80f8003f8018003f8018007f801800f78019ffe1e0187f00f0187f0078180f00101807800000000000000000000001c0007fffffff7ffffffe7c000078600000706000007060000070607c007871fe00787fffc0707c01f0e03800ffe0000000000000000000000000000000000000000000060006000e0006007e000e00f8001c3ff0001c7f0000387e0780701c0380e01801c1e01800e7801800ff801801fc001803f8001e0fc0001fff80000fc00000070000000000000000000000000000007ffffffe7ffffffe7ffffffe00f800000078000000380000001f0000000780000003f0000000700000003800$长寿郊外$1297$32$139",
        "001c0003180600038e0380038700e00781c0700f8070180f801c000f8004000e0000000e000000000100000001c1000000e1c0000070e00000387000001c3800000e1c0000070e00000387000003c3ffffffe1fffffff0e00000787000003c3800000e1c0000070e00000387000001c3800000e1c0000070e000003820000008000000000000000000000000000000000100000001c1ffffe0e1fffff871fffffc38e000001cf000000e7800c0073c38e0039e1c7001cf8e3800e7ff1c0073ff8e0039e3c7001cf0f3c03ff87ff03ffc3fffcffe1fffe7ff0fffe1e7879e0073c78e0039f7c7001cffe3800e7e71c0073e38e0c39e1c7061cf061838e780001c73c0000e38e0078f1c7fffff0e1fffff0607ffff0000000000000000000000000000000000000000003fff81039fffe181ce7ef0e0e61c1870630e0c3831878f1e38fffffffc7ffffffe3fffffff187861e78c3830e1c61e3870c3fffc38e1fffc0860fffe00100006000000030000000180008c70c000c6186000730f30003981fc001cc0fffffe60fffffe30ffffff186180000cf0c00007e0600003f031f801e01ff000600ff000000000000000000000000000000000000000000000003000300038001800fc001c00f8001c1ff8000e1fc0000e0fc0f00e01c0380e00c00e0f0060039e003001ff001801fc000c01fc000783f00003fff00000fc000000380000000000000000000000000000003fffffff1fffffff8fffffffc00f80000003c0000000e00000003e0000000780000001f80000001c0000000700@000$江南野外$1511$33$139",
        "0180000e0180001e0180001c0180003801800078018000f0018001e0018003c00180078001800f0001801e00018078000181f00007e7c000ffff8000ffff80007fff80000183e0000181f80001803c0001801e0001800700018003c0018001c0018000e001800070018000780180001c0180001e0180000e0100000e000000000000000000000000000000000000001c0ffffffe1fffffe03fffff80381c00003818000038180000399c63fe399c67fe399c6786399c6706399c6706399c6706799ce706799ce706fb9fe706ffffff06ffffff067fffe7063f9fe706399ee706399c6706399c6706399c6706399c6706399ce706399fe78639ffe7fe39ffc3fe38ff81fc381c00001008000000000000000000000000000000000000000000007ffffffe7ffffffe7ffffffe600000066000000660000086638001c6638101c6678381c6678381c6678381c6678381c6678381c6678781c667ffffc667ffffc667ffffc6678781c6678381c6678381c66783f1c66783f9c6638399c6638389c6630101c66000008660000006600001867ffffffe7ffffffe3ffffffc000000000000000000000000000000000000000000e0007001e000607fffffe07fffffe07fffffc001e0078000c00787000000070000000700c0000639e7fe0639e7fe0e39fffe1e39ffe79c3ffe67f83ffe67e03ffe67e079fe6700f9fe660079fe678079fe67f039fe67fc3ffe67fe3ffe67063ffe660739ffe60739fffe0739e7fe0739e7fc0600c0001e0000007e$大唐国境$1767$32$139",
        "0180000e0180001e0180001c0180003801800078018000f0018001e0018003c00180078001800f0001801e00018078000181f00007e7c000ffff8000ffff80007fff800001c3e0000181f80001803c0001801e0001800700018003c0018001c0018000e001800070018000780180001c0180001e0180000e0100000e000000000000000000000000000000000000001c0ffffffe1fffffe03fffff80381c00003818000038180000399c63fe399c67fe399c6786399c6706399c6706399c6706799ce706799ce706fb9fe706ffffff06ffffff067fffe7063f9fe706399ee706399c6706399c6706399c6706399c6706399ce706399fe78639ffe7fe39ffc3fe38ff81fc381c000010080000000000000000000000000000000000000000000000e0007001e000e07fffffe07fffffe03fffffc001e0078000c00307000000070000000700c0040639e7fe0639e7fe0e39fffe1e39ffe7bc3ffe67f83ffe67e03ffe67c079fe6700f9fe660079fe678079fe67f039fe67fc3ffe67fe3ffe67063ffe660639ffe60738fffe0738e7fe0730e7fc0600c0001e0000003e000000000000000000000000000000000000000000060006000e0006007e000e00f8001c3ff0001c7f0000387e0780701c0380e01801c1e01800e7801800ff801801fc001803f8001e0fc0001fff80000fc00000070000000000000000000000000000007ffffffe7ffffffe7ffffffe00f800000078000000380000001f0000000780000003f0000000700000003800$大唐境外$1531$32$139",
        "000002000000e38180007380c7f3ff8063ffff8231ffff0398c7ff01cc63ff80e63fffc0731fffe0398ffff81cc67ffffe631ffcf7318ffe1f98ffff0ffc7fff87fe3fffc3ff1fffe0ff8cfff01cc63ffc0e633fffc731ffffff98ffff01cc7fff80e631ffc07318ffe0398ffff81cc7ffff0661f03fc030f00e781800071c0c000104020000000000000000000000000000000000380000007e06187878030c383801861c1c01c70c0e61c3860730e387039861c701cc30c380e670e180733861c039f871c71cfc70c38e7e70e1df3ff0c0ff9ff86077ce7cf079e61ff8787303fff83981fff81cc0ff800e607f80073038e00398187801cc1c0e00e61c0780700e00e0380600781c02001c0fc0000703f0000381f80000c0000000000000000000000000000000000000038000e007c0007007c000780fc0003c0f00001e7f80001fffe001ffffffff3ffffffe01e7f00000f07c0000301e0000000380000001c00000000000010000000180000001e3800100f0f001c0383f00e01c03c0300e00f8180700000c0380000701c0000381e00001c0f00001cfffffffe3ffffffc03f0000000f00000003000000$墨家村$1342$33$104",
        "0067003800f3801c00f1c01e01f0e00e03f0700e03f8380f01f81c07000c0e070006070780030383800181c78000c0f38000607fc0007c3ff001fffffff9fffffffeffffffff0383fc000181fe0000c0f380006070e00030383800181c1e000c0e0700060701c0030380f00181c03800c0e00e0060700780003801c0000c006000000000000000000000000000000000000000000001e00060ffe00030fff006380070071c00187f9c000c3fce000e3fe607ff3fff0fff9fff80f3ffff8071ffff1838ffff0e187e7f870c3f3fc3c61f1fffc0000fffe000067fe7fe073c03ffc39c0038f38e00183986000c1cc3300606019c030300c6018183e181c0c1f0c0c0e0787060f01e1800f0078e00f800c3007800408000000000000000000000000000000000000000007ffffffe3fffffff1fffffff8c000000c600000063000004318e000718c702038c678381c633c1c0e319e0e0718cf07038c678381c633c3c0e319fffff18cfffff8c67ffffc633c3c0e319e0e0718cf07038c6383f1c631c1fce318e0e6718c707138c630101c630000043180000018c000038c7ffffffe3fffffff0fffffff@000$朱紫国$1309$33$103",
        "0000007f1ffffffe3fffffc07fffff807beffff879e7fffe7fff8706ffff8606f9c78606f18386067ffffffe7ffffffe79c7860671c7860671ff060620ff060000000200080002001c0006033ffffe0f7ffffe3e7ffffefc1c71c67818718660187186001c7186001c71c6001e79c6703ffffe787ffffe1e1c00060e18000206000000000000000000000000000000000000003f3fffffff7fcfffe07f87ff807ffffffc7fffdffeffff8606ff8786067fff86067ffffffe7fc7fffe61879ffe61ff060661ff0606009e0706000e0786010e0f86639fff867b98f1dc3b9861f803e07ff003e07fe00ff83fc0fffc3f803ffc3ff00ff03ff81ff878781ff878383f98fcfc7999ffff018c787801003038000000000000000000000000000000000000000003fffff803fffffc03fffffe0000000e0000000600000006000000060000000600000006000000060000000600000006000000060000001e7ffffffe7ffffffe7ffffffe0000000e0000000600000006000000060000000600000006000000060000000600000006000000060000001e03fffffe03fffffc01fffff8$麒麟山$1429$32$104",
        "18001c000c001e0006001e0003001f0001803fc000c07ffff8e1fffffdfce00000ffe000001e0000000e00000003000180018001c000c000e0006000700030007e00187ffffe0c1fffff06007e078f803c00cff00e0073f00e0039f007001c3007000c180700060c0380030603800183008001c180000fe0c0000fe0400007e0000000000000000000000000000000000000000080000380e00001c070ffe0e070fff870307ffe381831c71c1c18e18e1c0c70c70c0638638e031c31c6018e18e600c70c7f0063863f803befffe01fffffffefffffffe7fffffc031c73fc018e18fe00c70c7300638639c031c31c6018618e380c30c70e06386387833ef1c1c1fff0e0e07ff070381ff0381e00001c0f0000040300000000000000000000000000000000000000000003fffff801fffffe00ffffff80000001c00000006000000030000000180000000c00000006000000030000000180000000c000000060000000f1fffffff8fffffffc7ffffffe000000070000000180000000c00000006000000030000000180000000c00000006000000030000000180000003c03fffffe01fffffe007ffffe@000$花果山$1052$33$103",
        "0300000000c0000200300001c00c0000700300e03800c0781c00307f0e000fffc70003fff3c001fc3cc001fe0f0031fc03c00c7f00f00380c03c00e0300f00380c03c00e0301f80f80c3ffffc030ffffe00c03c0000300f00000c03c0000300f00000c03c0000300f1c000c03c3800300f0f000c03c1e00300603c00c0000700300000c000000000000000000000000000000000000000000c203c000f0c07000f0380e01fc070181f001c02078000000000000c0200000701c00003c0f3f001e03ffc01f03fff01f1ffc0c07c7ff0300f3c3c0c03cf070300f381c0c03ce0fc300f3c3f8cc3cfcff338f3ffccce3cfff133cf38fc0cf3ce1f033cf383c0ff3ce0f03f8f383e1fc3cf0ffff0f3ffffe03c7ffc3006003c0c0180060100000000000000000000000000000000000000400000303c000f8e07000f83c0e03fc070383f000c063f80000000000000000000000000000038c7e3061c33f8c3fe0cfe30f0033f8c3c00cce30f003338c3ff8cce30fff7338e3fffcce39f003338efc00cce39f003338e3c00cce38f003338e3fffcce38ffe3338e3c00cce38f003338e3c00cce38f003f3cc1fe0fcff001c0e1f80038003c@00$东海湾$1198$34$103",
        "00010000000f0000003f800000fffffe1fffffffff81c000fe0000001c0100061801800f1c61803e1c6187fc1c61ffe01ee3ff803fff9e00ffff8e073fff8e071ee38e071e618f3e1c6187fe1803800408070000007e000600fe001e07ff003e7fffc07c3e03f8f00e01ffe006007fe006003fe00701f87007fff07c07f8001e0700000e000000000000000000000000000000000000000c0001801c00018018180180181c0180381c0180701f8180e01fe181e01c7981c0187f838018018700180186001801fc001c01fc003e03fe007ffffffe7ffffffe7ffffffe1c01fe001801fc001801ce0018018700180183801c3f81c01e7981c01ff180e01f8180701e0180381c018018080180180001801c0000800c00000000000000000000000000000000000000007ffffffe7ffffffe7ffffffe600000066000000660000086638001c6638101c6678381c6678381c6678381c6678381c6678381c6678781c667ffffc667ffffc667ffffc6678781c6638381c6638381c66383f1c66383f9c6638399c6638389c6630101c66000008660000006600001c67ffffffe7ffffffe3ffffffc$傲来国$1286$32$105",
        "2060000078e038061fe070071fe070063ffffc3e7ffffffcf801ffc0f000fe00001ffe0007fffc0003fff80003fff01f03fffe7c3ffffff8ffffff80ffffff006000000060000000603ffff060fffff860e0000061e000007bf000007ffffffe7ffffffe7ffffffe71e0003861e0001860e0007860fffff8607ffff0207fffe00000000000000000000000000000000000000000600f038060ff838067ff87806001870060018706600187066001860760078607607f86077fff80077fffc01e3c01fffe0000fffc0f0000000fc000001fe000001e1ffff81c1ffffc181ffffe180070061800600638006006f800e0067800c0063801c00618038006180780061c07000e1e06003e1fc001fc0fc001f8000000000000000000000000000000000000000007fffff00000fff00000007803fffff87ffffff87ffffff87ffffff8000000780000007803fffff807fffff001e0000001c000000180000003806000070060000e0060e01c0060603800607070006070e0606078e0706078e038607c701860fe381861fe1c0063870e00678307007e0003807e000180700001c00000$狮驼岭$1261$32$104",
)

tu_text_features = ['图','T']
shop_emty = (727,651,"0x3f4a53"),(663,644,"0x3f4a53"),(623,645,"0x3f4a53"),(720,616,"0x3f4a53"),(718,683,"0x3f4a53"),(797,679,"0x3f4a53"),(855,675,"0x3f4a53"),(852,637,"0x3f4a53")
tu_money = 27999

feixingfu_jiemian = (1309,382, '0x0c5a9b'),(839,272, '0x1064a7'),(689,370, '0x1367a9'),(814,536, '0x166baa'),(927,669, '0x1160a0'),(1138,597, '0x196ca6'),(1432,674, '0x0c4e95'),(755,423, '0xe879aa'),(1165,550, '0xf0ce08'),(770,292, '0xebf200')
zhujiemian = (667,1015,'0xefc250'),(782,1024,'0xd89825'),(907,1022,'0xea8f4f'),(1022,1017,'0xf8cf48'),(1124,1020,'0xb75715')
fanhui = (1600,80, '0x183850'),(1586,67, '0x204057'),(1585,97, '0x18324a'),(1617,65, '0x183a4f'),(1616,95, '0x18324c'),(1620,82, '0x305b80'),(1603,63, '0x497fa3'),(1586,81, '0x305c80'),(1600,95, '0x32638c'),(1601,83,'0x183850')
ditujiemian = (253, 74, '0x20a9c0'),(219, 75,'0x37cddf'),(266, 61, '0xab5694'),(264, 90, '0xa5558d')
start_map = (143,79)




Table_梦幻 = {
	"无名鬼蜮":{ "坐标计算":(712,304,1445,855,192,144),"返回":(1473,195)},
	"大唐国境":{ "坐标计算" : (624,146,1533,1013,352,336), "返回" :(1560,37)},
    "长安城":{ "坐标计算" :(266,187,1653,892,550,280),"返回" :(1674,86) },
	"地府" : { "坐标计算" : (596,218,1561,941,160,120), "返回" : (1588,108) },
	"地狱迷宫一层"  : { "坐标计算" : (608,226,1551,933,120,90), "返回" : (1578, 115) },
	"地狱迷宫二层" : { "坐标计算" : (604,222,1555,935,120,90), "返回" : (1582, 114) },
	"地狱迷宫三层" : { "坐标计算" : (598,218,1561,939,120,90), "返回" : (1590, 110) },
	"地狱迷宫四层" : { "坐标计算" : (598,218,1559,939,120,90), "返回" : (1584, 111) },
	"花果山" : {"坐标计算" : (611,227,1546,932,160,120),"返回" : (1571,120)},
    "北俱芦洲": {"坐标计算":(604,218,1554,938,228,170),"返回" :(1579,118)},
	"女娲神迹" : {"坐标计算": (609,226,1550,932,192,144), "返回" :(1583,128)},
	"大雁塔六层":{"坐标计算":(296,169,1623,908,138,77),"返回":(1647,68)},
	"大唐境外" : {"坐标计算":(187,392,1727,684,640,120), "返回":(1753,296)},
    "墨家村" : { "坐标计算" :(849,177,1310,982,96,168), "返回" :(1329,77)},
	"狮驼岭" : { "坐标计算" :(598,216,1558,938,132,99), "返回":(1575,117)},
	"普陀山" : { "坐标计算" :(605,223,1553,935,96,72), "返回" :(1577,120)},
	"五庄观" : { "坐标计算" :(605,223,1552,934,100,75), "返回":(1570,114)},
	"女儿村" : { "坐标计算" :(800,266,1358,892,128,144), "返回" :(1386,162)},
	"东海湾" : { "坐标计算" :(727,227,1432,932,120,120), "返回":(1454,123)},
	"建邺城" : { "坐标计算" :(250,185,1669,894,288,144), "返回" :(1702,81)},
	"傲来国" : { "坐标计算" :(431,183,1486,894,224,151), "返回":(1512,77)},
	"朱紫国" : { "坐标计算" :(382,175,1537,901,192,120), "返回":(1565,72)},
	"江南野外" : { "坐标计算":(601,221,1556,938,160,120), "返回":(1582,118)},
	"长寿郊外" : { "坐标计算":(677,227,1480,930,192,168), "返回" :(1505,124)},
	"长寿村" : { "坐标计算" :(797,210,1362,950,160,210), "返回":(1400,101)},
	"麒麟山" : { "坐标计算" :(597,227,1561,930,191,143), "返回":(1586,127)},
}

#(727,78,1430,1000,160,210)

map_feature = {
	"装备收购商" : { "坐标":((800,501,0xe2d132),(812,496,0xdccc32),(801,491,0xdfce32),(800,497,0xbfb830),(800,501,0xe2d132),(798,503,0xd1c02e),(812,506,0xe3d132),(804,513,0xdcca31),(797,515,0x242a0e),(790,514,0xd4c731)), "范围参数":(90,514,216,1162,712)},
	"长寿村": {"坐标":((1158,901,0x000cf8),(1206,900,0x000cf8),(1246,901,0x0611f8 ),(1290,901,0x0612f8)),"范围参数":(90,1175,926,1226,974)},
	"朱紫国":{"坐标":((511,224,0xeef6f0),(521,223,0x4a68f0),(521,227,0x2e50f0),(519,232,0x0028f0),(513,232,0x0028f0),(506,233,0x0f35f0),(503,229,0xa5b7f0),(511,224,0xeef6f0),(512,230,0x0028f0),(514,223,0x0028f0)), "范围参数": (90,485,204,528,252)},
	"傲来国":{"坐标":((532,379,0x0f1ef8),(544,379,0x0010f8),(544,390,0x1322f8),(534,390,0xd8ddf8),(544,391,0x0e1df8),(546,378,0x1b2af8),(544,387,0x0e1df8),(537,390,0xd8ddf8),(542,390,0x0010f8),(545,390,0x7e88f8)),"范围参数": (90,501,352,563,417)},
	"长安城A":{"坐标":((994,714,0xbab4ab),(994,719,0xbab4ab),(996,723,0x664b44),(1006,714,0x7c675f),(1010,714,0x684e46),(1005,721,0x442018),(1004,724,0x7d6860),(999,728,0xdfe3db)),"范围参数":(90,946,676,1099,779)},
	"选择我要做的事情":{"坐标":((1600,640,0xd2d9dd),(1602,636,0x597081),(1612,632,0x385468),(1614,634,0x798c9a),(1601,654,0x698392),(1589,654,0xbbc6cd),(1615,669,0x305068),(1635,653,0xbdc8ce),(1644,649,0x305468),(1653,638,0x385468)),"范围参数":(90,1358,565,1870,719)},
	"颜如玉": { "坐标":((699,296,0xd7cb40),(699,302,0xd8c732),(699,309,0xcdbe31),(706,309,0xe6d537),(710,309,0xdfcf37),(717,309,0xe2d032),(717,300,0xe2d032),(711,294,0xcebf2f)),"范围参数":(90,355,5,1334,728)},
	"长安城": { "坐标":((1478,610,0x6b524a),(1486,613,0xb3aca4),(1494,614,0x371103),(1480,622,0x6d554d),(1476,623,0x6e564e),(1491,620,0xd7d9d1),(1498,616,0x8e7e73),(1492,614,0xb4ada5),(1494,615,0x381304)),"范围参数":(90,1327,506,1576,688)},
	"大唐国境" : { "坐标": (( 174, 47, 0x020202),( 223, 52, 0x020202),( 247, 52, 0x020202),( 287, 48, 0x0c0c0e),( 306, 52, 0xb0b9d0),( 162, 53, 0xb1b8d0),( 175, 65, 0xa1acc8),( 184, 52, 0xb1b8d0),( 213, 66, 0xa8b0d0),( 213, 62, 0x080809)),"范围参数":(90,143,30,331,76)},
	"地府" : { "坐标": (( 196, 51, 0x020202),( 220, 45, 0x050505),( 217, 52, 0xb0b8d0),( 217, 65, 0xa8b0d0),( 256, 50, 0x020202),( 247, 60, 0x0b0c0d),( 250, 55, 0xb0b8d0),( 231, 62, 0x020202),( 244, 42, 0x020202),( 211, 48, 0x030304)),"范围参数":(90,143,30,331,76)},
	"地狱迷宫一层" : { "坐标": (( 685, 400, 0xf00000),( 718, 401, 0xf00000),( 766, 411, 0xf00000),( 815, 398, 0xf00c0c),( 725, 851, 0x0000f0),( 761, 843, 0x0000f0),( 802, 834, 0x0000f0),( 849, 837, 0x0202f0),( 860, 849, 0x0000f0),( 904, 847, 0x0000f0)),"范围参数":(90,606,333,945,888)},
	"地狱迷宫二层" : { "坐标": (( 1488, 318, 0x1212f0),( 1521, 322, 0x1212f0),( 1470, 613, 0x0000f0),( 1522, 630, 0x0000f0),( 1438, 888, 0x0000f0),( 1536, 870, 0x0000f0),( 1303, 631, 0x0000f0),( 1304, 314, 0x0000f0),( 1391, 316, 0x0000f0),( 1386, 621, 0x0000f0)),"范围参数":(90,1259,282,1551,903)},
	"地狱迷宫三层" : { "坐标": (( 748, 397, 0x0000f0),( 744, 623, 0x0000f0),( 842, 628, 0x0000f0),( 845, 403, 0x0000f0),( 1424, 908, 0x0000f0),( 1532, 894, 0x0000f0),( 1393, 896, 0x0000f0),( 1298, 900, 0x0000f0),( 644, 400, 0x0000f0),( 793, 409, 0x0000f0)),"范围参数":(90,614,364,1552,923)},
	"地狱迷宫四层" : { "坐标": (( 799, 254, 0x0505f0),( 848, 271, 0x0000f0),( 893, 266, 0x0708f0),( 1214, 446, 0x0000f0),( 1276, 458, 0x0000f0),( 1301, 449, 0x0000f0),( 1277, 454, 0x0000f0),( 1361, 441, 0x091df4),( 1301, 445, 0x0202f0),( 1323, 456, 0x0202f0)),"范围参数":(90,612,235,1387,475)},
	"千年怨鬼" : {"坐标":(( 765, 572, 0xebd834),( 803, 593, 0xebd834),( 850, 575, 0xe9d634),( 826, 575, 0xebd834),( 886, 581, 0xe8d633),( 871, 588, 0xebd834),( 840, 599, 0xd8c730),( 802, 593, 0xead734),( 765, 583, 0xebd834),( 765, 586, 0xe0ce32)),"范围参数":(90,553,305,1303,820)},
	"进入无名鬼蜮" : { "坐标": (( 1443, 480, 0xfdfdfe),( 1460, 621, 0xffffff),( 1703, 617, 0xfafbfb),( 1708, 482, 0xffffff),( 1695, 410, 0xffffff),( 1696, 422, 0xfbfbfb),( 1717, 406, 0x081317),( 1697, 529, 0x305068),( 1707, 687, 0x305060),( 1591, 524, 0x305468)),"范围参数":(90,1402,377,1729,709)},
	"无名鬼蜮" : { "坐标": (( 171, 53, 0x020202),( 213, 64, 0xa8b0d0),( 245, 50, 0x030304),( 291, 63, 0x1d1f23),( 268, 50, 0x020202),( 217, 59, 0x060607),( 165, 66, 0x090a0b),( 167, 42, 0x09090a),( 209, 48, 0xb0b8d0),( 279, 59, 0xa7afcb)),"范围参数":(90,143,30,331,76)},
	"传送女娲": { "坐标":((566,525,0xe5d973),(560,525,0xe3d669),(569,527,0xafa027),(566,531,0xdecc31),(561,535,0xbaab2a),(551,535,0xcbbb2d),(551,547,0xd1c131),(562,550,0x9d9023),(573,548,0xe0d152),(574,544,0xead836)),"范围参数":(90,335,217,968,701)},
	"花果山土地" : { "坐标":((804,486,0xebd834),(807,493,0xa89b25),(807,497,0xd0c533),(807,499,0xd6c530),(799,499,0xcbbb2d),(799,497,0xd1c433),(793,497,0xdcde41),(797,498,0xe1cf32),(799,499,0xcbbb2d)),"范围参数":(90,212,106,1720,885)},
	"请送我进去" : { "坐标": ((1470,358,0x435d70),(1491,358,0x9facb6),(1452,373,0xeef0f2),(1522,373,0xe1e5e9),(1551,371,0x385468),(1592,365,0x385468),(1594,369,0x748795)),"范围参数":(90,1404,312,1880,438)},
	"是的" :{ "坐标":((1529,499,0x385468),(1586,498,0xf5f6f7),(1574,506,0xc8d0d5),(1565,511,0xa3b0b9),(1607,518,0x8da1ac),(1637,512,0xadb9c1),(1641,506,0x385468),(1565,497,0xe3e7e9),(1489,499,0x8495a2)),"范围参数":(90,1410,449,1872,581)},
	"北俱芦洲" :{"坐标":((182,50,0x070808),(179,50,0x2e3036),(178,51,0x0a0a0b),(172,65,0x6d7588),(173,65,0x97a2bd),(177,65,0x0e0e11),(168,55,0x5d616e),(178,56,0x303238),(187,69,0x050606)),"范围参数":(90,143,30,331,76)},
	"花果山" :{"坐标":((195,56,0x131417),(208,44,0x43464f),(188,52,0xb0b8d0),(186,52,0x717685),(181,59,0x080809),(199,57,0x17181b),(195,66,0x23252b)),"范围参数":(90,143,30,331,76)},
	"女娲神迹" :{"坐标":((196,48,0x35383f),(208,50,0x747a89),(208,60,0x060607),(205,62,0x9aa1b7),(223,69,0x090a0b),(223,56,0x070708),(223,53,0x4e515c),(214,52,0x757a8a)),"范围参数":(90,143,30,331,76)},
	"我要做其他事情": {"坐标":((1460,499,0x385468),(1469,502,0x607686),(1459,508,0x6c808f),(1450,511,0x718593),(1447,516,0xadbbc2),(1439,517,0xdce2e5),(1451,522,0x4a6a7b),(1461,520,0xfcfdfd),(1460,505,0xe5e8eb),(1446,501,0x6f8492)),"范围参数":(90,1406,447,1869,579)},
	"驿站老板": {"坐标":((1181,415,0xc4bd45),(1187,415,0x8d8426),(1188,407,0xebd836),(1194,405,0xb0a227),(1177,420,0xdac931),(1169,420,0xe5d434),(1170,403,0xcdbd41),(1171,424,0x5e5a1a),(1212,415,0xe6d53e),(1216,408,0xe7d740)),"范围参数":(90,644,4,1576,662)},
	"打工": {"坐标":((567,917,0x9fafb9),(573,912,0xdbe0e4),(579,912,0x94a5ad),(580,918,0x8b9faa),(575,928,0xffffff),(590,929,0xfbfcfc),(591,921,0xbfc9ce),(594,930,0xfdfefe),(582,938,0x637984)),"范围参数":(90,416,889,904,966)},
	"体力不足": {"坐标":((184,810,0x182c38),(201,811,0x253844),(201,811,0x253844),(197,811,0xfdfdfd),(194,826,0x6e7b82),(196,826,0xffffff),(194,836,0x6e7b82),(194,836,0x6e7b82),(210,823,0xd8dbdd),(181,825,0xf4f5f6)),"范围参数":(90,1,684,512,917)},
	"大雁塔六层" :{"坐标":((864,569,0xbeae66),(861,572,0xb8a45e),(848,561,0x917c32),(878,560,0xb6a556)),"范围参数":(90,753,436,1180,706)},
	"火焰山土地" :{ "坐标":((1115,361,0xa99a27),(1114,363,0xc9b92c),(1117,371,0x4a4311),(1118,375,0x90672b),(1127,373,0x978a22),(1133,373,0xe5cb35),(1127,363,0xdbc931),(1124,363,0xd8c233),(1118,368,0x9e9123),(1118,375,0x90672b)),"范围参数":(90,884,50,1494,637)},
	"送我进墨家村" : {"坐标":((1560,356,0xf6f7f8),(1571,354,0xeaedef),(1574,354,0xeaedef),(1577,356,0xd8dde1),(1572,364,0xffffff),(1563,364,0xf2f4f5),(1573,365,0xffffff),(1579,365,0xf7f8f9),(1581,362,0xf3f5f6),(1582,357,0xc0c9cf)),"范围参数":(90,1415,316,1868,434)},
	"传送仙女":{ "坐标":((695,564,0x686619),(695,572,0x878723),(698,578,0xe4d533),(700,579,0xe6d433),(690,582,0xead637),(689,572,0xabb540),(690,560,0xb0a82b),(705,566,0x32350f),(704,576,0xe3d434),(706,585,0xe8d534)),"范围参数":(85,494,128,1116,808)},
	"我要去": {"坐标": ((1603,507,0x9eacb5),(1602,500,0xd6dce0),(1607,499,0xe0e4e8),(1616,498,0xc5cdd3),(1621,506,0x7f919e),(1609,513,0xf9fafb),(1604,516,0xffffff),(1615,523,0xffffff),(1621,512,0x8495a1),(1611,498,0x8797a4)),"范围参数":(90,1425,459,1791,567)},
	"大唐境外A":{"坐标": ((1384,406,0xe7ece4),(1381,427,0xf85555),(1388,423,0xf80000),(1391,422,0xf8bdba),(1396,422,0xf8d4d1),(1398,412,0xf88381),(1397,405,0x94967c),(1394,402,0x8f946c),(1380,404,0x36452d),(1387,417,0xf8e2df)),"范围参数":(90,1371,382,1548,480)},
	"驿站老板A":{ "坐标": ((913,649,0xdfcd31),(916,643,0xa49727),(909,640,0xc7d078),(906,647,0xc9b690),(907,650,0xdfcc51),(915,651,0xdbc933),(915,651,0xdbc933),(914,658,0xebd834),(913,665,0xe7d433),(901,664,0xe5d233)),"范围参数":(90,638,237,1335,867)},
	"大唐境外":{"坐标": ((174,50,0x020202),(180,57,0x858b9d),(197,55,0x080809),(240,50,0x474a54),(255,51,0x202226),(275,43,0x32353b),(284,43,0x858b9e),(267,70,0x2a2e37),(288,69,0x0e0f12),(294,55,0x24262b)),"范围参数":(90,143,30,331,76)},
	"超级巫医":{ "坐标": ((770,613,0xcbba2d),(774,609,0xd8c730),(785,616,0xbbac2a),(783,614,0xebd834),(783,602,0xe0ce32),(789,621,0xe0ce32),(795,612,0xebd834),(739,617,0xe6d433),(750,629,0xd3c32f),(771,611,0xe6d433)),"范围参数":(90,548,249,1136,812)},
    "超级巫医A":{ "坐标": ((770,613,0xcbba2d),(774,609,0xd8c730),(785,616,0xbbac2a),(783,614,0xebd834),(783,602,0xe0ce32),(789,621,0xe0ce32),(795,612,0xebd834),(739,617,0xe6d433),(750,629,0xd3c32f),(771,611,0xe6d433)),"范围参数":(90,350,3,1397,820)},
    "提示框":{"坐标": ((568,58,0xf0f427),(570,51,0xf8f830),(568,78,0xe8eb00),(549,59,0xf0f22f),(584,59,0xf0f423),(581,52,0x385157),(565,53,0xa3ad54),(565,64,0x9da830),(574,64,0x304549),(574,66,0x304850)),"范围参数":(90,0,0,1920,1080)},
}




class action(rb.Robot):

    def __init__(self,class_name="subWin",title_name="sub",zoom_count=1.5):
        rb.Robot.__init__(self,class_name=class_name,title_name=title_name,zoom_count=zoom_count)
        self.Get_GameHwnd()
        self.cx = None
        self.error = list()
        
    def find_map_by_shop(self):
        tpl = self.Print_screen()
        start_pos = [285,196,532,244] #第一个摊位
        conversion = [285,196,532,244]
        #self.show(tpl)
        tu_shop = list()
        xret = list()
        jump = False
        xret.clear()
        for i in range(0,5):
            if jump:
                break
            conversion[1] = start_pos[1] + i*144
            conversion[3] = start_pos[3] + i*144
            for j in range(0,4):
                conversion[0] = start_pos[0] + j*341
                conversion[2] = start_pos[2] + j*341
                #print("conversion{0}".format(conversion))
                e_shop_emty = self.findMultiColorInRegionFuzzyByTable(shop_emty,90,conversion[0],conversion[1],conversion[2],conversion[3])                
                if e_shop_emty[0] == State.OK:
                    print("发现空摊位")
                    jump = True
                    break
                tu_shop = self.tsOcrText(tpl,tu_text_features,conversion[0],conversion[1],conversion[2],conversion[3]) 
                if len(tu_shop):
                    print("ret:{0}".format(tu_shop))
                    xret.append(tu_shop[0])
        return xret
    
    def buy_map(self):
        #点击系统界面
        self.click(673,1025)
        time.sleep(2)
        self.click(1260,729)
        time.sleep(2)
        tpl = self.Print_screen()
        max_page = int(self.OcrText(tpl,1411, 921, 1447, 962,config=('--oem 1 -l chi_sim --psm 7 '))[0][0])
        print(max_page)
        for i in range(1,max_page+1):
          shop_pos_list = self.find_map_by_shop()
          if len(shop_pos_list):
             print("发现摊位坐标:{0}".format(shop_pos_list))
             for j in shop_pos_list:
                x = j[1]
                y = j[2]
                print("点击摊位坐标:({0},{1})".format(x,y))
                self.click(x,y)
                time.sleep(2)
                self.click(1700,82)
                time.sleep(2)
          if i >= max_page:
                continue
          else:
                print("点击下一页")   
                self.click(1549,937) 
                time.sleep(2)
                
    
    def run_with_callback(self,fun,fun_param,pre_fun1,fun1_param,post_fun2,fun2_param):
        try:
            print("start pre_fun1")
            ret = pre_fun1(fun_param)
            ret = fun(ret,fun1_param)
            ret = post_fun2(ret,fun2_param)
            self.cx = ret
        except Exception as identifier:
            self.error.append(identifier)
    '''
    在各主城增加了仓库管理员NPC，坐标分别为：长安城（346，244）、长安城（224，141）、建邺城（54，32)、傲来国（143，101）、长寿村（111，62）、朱紫国（126，90）
    '''
    #check_map 打开道具栏遍历宝图
    def check_map(self):
        n,nn,nnn,nnnn=None,None,None,None
        #打开道具栏
        self.click(1695,1015)
        time.sleep(1)
        tpl = self.Print_screen()
        target = cv2.imread("./images/tu.png")
        start_pos = (902,269,1013,378)
        convert_pos = [902,269,1013,378]
        tu_list = list()
        for i in range(0,5):
            time.sleep(0.5)
            convert_pos[0] = start_pos[0] + i*134
            convert_pos[2] = start_pos[2] + i*134
            for j in range(0,4):
                time.sleep(0.5)
                print(j)
                convert_pos[1] = start_pos[1] + j*134
                convert_pos[3] = start_pos[3] + j*134
                self.click(convert_pos[0]+5,convert_pos[1]+5)
                time.sleep(0.5)
                tpl = self.Print_screen()
                #self.show(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]])
                x,y = self.matchTemplate(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]],target,0.15)
                if x != -1:
                    print("找到宝图")
                    data = self.x_Ocrtext(ditu,"00E804,011805#03DC07,032006#08DD0B,072009",444,506,589,560)
                    print(data)
                    if data:
                        if len(data)>3:
                            pos = self.Ocrtext("06BE0B,06420B#00E804,011805#03DC07,032006#08DD0B,072009",
                                               591,511,732,547,ril=RIL.TEXTLINE,
                                               lang='eng',oem=1,
                                               attribute=["tessedit_char_whitelist", 
                                                "0123456789,"])
                            print(pos)
                            
                            _x = int(pos['text'].split(',')[0])
                            _y = int(pos['text'].split(',')[1])
                            tu_list.append((data,_x,_y))
                        else:
                            pos = self.Ocrtext("06BE0B,06420B#03E105,031E05#00E804,011805#03DC07,032006#08DD0B,072009"
                                               ,555,513,693,548,ril=RIL.TEXTLINE,
                                               lang='eng',oem=1,
                                               attribute=["tessedit_char_whitelist",
                                                "0123456789,"])
                            print(pos)
                            _x = int(pos['text'].split(',')[0])
                            _y = int(pos['text'].split(',')[1])
                            tu_list.append((data,_x,_y))
        return  tu_list  
    
    
    def go_to_CSC(self):
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(feixingfu_jiemian)
            if status==status.OK:
                time.sleep(0.7)
                self.click(762,309)
                time.sleep(0.7)
                break
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
            time.sleep(0.5)
            if status==status.NOTMATCH:
                print("前往长寿村")
                status,ag= self.findMultiColorInRegionFuzzyByTable(fanhui)
                if status==status.OK:
                    self.click(ag[0],ag[1])
                time.sleep(0.5)
            elif status==status.OK:
                print("抵达长寿村")
                break
        return True
    #TAPP 计算坐标
    def TAPP(self,D,xx,yy):
        rx = Table_梦幻[D]["坐标计算"][0] +  (((Table_梦幻[D]["坐标计算"][2] - Table_梦幻[D]["坐标计算"][0]) / Table_梦幻[D]["坐标计算"][4]) * xx+0)
        ry = Table_梦幻[D]["坐标计算"][3] - (((Table_梦幻[D]["坐标计算"][3] - Table_梦幻[D]["坐标计算"][1]) / Table_梦幻[D]["坐标计算"][5]) * yy+0)
        _min,_max = math.modf(rx)
        if _min>=0.5:
            rx = _max+1
        else:
            rx = _max                                                                                                                                                                                                                        
        _miny,_maxy = math.modf(ry) 
        if _miny>=0.5:
            ry = _maxy+1
        else:
            ry = _maxy
        return rx,ry
        
    def rgb_array(self,table_name):
        ddegree = table_name["范围参数"][0]
        x1 = table_name["范围参数"][1]
        y1 =  table_name["范围参数"][2]
        x2 =  table_name["范围参数"][3]
        y2 =  table_name["范围参数"][4]
        status,ag= self.findMultiColorInRegionFuzzyByTable(table_name["坐标"],ddegree,x1,y1,x2,y2)
        if status==status.OK:
            return status.OK
        else:
            return status.NOTMATCH
        
    #前往长寿郊外
    def go_to_CSJW(self):
        ok = self.go_to_CSC()
        if ok:
            pass
    def tap_(self,D,X,Y):
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
            if status==status.NOTMATCH:
                x,y=self.TAPP(D,X,Y)
                self.click(x,y)
                time.sleep(1)
                self.click(Table_梦幻[D]["返回"][0],Table_梦幻[D]["返回"][1])
                time.sleep(2)
                break
        print("监控坐标")
        while True:
            pos = self.Ocrtext("B5C1C5,4B3F3A",160, 90, 306, 125,
                                lang='eng',oem=1,
                                attribute=["tessedit_char_whitelist", 
                                "0123456789,"],THRESH_GAUSSIAN=False)
            if len(pos):
                postr = pos[0]['text'].replace("\n","")
                _x = int(postr.split(',')[0])
                _y = int(postr.split(',')[1])
                time.sleep(1)
                print("当前坐标(x:{0},y:{1})----实际坐标(x:{2},y:{3})".format(str(_x),str(_y),str(X),str(Y)))
                if (abs(X-_x)<3) and (abs(Y-_y)<3):
                    break
                
                
    def go_to_map_by_f(self):
        pass
        
    
    def discover_feixingfu(self):
        tpl = self.Print_screen()
        status = State.NOTMATCH
        target = cv2.imread("./images/feixingfu.png")
        x,y = self.matchTemplate(tpl,target,0.15)
        if x != -1:
            print("发现飞行符")
            return State.OK,x,y
        return State.NOTMATCH,x,y
        
        
    def Tothecountryside(self):
        self.click(1695,1015)
        time.sleep(1)
        status,x,y= self.discover_feixingfu()
        if status == status.OK:
            print(x,y)
        self.click(x,y)
        time.sleep(1)
        self.click(654,669)
        time.sleep(1)
        self.go_to_CSC()
        #打开地图
        time.sleep(1)
        self.click(60,81)
        time.sleep(1)        
        if self.rgb_array(map_feature["长寿村"])==State.OK:
            self.tap_("长寿村",144,6)   
            time.sleep(0.5)
            while True:
                status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
                if status==status.NOTMATCH:
                    time.sleep(0.5)        
                else:
                    print("抵达目的地")
                    break
                
    def map_pos_conversion(self,_map,x,y):
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
            if status==status.OK:
                self.click(143,79)
                break
        qx = None,qy = None
        if _map in "长安城":
            qx = 267,qy = 891
            x = qx + math.ceil(x * 2.52)
            y = qy - math.ceil(y * 2.51)
            self.tap_(x,y)
        elif _map in "建邺城":
            qx = 267,qy = 893
            x = qx + math.ceil(x * 4.92)
            y = qy - math.ceil(y * 4.88)
            self.tap_(x+5,y-5)  
        elif _map in "朱紫国":
            qx = 382,qy = 901
            x = qx + math.ceil(x * 6.05)
            y = qy - math.ceil(y * 6.04)
            self.tap_(x,y)
        elif _map in "傲来国":
            qx = 431,qy = 894
            x = qx + math.ceil(x * 4.731)
            y = qy - math.ceil(y * 4.74)
            self.tap_(x,y)        
        elif _map in "大唐境外":
            qx = 191,qy = 683
            x = qx + math.ceil(x * 2.3984)
            y = qy - math.ceil(y * 2.4)
            self.tap_(x,y)
        elif _map in "大唐国境":
            qx = 624,qy = 1013
            x = qx + math.ceil(x * 2.5824)
            y = qy - math.ceil(y * 2.6)
            self.tap_(x,y+3)
        elif _map in "墨家村":
            qx = 850,qy = 982
            x = qx + math.ceil(x * 4.832)
            y = qy - math.ceil(y * 4.8)
            self.tap_(x,y+3)
        elif _map in "狮驼岭":
            qx = 602,qy = 937
            x = qx + math.ceil(x * 7.3)
            y = qy - math.ceil(y * 7.25)
            self.tap_(x+3,y-3)
        elif _map in "长寿郊外":
            qx = 678,qy = 929
            x = qx + math.ceil(x * 4.216)
            y = qy - math.ceil(y * 4.18)
            self.tap_(x,y)            
        elif _map in "北俱芦洲":
            qx = 608,qy = 935
            x = qx + math.ceil(x * 4.19)
            y = qy - math.ceil(y * 4.2)
            self.tap_(x,y)   
        elif _map in "花果山":
            qx = 612,qy = 932
            x = qx + math.ceil(x * 5.83125)
            y = qy - math.ceil(y * 5.859)
            self.tap_(x+5,y) 
        elif _map in "女儿村":
            qx = 802,qy = 891
            x = qx + math.ceil(x * 4.33594)
            y = qy - math.ceil(y * 4.32639)
            self.tap_(x+4,y+4)
        elif _map in "东海湾":
            qx = 728,qy = 932
            x = qx + math.ceil(x * 5.87)
            y = qy - math.ceil(y * 5.87)
            self.tap_(x+5,y)
        elif _map in "麒麟山":
            qx = 598,qy = 929
            x = qx + math.ceil(x * 5.0632)
            y = qy - math.ceil(y * 4.944)
            self.tap_(x,y)
        elif _map in "江南野外":
            qx = 602,qy = 938
            x = qx + math.ceil(x * 5.9625)
            y = qy - math.ceil(y * 5.967)
            self.tap_(x+5,y)
        elif _map in "五庄观":
            qx = 606,qy = 934
            x = qx + math.ceil(x * 9.46)
            y = qy - math.ceil(y * 9.467)
            self.tap_(x+9,y)
        elif _map in "普陀山":
            qx = 606,qy = 934
            x = qx + math.ceil(x * 9.9579)
            y = qy - math.ceil(y * 9.861)
            self.tap_(x,y)
        time.sleep(0.5)
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
            if status==status.NOTMATCH:
                time.sleep(0.5)        
            else:
                print("抵达目的地")
                break
                                                            
def main():
    #blRobot.Get_GameHwnd()
    start = time.time()
    Robot = action(zoom_count=1.5)
    Robot.Tothecountryside()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    
if __name__ == "__main__":
    main()