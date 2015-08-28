# -*- coding: utf-8 -*- 
#slb@slb.moe


import os
import sys
import re
import subprocess as sbp
import shutil

readme=\
u"""
人家的用法是~:

    1.把要批量重命名的文件或文件夾放到同一個"文件夾A"下

    2.保證這些文件的名稱按照0~9a~z自然排列的結果是符合你的預期的

    3.把"文件夾A"命名為你希望批量重命名的名稱
      其中的序號的位置用###01代替
      ###01 只能出現一次
      數字代表起始的序號
      而數字的長度則代表序號的最小長度 不足的位會用0填充
      比如:
      [KNA][FSN_UBW][###1][720p][rev][x264_AAC][cht]
      [KNA][FSN_UBW][###01][720p][rev][x264_AAC][cht]
      [KNA][FSN_UBW][###001][720p][rev][x264_AAC][cht]
      [KNA][FSN_UBW][###213][720p][rev][x264_AAC][cht]
      根據情況 這四個名稱的效果都是不盡相同的

    4.把"文件夾A"拖到本exe文件上

    ps:
      如果文件夾中有視頻文件和與其對應的同名字幕文件 是可以正確識別處理的
      但字幕文件與視頻文件的文件名必須嚴格對應 除擴展名外一字不差
      如果并不對應 建議放到不同文件夾中分開處理
      強行處理的話 識別出錯會把名稱弄亂 到時候不要來怪我!
      可以一次拖多個文件夾進去喔~
                                                        slb@slb.moe
    =====================================================================

    X.為應付某些奇葩狀況:
      如果將"文件夾A"末尾加上.noextXXX
      則會將"文件夾A"下面子項末尾的.XXX不作為擴展名處理
      例如:

        "文件夾A"名稱為:
        Example.Name.###01.BluRay
        下面有子項:
        7500.2014.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-RARBG
        一般情況下 會被錯誤的重命名為:
        Example.Name.01.BluRay.1-RARBG

        若將"文件夾A"命名為:
        Example.Name.#01.BluRay.noext1-RARBG
        則以上文件會被正確的重命名為:
        Example.Name.01.BluRay

    Y.另一種更奇葩的狀況:

        "文件夾A"名稱為:
        Example.Name.###01
        其下有文件":
        .part1
        .part2
        .part3
        .part4

        這時你需要將"文件夾A"命名為
        Example.Name.###01.7z.forceextABCD
        那麼這些文件將會正被正確的命名為
        Example.Name.01.ABCD
        Example.Name.02.ABCD
        Example.Name.03.ABCD
        Example.Name.04.ABCD

        ※※※
        這種情況下將無法正確處理視頻文件附帶同名字幕文件類似的狀況
        請分開處理 勿強行裝逼
"""











def gocmd(CMD,CWD=None):
    c = sbp.Popen(CMD, cwd=CWD, shell=True, stdout=sbp.PIPE, stderr=sbp.PIPE)
    out = c.stdout.read() + "\n" + c.stderr.read()
    try:
        out = out.decode("mbcs")
    except:
        pass
    print out

def pause():
    print u"要繼續就按回車哦"
    raw_input("")



def rename(fl,tn):

    noext = None
    forceext = None
    try:
        fn = tn.split(u".")
        ne = fn[-1]
        if ne[:5] == u"noext":
            noext = u"." + ne[5:]
            tn = ".".join(fn[:-1])
        if ne[:8] == u"forceext":
            forceext = u"." + ne[8:]
            tn = ".".join(fn[:-1])
    except:
        pass
    
    rexp = ur"###\d{1,}"
    number = re.search(rexp,tn).group()[3:]
    lennumber = len(number)
    number = int(number) - 1

    fl.sort()
    rntl = []
    tmp = None
    mf = 0
    nc = number+1
    for i in fl:
        mf += 1
        nae = os.path.splitext(i)
        if nae[1] == noext:
            nae = ( nae[0]+nae[1] , u"" )
        if forceext:
            nae = ( nae[0]+nae[1] , u"" , forceext )
        nae = list(nae)
        if nae[0] != tmp:
            tmp = nae[0]
            number += 1
        on = nae[0] + nae[1]
        nn = re.sub(rexp, str(number).decode("mbcs").zfill(lennumber), tn) + nae[1]
        if len(nae) > 2:
            nn = nn + nae[2]
        rnt = ( on , nn )
        rntl.append(rnt)
    print u"其中中共有 " + str(mf).decode("mbcs") +u" 個文件"
    print u"序號將從 " + str(nc).decode("mbcs").zfill(lennumber) + u" 增長至 " + str(number).decode("mbcs").zfill(lennumber)

    try:
        cmd = ur"mkdir renamed".encode("mbcs")
        gocmd(cmd)
    except:
        pass

    for i in rntl:
        oldname = i[0]

        newname = os.path.join(ur"renamed" , i[1])
        cmd = [ur"move".encode("mbcs"),oldname.encode("mbcs"),newname.encode("mbcs")]

        cwd = os.getcwd()
        print cmd[1] + u"\n將被重命名為\n".encode("mbcs") + cmd[2]
        gocmd(cmd)

    if not os.listdir(ur"renamed".encode("mbcs")):
        shutil.rmtree(ur"renamed".encode("mbcs"))

    print "================================================="
    pass



def checkdir(path):
    print u"正在處理..."
    print path + u"\n"
    tn = os.path.split(path)[1]
    rexp = re.compile(ur"###\d{1,}")
    tmp = rexp.findall(tn)
    if not len(tmp)==1:
        print u"###01之類的序號標記在文件夾名中必須有且只有一個!!!"
        print u"而以下文件夾名稱與此不符"
        print tn
        print "========================================"
        pause()
        return

    os.chdir(path.encode("mbcs"))
    l = os.listdir(".")
    fl = []
    dl = []
    for i in l:
        if os.path.isfile(i):
            fl.append(i.decode("mbcs"))
        if os.path.isdir(i):
            dl.append(i.decode("mbcs"))

    if dl and fl:
        print u"又有文件夾又有文件是什麼鬼!?\n人家只會處理只有文件夾或只有文件的狀況啦!!\n"
        pause()
        return

    fl.extend(dl)
    if ur"renamed" in fl:
        print u'"renamed"是什麼鬼 快把他移走啦! 我才不處理這種麻煩事情呢!'
        pause()
        return

    rename(fl, tn)




def check_input():
    if len(sys.argv)>1:
        l = sys.argv[1:]
        lp = []
        for i in l:
            if os.path.isdir(i):
                lp.append(i.decode("mbcs"))
    else:
        return 0
    return lp


if __name__ == '__main__':

    l = check_input()
    if l:
        print u"現在將會開始處理下面這些路徑:\n"
        for i in l:
            print i
            print "\n"
        pause()
        print "========================================"
        for i in l :
            checkdir(i)
        pause()
    
    else:
        print readme
        pause()











