# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 20:11:02 2020

@author: Administrator
"""
#encoding=utf-8

import pandas as pd
import numpy as np
import jieba
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import re
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans,MeanShift
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from numpy import linspace
import random

plt.rcParams['font.sans-serif']=['SimHei'] 
plt.rcParams['axes.unicode_minus']=False
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 23:48:40 2020

@author: Kade
Crawler for shixiseng
"""
# -*- coding:utf-8 -*- 

import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

class SXCCrawer:
    
    def __init__(self):
        self.setParams(keyword='Python',area='',months='',days='',degree='',official='',salary='',publishTime='',city=['全国'])

    def HELP(self):
        
        publishDic = {
                'city':'职位发布时间',
                'day':'今天发布',
                'wek':'这周发布',
                'mon':'三十天内发布'
                }
        
        monDic = {
                'mon':'实习时间',
                '1':'一个月',
                '2':'两个月',
                '3':'三个月',
                '4':'三个月以上'
                }
        
        dayDic = {
                'day':'一周工作天数',
                '1':'1天',
                '2':'2天',
                '3':'3天',
                '4':'4天',
                '5':'5天',
                '6':'6天以上'
                }
        
        degreeDic = {
                'degree':'学历要求',
                '大专':'大专',
                '本科':'本科',
                '硕士':'硕士',
                '博士':'博士'
                }
        
        cityDic = {
                'city':'工作城市',
                '例子':'["武汉","北京"], downloader.setParams(city="武汉")'
                
                }
        
        keyDic = {
                'keyword':'职位关键字',
                '例子':'算法工程师/Python'
                }
        areaDic = {
                'area':'城市区域',
                '例子':'朝阳区'
                }
        
        salaryDic = {
                'salary':'日薪',
                '-0':'不限',
                '0-100':'0-100',
                '100-150':'100-150',
                '150-200':'150-200',
                '200-300':'200-300',
                '300-':'300以上'
                }
        
             
        dicList = [keyDic,cityDic,areaDic,publishDic,monDic,dayDic,degreeDic,salaryDic]
    
        for i in dicList:
            for j in i:
                print(j+':'+i[j])
            print('\n')
        
    def setParams(self,keyword='爬虫',area='',months='',days='',degree='',official='',salary='-0',publishTime='',city='全国'):
        self.__params = {
        'page':0,
        'keyword':'',
        'type':'intern',
        'area':'',
        'months':'',
        'days':'',
        'degree':'',
        'official':'',
        'enterprise':'',
        'salary':'',
        'publishTime':'',
        'sortType':'',    
        'city':'',
        'internExtend':''
        }
        
        self.__validation = {
                'city':[''],
                'keyword':[''],
                'area':[''],
                
                #发布时间
                'publishTime':['day','wek','mon'],
                
                #实习时长1个月，2个月，3个月，三个月以上
                'mon':['1','2','3','4'],
                
                #每周工作天数 1，2，3，4，5，6天以上
                'days':['1','2','3','4','5','6'],
                
                #学历要求
                'degree':['大专','本科','硕士','博士'],
                
                #日薪
                'salary':['-0','0-100','100-150','150-200','200-300','300-']
                }
        
        translation = {
                'keyword':'关键字',
                'city':'城市',
                'publishTime':'发布时间',
                'mon':'实习时常',
                'days':'每周工作天数',
                'degree':'学历',
                'salary':'日薪',
                'area':'区域'
                }
        
        self.__params['keyword'] = keyword
        self.__params['area'] = area
        self.__params['months'] = months
        self.__params['days'] = days
        self.__params['degree'] = degree
        self.__params['official'] = official
        self.__params['salary'] = salary
        self.__params['publishTime'] = publishTime
        self.__params['city'] = city
        
        print('当前抓取参数:')
        
        for i in self.__params:
            if i in self.__validation:
                print(i + ':' + str(self.__params[i]))
        print('\n')

        
    def __createDF(self):
        col_names =  ['title', 'jobDescrib', 'companyName','companyIndustry','companyType','companyScal','companyTage','companyLocation','jobUrl']
        df = pd.DataFrame(columns = col_names)
        self.__params['city'] = self.__cities
        path = './'+''.join([str(i) for i in self.__params.values()])+'.csv'
        df.to_csv(path_or_buf = path,encoding='GBK',index=False)
        return path
    
    def __saveJob(self,jobUrl,path):
        colNames =  ['title','jobDescrib','companyName','companyIndustry','companyType','companyScal','companyTage','companyLocation','jobUrl'] 
        df = pd.DataFrame(columns = colNames)
        dic = {}
        
        soup = self.__getSoup(jobUrl)
        
        try:
            title = soup.find(class_='new_job_name').get('title')
            jobDescrib = soup.find(class_='job_detail').text.replace('\n',' ').replace('\t',' ')
            jobDescrib = re.sub(' +',' ',jobDescrib)
            companyName = soup.find(class_='com-name').text.replace('\n','')  
            compDatil = list(soup.find(class_='com-detail').children)
            lenght = len(compDatil)
        except Exception as e:
            print(e)
            return
        
        companyIndustry = compDatil[1].text.replace('\n',' ').replace('/',' ') if lenght > 2 else ''
        companyType = compDatil[3].text if lenght > 4 else ''
        companyScal = compDatil[5].text.replace('\n',' ') if lenght > 6 else ''
        companyTage = soup.find(class_='com-tags').text.replace('\n',' ') 
        companyLocation = compDatil[7].text.replace('\n',' ') if lenght > 8 else ''
        
        dic['title'] = title
        dic['jobDescrib'] = jobDescrib 
        dic['companyName'] = companyName
        dic['companyIndustry'] = companyIndustry
        dic['companyType'] = companyType
        dic['companyScal'] = companyScal
        dic['companyTage'] = companyTage
        dic['companyLocation'] = companyLocation
        dic['jobUrl'] = jobUrl
            
        df = df.append(dic,ignore_index=True)
        
        try:
            df.to_csv(path_or_buf = path, mode="a+",index=False,header=None,encoding="GB18030")
        except Exception as e:
            print(e)
            print('写入失败')
        print(dic['title'],dic['companyName'])
        time.sleep(0.5)
            
            
    def __getJobFromPage(self,soup):
        if not soup: return []
        jobList = []
        allJob = soup.find_all(class_=['intern-wrap intern-item','intern-wrap intern-item is-view'])
        for job in allJob:             
            jobList.append(job.find(class_='title ellipsis font').get('href'))
        return jobList

    def __getUrlList(self,soup):
        
        def getPage(soup):
            pages = soup.find_all(class_='number')
            temp = []
            for i in pages:
                temp.append(i.text)
            return max(map(int,temp))
        
        numPage = getPage(soup)
        
        
        urlList = []
        for i in range(1,numPage+1):
            tempUrl = self.__getUrl(page=str(i))
            urlList.append(tempUrl) 
        return urlList
        
    def __getUrl(self,page=1):
        baseUrl = 'https://www.shixiseng.com/interns?'
        self.__params['page'] = page
        url = baseUrl + urlencode(self.__params)
        return url
    
        
    def __getSoup(self,baseUrl):
        headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,en-AU;q=0.8,en;q=0.7',
                'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                'referer': 'https://www.shixiseng.com/interns?page=1&keyword=%E7%88%AC%E8%99%AB&type=intern&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%8C%97%E4%BA%AC&internExtend='
                }
        try:
           r = requests.get(baseUrl,headers=headers)
           r.encoding = 'utf-8'
           content = BeautifulSoup(r.text,"html.parser")
           return content
        except Exception as e:
            return None
            print(e)
            
    def __getAllUrl(self):
        self.__cities = self.__params['city']
        self.__urlList = []
        for city in self.__cities:
            self.__params['city'] = city
            url = self.__getUrl()
            soup = self.__getSoup(url)
            self.__urlList.extend(self.__getUrlList(soup))

    
    def run(self):
        
        self.__getAllUrl()  
        self.path = self.__createDF()
        nums = pages = 0
        
        print('number of page:',len(self.__urlList))
        

        for url in self.__urlList:
            soup = self.__getSoup(url)
            jobList = self.__getJobFromPage(soup)

            for job in jobList:
                nums += 1
                self.__saveJob(job,self.path)
            pages += 1
            
            print('第%d页数据已抓取完毕。'%(pages),'='*50,'\n')
