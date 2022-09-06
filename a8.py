import re


def chiba_jusho_douro(jusho):#千葉の住所を道路を取得するために分割
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
    else:
        pass
    
    ku_lst = ['中央区', '花見川区', '稲毛区', '若葉区', '緑区', '美浜区']

    if (ku in ku_lst)==False:
        #存在しない住所
        pass

    else:
        if('A' not in jusho):
            chou = "丁目なし"
            #print("丁:"+chou)
            #数字より前が町大字名
            #残りの数字は街区番号
            m = re.search(r'\d+', jusho)
            ban = (m.group())
            machi_ = jusho.split(ban)
            ban = ban.replace("１","1").replace("２","2").replace("３","3").replace("４","4").replace("５","5").replace("６","6").replace("７","7").replace("８","8").replace("９","9").replace("０","0")
            #machi_ = jusho.split(ban)
            machi_chou = machi_[0]
            # print(ban)
            # print(machi_chou)

        else:
            index_A = jusho.index("A") #'A'が何文字目にあるのか取得
            #print(index_A)
            chou = jusho[index_A-1]+'丁目'
            #print("丁:"+chou)
            machi = jusho[:index_A-1]
            #print("町大字名:"+machi)
            jusho = jusho.split('A')
            #print(jusho)
            jusho = jusho[1]
            # print(jusho)
            jusho = jusho.replace("１","1").replace("２","2").replace("３","3").replace("４","4").replace("５","5").replace("６","6").replace("７","7").replace("８","8").replace("９","9").replace("０","0")
            # print(jusho)
            m = re.search(r'\d+', jusho)
            ban = m.group()
            ban = ban.replace("１","1").replace("２","2").replace("３","3").replace("４","4").replace("５","5").replace("６","6").replace("７","7").replace("８","8").replace("９","9").replace("０","0")
            # print(ban)
            machi_chou = machi+chou
    return [ku,machi_chou,ban]