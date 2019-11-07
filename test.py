#coding:utf-8

import re
import pprint
from sys import argv

# logFileName = "./Gaussian/output/C13H10-フルオレン_ExS.log" # ログファイル名
logFileName = argv[1]
# logText = None

def readlog(logFileName):
    with open(logFileName, "r", encoding="utf-8", errors="ignore") as logFile:
        for eachLogLine in logFile:
            yield eachLogLine

def is_float(s):
    try:
        float(s)
    except:
        return False
    return True

def getExcitedStateLog(call, logFileName):
    """
    励起状態のエネルギー，波長，振動子強度などの情報が記された
    ログを取得する
    """
    for eachLogLine in call(logFileName):
        if "Excited State" in eachLogLine:
            # print(eachLogLine)
            yield eachLogLine
        if "->" in eachLogLine:
            # print(eachLogLine)
            yield eachLogLine

def getMolcularOrbitalLog(logFileName):
    orbitalInfoLoad = False
    # logOrbitalInfo = ""
    for eachLogLine in readlog(logFileName):
        if "Molecular Orbital Coefficients:" in eachLogLine:
            orbitalInfoLoad = True
            continue
        if orbitalInfoLoad and not "Density Matrix" in eachLogLine:
            # logOrbitalInfo += eachLogLine
            yield eachLogLine
        if not "Density Matrix" in eachLogLine:
            continue
        else:
            break
    # return logOrbitalInfo

def getExcitedStateParameters():
    excitedStateDict = {}
    excitedElectronDict = {}
    nthexcitedState = 0
    for line in getExcitedStateLog(readlog, logFileName):
        # excitedStateInfoList = line.strip().split()
        # if "Excited" in ex
        line = line.strip()
        if "Excited State" in line:
            excitedStateInfoList = line[16:].split()
            excitedStateInfoList[0] = excitedStateInfoList[0][0]
            excitedStateDict[excitedStateInfoList[0]] = [
                excitedStateInfoList[1], # 電子状態
                excitedStateInfoList[2], # 励起エネルギー
                excitedStateInfoList[4], # 波長
                excitedStateInfoList[6][2:] # 振動子強度
            ]
            nthexcitedState = excitedStateInfoList[0]
            if nthexcitedState not in excitedElectronDict:
                excitedElectronDict[nthexcitedState] = []
        else:
            excitedStateInfoList = line.split("  ")
            excitedElectronDict[nthexcitedState].append([excitedStateInfoList[0], excitedStateInfoList[-1]])


    for key in excitedStateDict.keys():
        print("第{}励起状態 電子状態: {} 励起エネルギー: {}eV 波長: {}nm 振動子強度: {}".format(
                key,
                excitedStateDict[key][0],
                excitedStateDict[key][1],
                excitedStateDict[key][2],
                excitedStateDict[key][3]
            ))
        # print("励起電子配置")
        # pprint.pprint(excitedElectronDict[key])

def getEigenValues():
    """
    軌道エネルギーのリストをログのファイルから取得する関数
    """
    occ_size = 0 # 被占軌道の数
    virt_size = 0 # 空軌道
    ssss = []
    for eachLogLine in readlog(logFileName):
        eachLogLine = eachLogLine.strip()
        if "Alpha  occ. eigenvalues --" in eachLogLine:
            eachLogLine = eachLogLine.strip("Alpha  occ. eigenvalues --")
            tmp = list(map(lambda x: float(x),eachLogLine.split()))
            ssss.extend(tmp)
            occ_size+=len(tmp)
        elif "Alpha virt. eigenvalues --" in eachLogLine :
            eachLogLine = eachLogLine.strip("Alpha  virt. eigenvalues --")
            # tmp = eachLogLine.split()
            tmp = list(map(lambda x: float(x),eachLogLine.split()))
            ssss.extend(tmp)
            virt_size+=len(tmp)
        else:
            continue
    return ssss
    # print(occ_size)
    # print(virt_size)
    # size = 5
    # eigenvalues = [] # 軌道エネルギー
    # i = 0
    # for s in ssss:
    #     if i == 0:
    #         d = []
    #         for _ in range(size):
    #             d.append(-99999999)
    #         eigenvalues.append(d)
    #     eigenvalues[-1][i] = s
    #     i+=1
    #     i%=5
    # print(dddd)

