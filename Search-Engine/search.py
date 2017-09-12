from __future__ import print_function
from nltk.stem.porter import PorterStemmer
import sys, operator
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
di = {"T":"title", "P":"page", "C":"category"}
docOffs = defaultdict(int)
with open('stopwords.txt','r') as file:
    GG = file.read().split('\n')
    for i in GG:
        KK = ps.stemWord(i) 
        if KK:stops[KK]=1
offS = 0
G=[]
with open('./title/allFiles') as FF:
    GG = FF.read().split('\n')
    for i in GG:
        G.append(offS)
        offS += len(i)+1
# print (G)
DOCS = defaultdict(float)
def func(query, directory):
    global DOCS
    for i in range(len(query)):
        word = query[i]
        off=-1
        word = ps.stemWord(word).lower()
        # print (word)
        if word not in stops:
            with open('./'+directory+'/offset.txt','r') as FF:
                GG = FF.read().split('\n')
                for kk in range(len(GG)):
                    F = GG[kk].split('|')
                    if len(F) > 1:
                        # print (F[0])
                        if word == F[0]:
                            try:off=int(F[1])
                            except: pass
        if off != -1:
            FF = open('./'+directory+'/final.txt','r')
            FF.seek(off)
            # print (FF.readline())
            # print (offSET[jj])
            line = FF.readline().split()
            # print (line)
            for i in range(1,len(line)):
                D1 = line[i].split('d')
                if len(D1) > 1:
                    D2 = D1[1].split('c')
                    if len(D2) > 1:
                        dd,cc = D2[0],float(D2[1])
                        DOCS[dd]+=(cc)
                        # if time.time() - start >= 0.003:break

    # ans = ''
    # for ii in range(min(10,len(DOCS))):
    #     FG = open('./title/allFiles','r')
    #     # print (DOCS[ii])
    #     FG.seek(G[int(DOCS[ii][0])])
    #     ans += (FG.readline())
    #     # print (G[int(DOCS[ii][0])-1])
    #     # print (DOCS[ii])
    #         # print (GO)
    #             # for kk in range(len(GO)):
    # # print (docOffs)
    # print (ans)

while 1:
    # print ('>>>')
    SSS = raw_input("search>")
    if SSS != "":
        start = time.time()
        query = SSS.split()
        DOCS = defaultdict(float)
        if ('T:' not in query[0]) and ('C:' not in query[0]) and ('P' not in query[0]):
            for i in range(len(query)):
                word = query[i]
                offSET = [-1,-1,-1]
                word = ps.stemWord(word).lower()
                # print (word)
                if word not in stops:
                    for jj in range(len(NAMES)):
                        with open('./'+NAMES[jj]+'/offset.txt','r') as FF:
                            GG = FF.read().split('\n')
                            for kk in range(len(GG)):
                                F = GG[kk].split('|')
                                if len(F) > 1:
                                    # print (F[0])
                                    if word == F[0]:
                                        try:offSET[jj]=int(F[1])
                                        except: pass
                for jj in range(len(offSET)):
                    if offSET[jj] != -1:
                        FF = open('./'+NAMES[jj]+'/final.txt','r')
                        FF.seek(offSET[jj])
                        # print (FF.readline())
                        # print (offSET[jj])
                        line = FF.readline().split()
                        # print (line)
                        for i in range(1,len(line)):
                            D1 = line[i].split('d')
                            if len(D1) > 1:
                                D2 = D1[1].split('c')
                                if len(D2) > 1:
                                    dd,cc = D2[0],float(D2[1])
                                    DOCS[dd]+=(cc)
                                    # if time.time() - start >= 0.003:break

            DOCS = sorted(DOCS.items(), key=operator.itemgetter(1))[::-1]
            ans = ''
            for ii in range(min(10,len(DOCS))):
                FG = open('./title/allFiles','r')
                # print (DOCS[ii])
                FG.seek(G[int(DOCS[ii][0])])
                ans += 'https://en.wikipedia.org/wiki/'+str(FG.readline()).replace(' ', '_')
                # print (G[int(DOCS[ii][0])-1])
                # print (DOCS[ii])
                    # print (GO)
                        # for kk in range(len(GO)):
            # print (docOffs)
            print (ans)
        else:
            for i in range(len(query)):
                DO = query[i].split(':')
                find = DO[1]
                FQ = DO[0]
                find = find.split()
                # print (FQ,find)
                func(find, di[FQ])
                # print (123)
                ans = ''
            ans = ''
            DOCS = sorted(DOCS.items(), key=operator.itemgetter(1))[::-1]

            for ii in range(min(10,len(DOCS))):
                FG = open('./title/allFiles','r')
                # print (DOCS[ii])
                FG.seek(G[int(DOCS[ii][0])])
                ans += 'https://en.wikipedia.org/wiki/'+str(FG.readline()).replace(' ', '_')
                # print (G[int(DOCS[ii][0])-1])
                # print (DOCS[ii])
                    # print (GO)
                        # for kk in range(len(GO)):
            # print (docOffs)
            print (ans)
    print (time.time() - start)