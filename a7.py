import re


def chiba_jusho_gesui(jusho):#千葉の住所を下水を取得するために分割
    #数字の間の文字を半角ハイフンに置き換え
    jusho = jusho.replace('丁目', '-',1).replace('番地', '-',1)
    jusho = jusho.replace('丁', '-',1).replace('番', '-',1)
    jusho = jusho.replace('ー', '-',1).replace('ー', '-',1)
    jusho = jusho.replace('―', '-',1).replace('―', '-',1)
    jusho = jusho.replace('‐', '-',1).replace('‐', '-',1)
    jusho = jusho.replace('－', '-',1).replace('－', '-',1)


    #数字を書き換える
    jusho = jusho.replace("一","１").replace("二","２").replace("三","３").replace("四","４").replace("五","５").replace("六","６").replace("七","７").replace("八","８").replace("九","９").replace("〇","０")
    jusho = jusho.replace("1","１").replace("2","２").replace("3","３").replace("4","４").replace("5","５").replace("6","６").replace("7","７").replace("8","８").replace("9","９").replace("0","０")
    #ハイフンの有無を確かめる
    jusho = jusho.replace('-', 'A',1)
    #print(jusho)

    # jusho = jusho.replace('-', 'B', 1)
    # print(jusho)
    
    

    if "千葉県" in jusho:
        jusho = jusho.split('県')
        jusho = jusho[1]
        #print('(千葉県)'+jusho)

    if "千葉市" in jusho:
        jusho = jusho.split('市')
        jusho = jusho[1]
        #print('(千葉市)'+jusho)


    if "区" in jusho:
        jusho = jusho.split('区')
        ku = jusho[0] + '区'
        jusho = jusho[1]
        #print("区："+ku)
        #print(jusho)
    else:
        pass
    
    ku_lst = ['中央区', '花見川区', '稲毛区', '若葉区', '緑区', '美浜区']

    if (ku in ku_lst)==False:
        #存在しない住所
        pass

    else:
        if('A' not in jusho):
            chou = "丁目なし"
            # print("丁:"+chou)
            #machi_chou = jusho #道路の時の引数
            #数字より前が町大字名
            #残りの数字は街区番号
            m = re.search(r'\d+', jusho)
            #banが違う
            ban = (m.group()+'番地')
            ban = ban.replace("１","1").replace("２","2").replace("３","3").replace("４","4").replace("５","5").replace("６","6").replace("７","7").replace("８","8").replace("９","9").replace("０","0")
            # print(ban)
            machi_ = jusho.split(m.group())
            # print(machi_[0])
            machi = machi_[0]

        else:
            index_A = jusho.index("A") #'A'が何文字目にあるのか取得
            #print(index_A)
            chou = jusho[index_A-1]+'丁目' #数字は全角
            # chou = chou.replace("一","1").replace("二","2").replace("三","3").replace("四","4").replace("五","5").replace("六","6").replace("七","7").replace("八","8").replace("九","9").replace("〇","0")
            # chou = chou.replace("１","1").replace("２","2").replace("３","3").replace("４","4").replace("５","5").replace("６","6").replace("７","7").replace("８","8").replace("９","9").replace("０","0")
            #print("丁:"+chou)
            machi = jusho[:index_A-1]
            #print("町大字名:"+machi)
            jusho = jusho.split('A')
            #print(jusho)
            jusho = jusho[1]
            m = re.search(r'\d+', jusho)
            ban = m.group()+'番'
            #print(ban)
    return [ku,machi,chou,ban]