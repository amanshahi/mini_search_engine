from __future__ import print_function
from nltk.stem.porter import PorterStemmer
import sys
import bz2, math
import heapq
import xml.etree.ElementTree as etree
import codecs
import csv
import time
import os,re
from collections import *
import sys
from Stemmer import Stemmer as PyStemmer
reload(sys)
sys.setdefaultencoding('utf-8')
C=defaultdict(list)
ps = PyStemmer('porter')
stops={}
pageNum=1
ofST=[0,0,0]
NAMES=['title', 'page', 'category']
try:
    os.remove('./title/allFiles')
    os.remove('./title/offset.txt')
    os.remove('./page/offset.txt')
    os.remove('./category/offset.txt')
    os.remove('./title/final.txt')
    os.remove('./page/final.txt')
    os.remove('./category/final.txt')

except: pass    
with open('stopwords.txt','r') as file:
    GG = file.read().split('\n')
    for i in GG:
        KK = ps.stemWord(i) 
        if KK:stops[KK]=1
def strip_tag_name(t):
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

def writeIntoFile(pathOfFolder, index, countFinalFile):                                        
    data=[]                                                                             #write the primary index
    
    for key in sorted(index):
        string= str(key)+' '
        temp=index[key]
        if len(temp) != 0:
            idf = math.log(pageNum/float(len(temp)))
        for i in range(len(temp)):
            S1=temp[i].split('d')
            # print (S1)  
            if len(S1) > 1:
                S2=S1[1].split('c')
                DD,CC = S2[0], int(S2[1])
                GG = (1+math.log(CC))*idf
                GG = ("%.2f" % GG)
                string += 'd'+DD+'c'+str(GG) + ' '
        # string+=' '.join(temp)
        data.append(string)
        FFGL = open(pathOfFolder + '/offset.txt','a')
        print (str(key)+'|'+str(ofST[NAMES.index(pathOfFolder[2:])]), file=FFGL)
        ofST[NAMES.index(pathOfFolder[2:])] += len(string)+1

    filename=pathOfFolder+'/final.txt'                            #compress and write into file
    with open(filename, 'a') as f:
        f.write('\n'.join(data))
    return countFinalFile+1

def mergeFiles(pathOfFolder, countFile, typed):                                                 #merge multiple primary indexes
    listOfWords={}
    indexFile={}
    topOfFile={}
    flag=[0]*countFile
    data=defaultdict(list)
    heap=[]
    countFinalFile=0
    offsetSize = 0
    for i in xrange(countFile):
        fileName = pathOfFolder+'/'+typed+str(i)
        indexFile[i]= open(fileName, 'rb')
        flag[i]=1
        topOfFile[i]=indexFile[i].readline().strip()
        listOfWords[i] = topOfFile[i].split(':')
        if listOfWords[i][0] not in heap:
            heapq.heappush(heap, listOfWords[i][0])        

    count=0        
    while any(flag)==1:
        temp = heapq.heappop(heap)
        count+=1
        for i in xrange(countFile):
            if flag[i]:
                if listOfWords[i][0]==temp:
                    data[temp].extend(listOfWords[i][1:])
                    if count==1000000:
                        oldCountFile=countFinalFile
                        countFinalFile = writeIntoFile(pathOfFolder, data, countFinalFile)
                        if oldCountFile!=  countFinalFile:
                            data=defaultdict(list)
                        
                    topOfFile[i]=indexFile[i].readline().strip()   
                    if topOfFile[i]=='':
                            flag[i]=0
                            indexFile[i].close()
                            os.remove(pathOfFolder+'/'+typed+str(i))
                    else:
                        listOfWords[i] = topOfFile[i].split(':')
                        if listOfWords[i][0] not in heap:
                            heapq.heappush(heap, listOfWords[i][0])
    countFinalFile = writeIntoFile(pathOfFolder, data,countFinalFile)

AG = sys.argv
pathWikiXML = AG[1]
FILE1 = open(AG[2], 'w')
extract = {'title':0, 'text':1, 'Category':2}
INFO = ['t', 'p', 'C']

