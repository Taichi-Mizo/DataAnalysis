import pandas as pd
import numpy as np
from sqlalchemy import column
import matplotlib.pyplot as plt
import seaborn as sns

#DataFrameの準備
fpath =r"C:\Users\mizot\OneDrive - シアトルコンサルティング株式会社\ドキュメント\会社関連\TTL\16期\仮説検証チーム\16期下期\20220328_STスコア.xlsx"
snames=['Relation', 'Communication', 'Direction', 'Role', 'Synergy']
df = pd.read_excel(fpath, sheet_name=snames)
df_rel = df[snames[0]]
df_com = df[snames[1]]
df_dir = df[snames[2]]
df_rol = df[snames[3]]
df_syn = df[snames[4]]

'''月ごとの平均値'''
def st_score_mean():
    #1. チームごとに大項目スコアをまとめる
    #1.1全てのdfを集約(チーム名とToカラムは未使用)
    df_all = pd.concat([df_rel, df_com, df_dir, df_rol, df_syn]).drop(axis=1, columns=['To', 'チーム名'])
    #1.2Fromカラムを月のみにする
    df_all['From'] = df_all['From'].dt.month
    #1.3カラム名変更
    df_all.rename(columns={'From':'month_answer'}, inplace=True)
    
    #2. ピボットテーブル作成
    #2.1チーム名, 時期(月)を行に定め、各項目の平均スコアをカラムとして指定
    df_pivot = pd.pivot_table(df_all, index=['month_answer'], columns=['大項目'], values=['スコア'], aggfunc=np.mean).reset_index()
    #multi-indexを分解して、一つのdfに変換
    df_pivot = pd.concat([df_pivot['month_answer'], df_pivot['スコア']], axis=1).drop(columns=['month_answer'])
    print(df_pivot)

    #3.相関係数を算出
    df_corr = df_pivot.corr()
    
    #4. 可視化
    #4-1. 可視化1: 散布図
    plt.figure()
    plt.figure(figsize=(6,6))
    imgpath_scatter = r'C:\Users\mizot\OneDrive - シアトルコンサルティング株式会社\ドキュメント\Python Scripts\データ分析\TTL\scatter_month.png'
    sns.pairplot(df_pivot).savefig(imgpath_scatter)
    #4-1. 可視化2: ヒートマップ
    plt.figure()
    plt.figure(figsize=(11,11))
    imgpath_heatmap = r'C:\Users\mizot\OneDrive - シアトルコンサルティング株式会社\ドキュメント\Python Scripts\データ分析\TTL\heatmap_month.png'
    sns.heatmap(df_corr, annot=True, cmap='PuBu', vmax=1.0, center=0.0, vmin=-1.0)
    plt.savefig(imgpath_heatmap)
    plt.close('all')

'''チーム単位で上記のdfを作成'''
#チームごとに相関係数を算出


#4. 各チームで算出した各相関係数の平均を各組み合わせで算出


'''実行'''
st_score_mean()