#        print('你小子抓了%d条数据，等着坐牢吧你。'%(nums))
        self.__params.pop('page')
        


class SXSAnalyser:
    
    def __init__(self,path,userDict='./dict.txt',stopWords='./stopwords/sum.txt'):
        self.__path = path
        self.__df = pd.read_csv(filepath_or_buffer=path,engine='python')
        jieba.load_userdict(userDict)
        stopWords = np.array(pd.read_csv(filepath_or_buffer=stopWords,header=None)).T.tolist()[0]
        
        self.__DeRedundancy()
        self.__RemoveStopWords(stopWords)
        self.__getWordFrequency()
        self.prapaerData()
        
    def __saveImag(self,plt,name):
        path = './image/' + self.__path[2:-4] + name + '.jpg'
        print(path)
        if name != '3D':
            plt.savefig(path,bbox_inches='tight')
        else:
            pass
        
    
    def prapaerData(self,select = 100,minCount = 10):
        self.__showWords = self.__wordsSelector(select,minCount)
        self.__wordVector = self.__getwordVec(self.__showWords)
        
        
    #数据去重
    def __DeRedundancy(self):
        self.__df.dropna(subset=['jobUrl'],inplace=True)
        self.__df.fillna(value='',inplace=True)
        self.__df.drop_duplicates(['title','companyName','jobDescrib'],inplace = True)
        self.__df.index = range(len(self.__df))

    #预处理，删除 stop words
    def __RemoveStopWords(self,stopWord):
        self.__df['jobDescrib'] = self.__df['jobDescrib'].apply(lambda x:re.sub('�0|�1|�6|�2|[【】◆]','',x.lower()))
        self.__df['title'] = self.__df['title'].apply(lambda x:re.sub('�0|�1|�6|�2|[【】◆]','',x.lower()))
        self.__df['titleWord'] = self.__df['title'].apply(lambda x:[i for i in jieba.lcut(x) if len(i)>=2 ])
        self.__df['jobDesWord'] = self.__df['jobDescrib'].apply(lambda x:[i for i in jieba.lcut(x) if len(i)>=2 and i not in stopWord])


    # 计算词频
    def __getWordFrequency(self):
        wordDf = pd.DataFrame({'Word':np.concatenate(self.__df.jobDesWord)})
        wordStat = wordDf.groupby(by=['Word'])["Word"].agg({'number':np.size})
        self._wordStat = wordStat.reset_index().sort_values(by='number',ascending=False)


    def __wordsSelector(self,select,minCount):
        #根据数字选择
        wordStat2 = self._wordStat.loc[self._wordStat['number'] >= minCount]
        if select < 1:
            num = int(len(wordStat2)*select)
        else:
            num = select
        wordStat3 = wordStat2.head(num)
        showWord = np.array(wordStat3['Word']).tolist()
        return showWord

    
    def __getwordVec(self,showWord):
        SentenceList = np.array(self.__df.jobDesWord).T.tolist()
        self._model = Word2Vec(SentenceList,min_count=10)
        wordVec = self._model.wv[showWord]
        return wordVec
    
    
    def draw2D(self):
        model = TSNE(n_components=2)
        result = model.fit_transform(self.__wordVector)

        model = MeanShift(2)
        lable = model.fit_predict(result)
        cm_subsection = linspace(0,1,10)
        colors = [cm.rainbow(x) for x in cm_subsection]
        random.shuffle(colors)

        fig = plt.figure(figsize=(20,12))
        for i,word in enumerate(self.__showWords):
                plt.scatter(result[i,0],result[i,1],color = colors[lable[i]])
                plt.annotate(word,xy=(result[i,0],result[i,1]))
        fig.show()
        

        self.__saveImag(plt,'2D')
        
    def draw3D(self):
        model = PCA(n_components=3)
        result = model.fit_transform(self.__wordVector)
        
        ax = plt.axes(projection='3d')
        fig = plt.figure()
        ax = Axes3D(fig)

        for i,word in enumerate(self.__showWords):
                ax.scatter3D(result[i,0],result[i,1],result[i,2])
                ax.text(result[i,0],result[i,1],result[i,2],word)
        self.__saveImag(ax,'3D')
    
    def drawCloud(self):
        wordList= ''

        word = np.array(self._wordStat['Word']).tolist()
        nums = np.array(self._wordStat['number']).tolist()
        fig = plt.figure(figsize=(20,12))
        
        for i in range(len(nums)):
            wordList += (word[i] + ' ')*nums[i]
    
        wordcloud = WordCloud(collocations=False,scale=8,font_path='simhei.ttf',background_color='white').generate(wordList)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        fig.show()
        self.__saveImag(plt,'wordCloud')
        
    
    def drawBar(self,nums=35):
        pltData = self._wordStat.head(nums)
        fig = plt.figure(figsize=(20,12))

        plt.xlabel('关键字')
        plt.ylabel('出现次数')
        plt.title('招聘关键字分析')
        plt.xticks(rotation = 45)
        plt.bar(pltData['Word'],pltData['number'])
        fig.show()
        self.__saveImag(plt,'BarChart')
                
