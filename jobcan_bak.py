'''
【要件】
pyファイルを実行したら、これまでの勤務時間や休憩時間を取得して、CSVファイルに出力できる。

最終的なゴール
・PowerBI上でPythonのコードを実行して、JOBCANの最新情報をCSVファイルに保存
・保存したCSVファイルをPowerBIで読み込み、データを可視化
'''

from bs4 import BeautifulSoup
import requests
import re
import numpy as np
from datetime import datetime

#フリーワード検索のURL
login_url = 'https://ssl.jobcan.jp/login/mb-employee'

#マイナビ版
def loginJOBCAN():

    '''前準備'''
    #セッションの立ち上げ
    session = requests.session()
    response = session.get(login_url)    
    soup = BeautifulSoup(response.text, 'lxml')
    
    #cookieを取得
    cookie = response.cookies
    
    #formで飛ばす情報
    info = {
        'client_id':'xxxxxxx',
        'email':'xxxx@xxxx.co.jp',
        'password':'xxxx1234',
        'url':'/m',
        'login_type':'1',
        'lang_code':'ja'
        }
    
    '''JOBCANのログインページのURLから、soupオブジェクトを作成'''
    login_res = session.post(login_url, data=info, cookies=cookie)

    '''出勤簿ページに入る'''
    recordURL = 'https://ssl.jobcan.jp/m/work/conditions'
    response2 = session.get('https://ssl.jobcan.jp/m/work/conditions')
    soup2 = BeautifulSoup(response2.text, 'lxml')
    #print(soup2)
    #exit()
    
    '''データの抽出'''
    monthData = soup2.find('th').get_text()
    
    #データテーブルの抽出
    clockedList = soup2.find_all('td')
    
    #整形したリ要素を格納するリスト
    sourceList = []
    
    #リストから不要な要素(改行, 空白) を削除
    clockedList = clockedList[2:-24]
    
    for t_bs in clockedList:
        t = t_bs.get_text()
        
        t = t.replace('\n', '')
        t = t.replace(' ','')
        t = t.replace('-','')
        t = t.replace('時間',':')
        t = t.replace('分','')
        #日付に月情報を加える
        try:
            if len(re.findall('^\w+\\(.+\\)$',t)) >= 1:
                t = monthData + t
        except TypeError:
            pass
        sourceList.append(t)

    #日ごとに要素をまとめる
    dataList = []
    dataList.append(['日付', '状態', '出勤', '退勤', '休憩', '総労働'])
    for num in range(0,len(sourceList),6):
        dataList.append(sourceList[num:num+6])
    
    #抽出データそのままのCSVファイル作成(目視用)
    try:
        #list->np.array->csv
        a = np.array(dataList)
        np.savetxt('jobcan_source.csv', a, delimiter=',', fmt='%s')
    except PermissionError:
        print('保存予定のCSVファイルを開いています。\nファイルを閉じてから処理を実行してください。')
        exit()
    
    
    '''日付、時間をdatetimeオブジェクトに変換する'''
    #データ型を変えた後に格納するリスト
    for num in range(1,len(dataList)):
        #第0要素が年月日
        dataList[num][0] = dataList[num][0].replace('年', '/')
        dataList[num][0] = dataList[num][0].replace('月', '/')
        dataList[num][0] = dataList[num][0][:-3]
        
        #月と日について、1桁の時、文字列'0'を追加。
        if ('/' in dataList[num][0][5:7]):
            dataList[num][0] = dataList[num][0][:5] + '0' +dataList[num][0][5:]
        if (len(dataList[num][0]) == 9):  
            dataList[num][0] = dataList[num][0][:8] + '0' + dataList[num][0][8]
        #datetime型への変換
        dt_obj_0 = datetime.strptime(dataList[num][0], '%Y/%m/%d')
        
        #開始時間、終了時間にも年月日データを追加する。
        if (len(dataList[num][2]) >= 1) or (len(dataList[num][3]) >= 1):   
            dataList[num][2] = dataList[num][0] + ' ' + dataList[num][2]
            dataList[num][3] = dataList[num][0] + ' ' + dataList[num][3]
            #datetime型への変換
            dt_obj_2 = datetime.strptime(dataList[num][2], '%Y/%m/%d %H:%M')
            dt_obj_3 = datetime.strptime(dataList[num][3], '%Y/%m/%d %H:%M')
            #上書き
            dataList[num][2] = dt_obj_2
            dataList[num][3] = dt_obj_3
        else:
            print(f'{dataList[num][0]}: 打刻なし')
            dataList[num][0] = dt_obj_0
            continue
        #年月日は文字列を処理中に使用するため、datetime型への変換の処理の後に基のリストを上書きする
        dataList[num][0] = dt_obj_0

        #休憩時間の小数化
        if (dataList[num][4][-2:] == '00'): 
            dataList[num][4] = float(dataList[num][4][0:2])
        else:
            dataList[num][4] = float(dataList[num][4][0:2]) + (float(dataList[num][4][-2:]) / 60)
        
        #総労働時間の小数化
        if (dataList[num][5][-2:] == '00'): 
            dataList[num][5] = float(dataList[num][5][0:2])
        else:
            dataList[num][5] = float(dataList[num][5][0:2]) + (float(dataList[num][5][-2:]) / 60)   
    
    #PowerBI用にCSVファイルを作成
    try:
        a = np.array(dataList)
        np.savetxt('jobcan_transformed.csv', a, delimiter=',', fmt='%s')
    except PermissionError:
        print('保存予定のCSVファイルを開いています。\nファイルを閉じてから処理を実行してください。')
        exit()
    
    
'''実行'''
loginJOBCAN()

