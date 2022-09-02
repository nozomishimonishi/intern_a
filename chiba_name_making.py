def chiba_road_name(ku,machi,chou,ban):
    if chou=="":
        return [ku,machi,ban]
    else:
        chou=chou.replace("0","０").replace("1","１").replace("2","２").replace("3","３").replace("4","４").replace("5","５").replace("6","６").replace("7","７").replace("8","８").replace("9","９")
        ban=ban.replace("0","０").replace("1","１").replace("2","２").replace("3","３").replace("4","４").replace("5","５").replace("6","６").replace("7","７").replace("8","８").replace("9","９")
        machi = machi+chou+"丁目"
        return [ku,machi,ban]

def chiba_gesui_name(ku,machi,chou,ban):
    if chou=="":
        chou="丁目なし"
    ban=ban.replace("0","０").replace("1","１").replace("2","２").replace("3","３").replace("4","４").replace("5","５").replace("6","６").replace("7","７").replace("8","８").replace("9","９")
    ban=ban+"番地"
    return [ku,machi,chou,ban]


