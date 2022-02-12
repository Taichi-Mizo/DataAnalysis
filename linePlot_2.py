import glob
import pandas as pd
import matplotlib.pyplot as plt
from googletrans import Translator


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
def getDF(fpath):
    
    #test_path
    #fpath = r"C:\Users\Taichi Mizo\OneDrive - シアトルコンサルティング株式会社\ドキュメント\Python Scripts\データ分析\情報通信業\FEH_00350600_220211180253.csv"
    
    #CSV→DataFrame(文字コード:SHIFT-JISとして読み込み)
    df_read = pd.read_csv(fpath, header=None, encoding='cp932')
    
    '''
    ファイルごとにレコード数が異なるため、年期カラムの年数を指定して、2001~2020年のデータを取得する。
    '''
    #文字列「年  期」がある行のインデックス(何行目にあるか)を取得(5列目に検索する値があると仮定)
    rowIndex = df_read.index[df_read[2] == '年  期'].tolist()
    
    #取得したindexにある値をheaderとして指定
    headerList = df_read.iloc[rowIndex[0]]
    df_read.columns = headerList    
    
    '''不要な列の削除'''
    #不要な行・列番号を指定し、リストで取得
    rowsList = getNums(0,rowIndex[0])
    colsList = [3]
    
    #読み込んだDFから不要なrowsを削除
    df = df_read.drop(index=df_read.index[rowsList], columns=df_read.columns[colsList])
    
    return df


'''
先頭行をheaderとして、入力したカラム名に一致する列のカラム名とデータを取得/extractCol
引数: 手順３で整形したDataFrame/df
戻り値: グラフ化の対象となるデータ/data
'''
def extractCol(df):
    
    #年期カラムの値から数字のみ取得・置換
    for y in df['年  期']:
        df = df.replace(y, y[0:4])
    
    #年期カラムの値が2001~2020年の行のインデックス(list)を取得
    f_num = df.index[df['年  期'] == '2001'].tolist()
    l_num = df.index[df['年  期'] == '2020'].tolist()
    
    #グラフ化するレコードを取得
    data = df.iloc[f_num[0]:l_num[0],:]
    
    return data


'''
Googletransを用いた日英翻訳/translateJP2EN
引数: 日本語の文字列/JPtext
戻り値: 英語の文字列/ENtext
'''
def translateJP2EN(JPtext):
    
    translator = Translator()
    
    ENtext = translator.translate(JPtext, src='ja', dest='ja').text
    
    #print(ENtext)
    
    return ENtext
    

'''
取得したいデータを指定し、グラフ化/visualizeData
引数: データセット/data, グラフの配置位置(list型)/lay_val
戻り値: グラフ
'''
def visualizeData(fig, axs, input_col, data, lay_val): 
    
    #業種を取得(for title)
    industry = data.iloc[0]['業種 (金融業、保険業以外の業種)']
    industryEN = translateJP2EN(industry)
    
    #資本金規模を取得(for title)
    capital = data.iloc[0]['規模 (金融業、保険業以外の業種)']
    capitalEN = translateJP2EN(capital)
    
    #カラム名をリストで取得
    colNames = list(data.columns)
    
    if (input_col not in colNames):
        print('入力した値が見つかりませんでした。')
        print('抽出したDataFrameのみ表示します')
        print(data)
        exit()

    else:
        print('検索した値が見つかりました。')
    
    '''入力値をカラム名とする列の値を取得'''
    obj_data = data[input_col]
    
    for v in obj_data:
        
        #カンマを排除
        no_c = v.replace(',','')
        #カンマを排除した値で置換
        obj_data = obj_data.replace(v, no_c)
    
    
    #データ型を調整
    obj_data = obj_data.astype(float) 
    
    '''取得した値をline plotでグラフ化・表示'''   
    #x軸(横軸), y軸(縦軸)に割り当てる値を指定
    x = data['年  期']
    y = obj_data
    
    #資本金規模を取得
    capital = data.iloc[0]['規模 (金融業、保険業以外の業種)']
    cap_EN = translateJP2EN(capital)
    
    '''プロット'''
    #グラフの表示位置
    ax = axs[lay_val[0], lay_val[1]]
    
    #グラフで表示する値の指定
    ax.plot(x, y)
    
    #y軸のスケールの種類
    ax.set_yscale('linear')
    
    #y軸のタイトル
    #ax.set_ylabel(labelEN)
    
    #x軸のタイトル
    #ax.set_xlabel('Fiscal Year')
    
    #タイトルの指定
    title_str = industryEN + ' /  ' + capitalEN
    ax.set_title(title_str)
    
    #グリッドの有無
    ax.grid(axis='y')
    
    
def controller():   

    #CSVファイルを格納しているディレクトリのパス
    dirPath = r'C:\Users\Taichi Mizo\OneDrive - シアトルコンサルティング株式会社\ドキュメント\Python Scripts\データ分析\情報通信業'
    
    #絶対パスの取得
    absPathList = getFilePath(dirPath)
    
    #取得したいデータ名を入力
    input_col = input('グラフ化したい列のカラム名を入力してください:')
    
    #フォルダ内の全ファイル分のデータセットを取得して、各資本金規模間で値の遷移を比較する。
    layoutLists = [[0,0], [0,1], [1,0], [1,1], [2,0], [2,1]]
    
    #表示するグラフの数を指定
    fig, axs = plt.subplots(3, 2, figsize=(3, 4),constrained_layout=True)
    
    for num in range(len(absPathList)):
        
        print('【',(num + 1), '/', len(absPathList), '】 読み込み中:\r\n')
        print(absPathList[num])
        
        #生データの読み込み
        df = getDF(absPathList[num])
        
        #dataframeの整形(意図したとおりに作成できているか確認)
        data = extractCol(df)
        
        #グラフ化
        visualizeData(fig, axs, input_col, data, layoutLists[num])
    
    #subplotのタイトルをつける
    labelEN = translateJP2EN(input_col)
    title = str(labelEN + ' , FY 2001-2020')
    fig.suptitle(title, fontsize=16)
    
    plt.show()


'''
実行
'''
controller()

