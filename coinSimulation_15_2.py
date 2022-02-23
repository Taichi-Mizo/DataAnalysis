'''
p.223 15.3 推計統計とシミュレーション
コード 15.2 コイン投げ
'''
import random
import pandas as pd
import matplotlib.pyplot as plt



def flip(numFlips):
    ''' numFlips: 正の整数'''
    heads = 0
    for i in range(numFlips):
        if random.choice(('H', 'T')) == 'H':
            heads += 1
    return heads/numFlips


def flipSim(numFlipsPerTrial, numTrials):
    '''numFlipsPerTrial, numTrials:　正の整数'''
    fracHeads = []
    for i in range(numTrials):
        fracHeads.append(flip(numFlipsPerTrial))
    mean = sum(fracHeads) / len(fracHeads)
    return mean

#print('Mean=', flipSim(10, 100))

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

def visualizeSimRes(numFlipsPerTrial, numTrials):
    '''numFlipsPerTrial, numTrials:　正の整数'''
    fracHeads = []
    calcList = []
    for i in range(numTrials):
        calcList.append(flip(numFlipsPerTrial))
        fracHeads.append((sum(calcList) / len(calcList)))
    
    #x軸の試行回数リスト生成
    numList = getNums(1, numTrials)
    
    print(fracHeads)    
    #シミュレーションで得た数列を可視化する
    x = numList
    y = fracHeads
    plt.plot(x, y)
    plt.xlabel('Number of Trials')
    plt.ylabel('Total Average')
    plt.title('Probability to be heads on tossing coin')
    plt.show()
    

'''execution'''
visualizeSimRes(10, 500)