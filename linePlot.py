import glob
import pandas as pd


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
    colsList = [0,1,2,5,6]
    
    #読み込んだDFから不要なrowsを削除
    df_rowsDeleted = df_read.drop(index=df_read.index[rowsList], columns=df_read.columns[colsList])
    
    return df_rowsDeleted


def controller():

    #CSVファイルを格納しているディレクトリのパス
    dirPath = r'C:\Users\Taichi Mizo\OneDrive - シアトルコンサルティング株式会社\ドキュメント\Python Scripts\データ分析\情報通信業'
    
    #絶対パスの取得
    absPathList = getFilePath(dirPath)
    
    #DataFrameの生成
    df_rowsDeleted = getDF()
    
    #DataFrameの可視化(意図したとおりに作成できているか確認)
    print(df_rowsDeleted)
    
    
    

'''
実行
'''
controller()