def getOrbitInfo(isDetail):
    spacePtn = re.compile(" {23}.*") # 分子軌道表のヘッダー部分の空白検知用
    numPtn = re.compile("\d.*") # はじめの一文字が数字を検知

    # orbitNumbers = []
    O_counter = 0
    orbitalLog = [] # 軌道係数

    for eachLogLine in getMolcularOrbitalLog(logFileName):
        if not isDetail:
            if spacePtn.match(eachLogLine): # header 
                eachLogLine = eachLogLine.strip() # 空白除去
                if numPtn.match(eachLogLine): # 数字の行を検知
                    splitted_line = eachLogLine.split() # スペースで区切る
                    # check = True
                    # for l in splitted_line:
                    #     if not is_float(l):
                    #         check = False
                    # if check:
                    #     continue
                    # orbitNumbers.extend(splitted_line) # 分子軌道番号
                    # yield splitted_line
                    # print(eachLogLine)
                else: # 軌道の説明行を検知
                    for orbital in eachLogLine.split(): 
                        if "O" in orbital: # 占有軌道を検知
                            O_counter += 1 # 
        else: # 軌道係数
            if spacePtn.match(eachLogLine):
                continue
            eachLogLine = eachLogLine.strip()
            # yield eachLogLine
            orbitalLog.append(eachLogLine)
    if not isDetail:
        return O_counter
    else:
        return orbitalLog

def getNumOrbitalHOMO_LUMO():
    homo = getOrbitInfo(False)
    lumo = homo+1
    # print(homo, lumo)
    return [homo, lumo]

def getOrbitalDetail():
    atomOrbitalNum = [] # 原子軌道番号 分子軌道表の左端
    orbitalDict = dict() # 分子軌道の表，基底関数の番号がdictのkey
    for eachLogLine in getOrbitInfo(True): 
        num =  eachLogLine.split() # 空白で分割
        if len(num) == 0:
            continue
        if "Eigenvalues" == num[0]: # 励起エネルギーの行をスキップ
            continue
        atomOrbitalNum.append(int(num[0])) # 原子軌道番号を格納
        if int(num[0]) not in orbitalDict: # 原子軌道番号表，原子軌道番号ごとにリストを作成
            orbitalDict[int(num[0])] = []

        eachLogLine = eachLogLine[19:] # 分子軌道係数一行分
        eachLogLineList = eachLogLine.split(" ") # リストに変換
        if len(eachLogLineList) != 5: 
            # 空白でsplitしてリストを作成する，
            # うまいことsplitできなかった-記号で数字がつながっている部分に空白を含める
            eachLogLineList = re.sub("(\d)(\-\d)", "\\1 \\2", eachLogLine).split() #
        for data in eachLogLineList:
            if is_float(data): 
                # float型に文字列型の数値が変換可能なとき
                # それは，分子軌道係数なのでその値を，分子軌道の辞書に格納する
                orbitalDict[int(num[0])].append(float(data))

    # atomOrbitalNum = list(set(atomOrbitalNum))
    # print(atomOrbitalNum)
    pprint.pprint(orbitalDict)

if __name__ == "__main__":
    getExcitedStateParameters()
    # getOrbitInfo(True)
    # getOrbitInfo(False)
    en = getEigenValues()
    homo, lumo = getNumOrbitalHOMO_LUMO()
    print("homo eigenvalues->", en[homo-1])
    print("lumo eigenvalues->", en[lumo-1])

    # getOrbitalDetail()