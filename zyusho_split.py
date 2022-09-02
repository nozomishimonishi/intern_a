from platform import machine
import re
from kanjize import int2kanji, kanji2int

# zyusho==文字列
def chiba_zyusho_split(zyusho):
    zyusho = str(zyusho)
    
    zyusho = zyusho.replace('丁目', '-',1).replace('番地', '-',1)
    zyusho = zyusho.replace('丁', '-',1).replace('番', '-',1)
    zyusho = zyusho.replace('ー', '-')
    zyusho = zyusho.replace('―', '-')
    zyusho = zyusho.replace('−', '-')
    zyusho = zyusho.replace('‐', '-')
    zyusho = zyusho.replace('－', '-')
    zyusho = zyusho.replace('-', 'A', 1)
    zyusho = zyusho.replace('-', 'B', 1)

    zyusho=zyusho.replace("一","1").replace("二","2").replace("三","3").replace("四","4").replace("五","5").replace("六","6").replace("七","7").replace("八","8").replace("九","9").replace("〇","0")
    zyusho=zyusho.replace("１","1").replace("２","2").replace("３","3").replace("４","4").replace("５","5").replace("６","6").replace("７","7").replace("８","8").replace("９","9").replace("０","0")

    
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
            suji=-1
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
                    if (ban2[i]=="0" or ban2[i]=="1" or ban2[i]=="2" or ban2[i]=="3" or ban2[i]=="4" or ban2[i]=="5" or ban2[i]=="6" or ban2[i]=="7" or ban2[i]=="8" or ban2[i]=="9" or ban2[i]=="0")==True:
                        suji = i
                    else:
                        break
                
                machi = ban2[:suji]
                ban = ban2[suji:]

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
                    if (chou2[i]=="0" or chou2[i]=="1" or chou2[i]=="2" or chou2[i]=="3" or chou2[i]=="4" or chou2[i]=="5" or chou2[i]=="6" or chou2[i]=="7" or chou2[i]=="8" or chou2[i]=="9" or chou2[i]=="0")==True:
                        suji = i
                    else:
                        break
                machi = chou2[:suji]
                chou = chou2[suji:]

        return [zyusho_akan,chou_nothing,ku,machi,chou,ban,other]
        

print(chiba_zyusho_split("千葉県千葉市美浜区真砂６丁目１−１"))  
#print(chiba_zyusho_split("千葉県千葉市新千葉一丁目7番2号"))
#print(chiba_zyusho_split("千葉県浦安市北栄1-15-9"))