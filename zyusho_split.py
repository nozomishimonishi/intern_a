from platform import machine
import re
from kanjize import int2kanji, kanji2int

# zyusho==文字列
def chiba_zyusho_split(zyusho):
    zyusho = str(zyusho)
    
    zyusho = zyusho.replace('丁目', '-',1).replace('番地', '-',1)
    zyusho = zyusho.replace('丁', '-',1).replace('番', '-',1)
    zyusho = zyusho.replace('ー', '-',1).replace('ー', '-',1)
    zyusho = zyusho.replace('―', '-',1).replace('―', '-',1)
    zyusho = zyusho.replace('‐', '-',1).replace('‐', '-',1)
    zyusho = zyusho.replace('－', '-',1).replace('－', '-',1)
    zyusho = zyusho.replace('-', 'A', 1)
    zyusho = zyusho.replace('-', 'B', 1)
    
    if "千葉県" in zyusho:
        zyusho = zyusho.split('県')
        zyusho = zyusho[1]

    if "千葉市" in zyusho:
        zyusho = zyusho.split('市')
        zyusho = zyusho[1]

    # 住所あかんかったらTrueにするで
    zyusho_akan = False

    if "区" in zyusho:
        zyusho = zyusho.split('区')
        ku = zyusho[0] + '区'
        zyusho = zyusho[1]
        # print(ku)
    else:
        # 住所あかん
        zyusho_akan = True
        return [zyusho_akan,True,'','','','','']
    
    ku_lst = ['中央区', '花見川区', '稲毛区', '若葉区', '緑区', '美浜区']

    if (ku in ku_lst)==False:
        zyusho_akan = True
        # 住所全然あかん
        zyusho_akan = True
        return [zyusho_akan,True,'','','','','']
    else:
        index_A = zyusho.index("A")  
        
        if ('A' in zyusho)==False:
            # 住所完全にあかん
            zyusho_akan = True
            return [zyusho_akan,True,'','','','','']

        else:
            
            # 丁目なし
            if ('B' in zyusho)==False:
                chou_nothing = True
                chou = ""
                ban = zyusho[:index_A]
                other = zyusho[index_A+1:]

                ban2 = ban
                ban2=ban2.replace("一","1").replace("二","2").replace("三","3").replace("四","4").replace("五","5").replace("六","6").replace("七","7").replace("八","8").replace("九","9").replace("〇","0")
                ban2=ban2.replace("１","1").replace("２","2").replace("３","3").replace("４","4").replace("５","5").replace("６","6").replace("７","7").replace("８","8").replace("９","9").replace("０","0")

                for i in range(-1,-4,-1):
                    if (ban2[i]==("0"or"1"or"2"or"3"or"4"or"5"or"6"or"7"or"8"or"9"or"0"))==False:
                        break
                    else:
                        suji = i
                
                machi = ban2[:i]
                ban = ban2[i:]

            # 丁目あり
            else:
                chou_nothing = False
                index_B = zyusho.index("B")
                chou = zyusho[:index_A]
                ban = zyusho[index_A+1:index_B]
                other = zyusho[index_B+1:]

                chou2 = chou
                chou2=chou2.replace("一","1").replace("二","2").replace("三","3").replace("四","4").replace("五","5").replace("六","6").replace("七","7").replace("八","8").replace("九","9").replace("〇","0")
                chou2=chou2.replace("１","1").replace("２","2").replace("３","3").replace("４","4").replace("５","5").replace("６","6").replace("７","7").replace("８","8").replace("９","9").replace("０","0")

                for i in range(-1,-4,-1):
                    if (chou2[i]==("0"or"1"or"2"or"3"or"4"or"5"or"6"or"7"or"8"or"9"or"0"))==False:
                        break
                    else:
                        suji = i
                machi = chou2[:i]
                chou = chou2[i:]

        return [zyusho_akan,chou_nothing,ku,machi,chou,ban,other]
        

#print(chiba_zyusho_split("千葉県千葉市美浜区真砂５ー１５ー１"))  
#print(chiba_zyusho_split("千葉県千葉市新千葉一丁目7番2号"))
#print(chiba_zyusho_split("千葉県浦安市北栄1-15-9"))