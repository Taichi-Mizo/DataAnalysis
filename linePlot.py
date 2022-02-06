import glob
import pandas as pd
import matplotlib.pyplot as plt

'''
1. CSVファイルを格納しているディレクトリのパスから、各CSVファイルのパスを取得/getFilePath
引数: dirPath
戻り値: 絶対パスリスト/absPathList
'''
def getFilePath(dirPath):

    #ディレクトリ内のファイルパスを取得
    absPathList = glob.glob((dirPath + '\\*'))
    
    return absPathList

'''
連番生成/getNums
引数: 最初の数字, 最後の数字
戻り値: 連番リスト/numsList
'''
def getNums(fnum, lnum):
    
    #連番リスト
    numList = [fnum]
    
    while (numList[(len(numList)-1)] != lnum):
    
        num_latest = len(numList) - 1
        nextNum = numList[num_latest] + 1
        numList.append(nextNum)
    
    return numList
        

'''
取得したCSVファイルのパスから、CSVファイルの読み込み/getDF
引数: csvファイルパス/fpath
戻り値: df
'''
def getDF():
    
    #test_path
    fpath = r"C:\Users\Taichi Mizo\OneDrive - シアトルコンサルティング株式会社\ドキュメント\Python Scripts\データ分析\情報通信業\10億円以上.csv"
    
    #CSV→DataFrame(文字コード:SHIFT-JISとして読み込み)
    df_read = pd.read_csv(fpath, header=None, encoding='SHIFT-JIS')
    
    #不要な行番号を指定し、リストで取得
    rowsList_1 = getNums(0,7)
    rowsList_2 = getNums(9,38)
    rowsList = rowsList_1 + rowsList_2
    
    #不要な列番号を指定し、リストで取得
    colsList = [0,1,2,4,6]
    
    #読み込んだDFから不要なrowsを削除
    df = df_read.drop(index=df_read.index[rowsList], columns=df_read.columns[colsList])
    
    return df


'''
先頭行をheaderとして、入力したカラム名に一致する列のカラム名とデータを取得/extractCol
引数: 手順３で整形したDataFrame/df
戻り値: グラフ化の対象となるデータ/data
'''
def extractCol(df):

    #headerList(列名を取得)
    headerList = df.iloc[0]
    
    #カラム名の指定
    df.columns = headerList
    
    #カラム付きデータセット
    df = df[1:]
    
    #年期の値から数字だけ抽出
    for y in df['年  期']:
        df = df.replace(y, y[0:4])
    
    #年期をindexに指定
    data = df.set_index('年  期')
    
    return data


'''
取得したいデータを指定し、グラフ化/visualizeData
引数: data
戻り値: グラフ
'''
def visualizeData(data):
    
    #取得したいデータ名を入力
    input_col = input('グラフ化したい列のカラム名を入力してください:')
    
    #カラム名をリストで取得
    colNames = list(data.columns)
    
    if (input_col not in colNames):
        print('入力した値が見つかりませんでした。')
        exit()

    else:
        print('検索した値が見つかりました。')
    
    #入力値をカラム名とする列の値を取得
    obj_data = data[input_col]
    for v in obj_data:
        
        #カンマを排除
        no_c = v.replace(',','')
        #カンマを排除した値で置換
        obj_data = obj_data.replace(v, no_c)
    #print(obj_data)
    
    
    #データ型を調整
    #data[input_col] = obj_data.astype(float)
    obj_data = obj_data.astype(int)
    
    
    #取得した値をline plotでグラフ化・表示
    linePlot = obj_data.plot(x = 'fiscal year', y = input_col, kind="line")
    plt.show()
    


def controller():

    #CSVファイルを格納しているディレクトリのパス
    dirPath = r'C:\Users\Taichi Mizo\OneDrive - シアトルコンサルティング株式会社\ドキュメント\Python Scripts\データ分析\情報通信業'
    
    #絶対パスの取得
    absPathList = getFilePath(dirPath)
    
    #DataFrameの生成
    df = getDF()
    
    #DataFrameの可視化(意図したとおりに作成できているか確認)
    data = extractCol(df)
    
    #グラフ化
    visualizeData(data)
    

'''
実行
'''
controller()