TEMP = defaultdict(int)
ARR = [defaultdict(int) for i in range(3)]
arr = [defaultdict(list) for i in range(3)]
C1,C2,D=defaultdict(int),defaultdict(int),{}
fileCount=[0,0,0]
fileSize = 2000
titL=[]
X=0
pageNum1=0
for event, elem in etree.iterparse(pathWikiXML, events=('start', 'end')):
    tname = strip_tag_name(elem.tag)
    if tname == 'page' and event == 'end':
        for i in D:
            sf='d' + str(pageNum)
            for j in range(3):
                if ARR[j][i] != 0:
                    sf+= INFO[j] + str(ARR[j][i])
                    # print (arr[j][i])
                    arr[j][i].append('d'+str(pageNum)+'c'+str(ARR[j][i]))
                    # print (arr[j][i])
            C[i].append(sf)
        ARR = [defaultdict(int) for i in range(3)]
        D={}
        pageNum += 1 
        pageNum1 += 1 
        elem.clear()
    if tname == 'text' and event == 'end':
        ST = re.findall("\[\[Category:(.*?)\]\]",str(elem.text))
        if ST :
            for i in ST :
                if i:
                    i = i.lower()
                    for jj in i.split():
                        jj = jj.lower()
                        jj = ps.stemWord(jj)
                        if jj not in stops:
                    # arr[extract['Category']][TX]+=1
                            # print (jj)
                            ARR[extract['Category']][jj] += 1       
                            D[jj]=1
    # if tname == 'title': 
    if tname in extract and event == 'end':
        if tname == 'title': 
            # print (str(elem.text))
            if str(elem.text) is not None:
                # print (str(elem.text))
                titL.append([str(elem.text),pageNum])
        for i in re.split('[^A-Za-z]',str(elem.text) ):
            if i:
                # if tname == 'title': print (i)
                i=i.lower()
                ST = ps.stemWord(i)
                if ST not in stops:
                    if ST:
                        # print (ST)
                        # if tname == 'title': print (ST)
                        # arr[extract[tname]][ST]+=1
                        ARR[extract[tname]][ST]+=1
                        D[ST]=1
    if pageNum1==fileSize:
        for i in range(len(arr)):
            s=''
            directory=NAMES[i]
            # print (directory)
            if not os.path.exists('./'+directory):
                os.makedirs('./'+directory)
            FILE=open('./'+directory+'/'+INFO[i]+str(fileCount[i]),'w')
            D1=sorted(arr[i])
            for j in D1:
                s+=j;
                for k in arr[i][j]:
                    s+=':'+str(k)
                s+='\n'
            # print (s,X)
            print(s,file=FILE)
            FILE.close()
            # arr[i]=defaultdict(int)
            # print (len(arr[i]))
            fileCount[i]+=1
        arr = [defaultdict(list) for i in range(3)]

        pageNum1=0
        # with open('./title/allFiles','a') as FILE:
        #     for i in titL:
        #         if i is not None:
        #             print (i)
        #             # FILE.write(i+'\n')
        #             print(i,file=FILE)
        FILE=open('./title/allFiles','a')
        # print ('\n'.join(titL))
        SS=""
        for i in range(len(titL)):
            SS+=str(titL[i][0])+'\n'
        # print (SS)
        print(SS, file=FILE)
        FILE.close()             
        titL=[]

    # elem.clear()

if pageNum1 != 0:
    for i in range(len(arr)):
        s=''
        directory=NAMES[i]
        # print (directory)
        if not os.path.exists('./'+directory):
            os.makedirs('./'+directory)
        FILE=open('./'+directory+'/'+INFO[i]+str(fileCount[i]),'w')
        D1=sorted(arr[i])
        for j in D1:
            s+=j;
            for k in arr[i][j]:
                s+=':'+str(k)
            s+='\n'
        # print (s,X)
        print(s,file=FILE)
        FILE.close()
        # arr[i]=defaultdict(int)
        # print (len(arr[i]))
        fileCount[i]+=1
    arr = [defaultdict(list) for i in range(3)]
    FILE=open('./title/allFiles','a')
    # print ('\n'.join(titL))
    SS=""
    for i in range(len(titL)):
        SS+=str(titL[i][0])+'\n'
    # print (SS)
    print(SS, file=FILE)
    FILE.close()             
    titL=[]
    pageNum1=0

for i in range(len(NAMES)):
    mergeFiles('./'+NAMES[i],fileCount[i],INFO[i])
    # if X == 1: break
# for i in sorted(C):
#     s=i+':'
#     for j in C[i]:
#         s+=j+'|'
#     print(s, file=FILE)

# for i in range(len(arr)):
# print (arr[0])

# for i in range(len(NAMES)):
#     DD = []
#     with open('./'+NAMES[i]+'/'+'final.txt', 'r') as FF:
#         GFG = FF.read().split('\n')
#         for j in range(len(GFG)):
#             FF = GFG.split()
#             DD.append([FF[0], ])
