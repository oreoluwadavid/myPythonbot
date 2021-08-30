 # -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 15:01:28 2021

@author: user
"""
import numpy as np
import pandas as pd
from  sklearn import *
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import random
import datetime
import math
from scipy.stats import linregress
import requests
import yfinance as yf
#import statsmodels.api as sm
def check_equal(gh):
    amount=len(gh.columns)
    items=[]
    disdata=pd.DataFrame(index=gh.index)
    for item in gh.columns:
        item=item.strip("")
        items.append(item)
        b=gh[item]
        try:
            for i in range(amount):
                a=gh[items[i]]
                disdata["value"]=np.where(np.equal(disdata["value"],b),disdata["value"],0)
        except:
            c=b
            disdata["value"]=c
            
    return disdata["value"]
def listsplit(list1:list,n:int):
    list2=[]
    p=0
    for item in list1:
        if p<=n:
            list2.append(item)
        else:
            continue
        p+=1
    return list2
def check_greater(gh):
    amount=len(gh.columns)
    items=[]
    disdata=pd.DataFrame(index=gh.index)
    for item in gh.columns:
        item=item.strip("")
        items.append(item)
        b=gh[item]
        try:
            for i in range(amount):
                a=gh[items[i]]
                disdata["value"]=np.where(np.greater(disdata["value"],b),disdata["value"],0)
        except:
            c=b
            disdata["value"]=c
            
    return disdata["value"]
def list_to_str_float_list(lis1:list)->list:
    """
    

    Parameters
    ----------
    lis1 : list
        DESCRIPTION.Takes a stringed list

    Returns
    -------
    list
        DESCRIPTION. A floated list

    """
    lis2=[]
    for items in lis1:
        if items==str:
            a=float(items.split('-')[2].split(' ')[4].split('N')[0])
            lis2.append(a)
        else:
            return lis1
        
    return lis2
def extracts(df,largest,key)->list:
    start=0
    lirt=[]
    while start<largest:
        val=df[key].iloc[start]
        val=eval(val)
        lirt.append(val)
        start+=1
    return lirt
def list_taker(n,j:list,k:"output"):
    if k=="output":
        try:
            return j[0][n]
    
        except:
            return j[n]
    else:
        k=[]
        for i in range(len(j)):
            if j[i]==n:
                k.append(i)
        return k
            
def list_extractor(lis:list):
    #Code to extract list 
    buy=[]
    sell=[]
    for i in range(len(lis)):
        j=0
        for n in lis[i]:
            x=lis[i][j]
            if x!=0 and j==0:
                buy.append(x)
            elif x!=0 and j!=0:
                sell.append(x)
            else:
                j+=1
    return buy,sell
def list_duplicate(lis1:list):
    #Code to remove duplicates
    temp_list=[]
    for i in lis1:
        if i not in temp_list:
            temp_list.append(i)
    lis1=temp_list
    return lis1

def multitimes(lisl:list):
    times=[]
    values=[]
    dic={}
    n=0
    for i in lisl:
        position=list_taker(i,lisl,k="in")
        if values[n]!=i:
            times.append(len(position))
            values.append(i)
            n+=1
            #dic={values:times}
            dic['pos']=position
                
    values=set(values)
    print("values:%2c and times:%2c",(values,times))
    #print("")
    #return values,times
    
def chunk_based_on_no(lst,chunk_no):
	n=math.ceil(len(lst)/chunk_no)
	for x in range(0,len(lst),n):
		each_chunk=lst[x:n+x]
		if len(each_chunk)<n:
			each_chunk=each_chunk+[None for y in range(n-len(each_chunk))]
		yield each_chunk
def removzerset(values,lisl:list):
    """Function to remove a values from list"""
    times=list_taker(values,j=lisl,k='in')
    m=0
    try:
        
        for  i in range(len(times)):    
            lisl.remove(values)
            m+=1
    except:
        """if m>0:
            return lisl
        else:
            pass"""
        return lisl

def pd_editzero(pdli:pd.DataFrame,x:str='price_sold',y:str='price_bought'):
    """
    

    Parameters
    ----------
    pdli : pd.DataFrame
        DESCRIPTION.
    x : str, optional
        DESCRIPTION. The default is 'price_sold'.
    y : str, optional
        DESCRIPTION. The default is 'price_bought'.

    Returns
    -------
    TYPE
    sell,buy
        DESCRIPTION.

    """
    try:
        sell=pdli[x].values.tolist()
        buy=pdli[y].values.tolist()
        removzerset(0,sell)
        removzerset(0,buy)
        return sell,buy
    except:
        if x=="price_sold" and y!="price_bought":
            hu=pdli[y].values.tolist()
            return hu
        elif x!="price_sold" and y=="price_bought":
            hu=pdli[x].values.tolist()
            return hu
        else:
            sell=pdli[x].values.tolist()
            buy=pdli[y].values.tolist()
            removzerset(0,sell)
            removzerset(0,buy)
            return sell,buy
   
     
                
def dataframetor(lis1:list,lis2:list):
    #Code to maintain data shape by adding zero
    #lis1=list_duplicate(lis1)
    #lis2=list_duplicate(lis2)
    while len(lis1)!=len(lis2):
        if len(lis1)<len(lis2):
            lis1.append(0)
        elif len(lis1)>len(lis2):
            lis2.append(0)
    return lis1,lis2

def range_concencutive(lisl:list):
    """
    

    Parameters
    ----------
    lisl : list
        DESCRIPTION.
        Performs last and some other functions
    Returns
    -------
    An int.
    """
    amount=list_taker(0,j=lisl,k="in")
    number=[]
    length=lisl.__len__()
    rangel=[]
    for items in range(len(amount)):
        list_value=amount[items]
        item1=list_value-1
        item2=list_value+1
        if item1>=0 and item2<length:
            rangel.append(item1)
            rangel.append(item2)
    for items in range(length):
        net=0
        if items not in amount:
            net+=1
        if net!=0:
            number.append(net)
    return sum(number)
                

def errorcashtester(fd:pd.DataFrame):
    #Code to create a error checking block of code
    price_bought=fd['Price_bought']
    price_sold=fd['Price_sold']
    prof=price_sold-price_bought
    cash=0.2*prof
    net=prof-cash
    cap=1000+net
    ret=price_sold-(cash+price_bought)
    kit=CashflowStatementBot(initial_capital=1000.0,price_bought=fd['Price_bought'],price_sold=fd['Price_sold']).loop()
    if np.where(np.equal(price_bought,kit.expense)):
        print("Successful testing of expense!!!")
        pass
    else:
        print("The expense is not the same with price_bought,i.e it is having probs")
        quit()
    if np.where(np.equal(prof,kit.grossprofit)):
        print("Successful tesing of profit!!!")
        pass
    else:
        print("The grossprofit is not the same with expected profit check it")
        quit()
    if np.where(np.equal(cash,kit.cashflow)):
        print("Successful testing!!! Cashflow")
        pass
    elif np.where(np.less(cash,0),np.equal(kit.cashflow,0)):
        print("Successful test!!! Cashflow")
        pass
    else:
        print("The expected cashflow is problematic")
        quit()
    if np.where(np.equal(cap,kit.capital)):
        print("Successful test!!! Capital")
        pass
    else:
        print("The cap is not equal to capital check")
        quit()
    if np.where(np.equal(ret,kit.returns)):
        print("Successful testing !!! Returns")
        pass
    else:
        print("The returns is problematic")
        quit()
    print(price_bought-kit.expense)
    print(prof-kit.grossprofit)
    print(cash-kit.cashflow)
    print(cap-kit.capital)
    print(ret-kit.returns)
def isgreatest(linl:list,hin:str="max"):
    #Function to find the largest items in a list
    """
    Parameter: A list
    Result: The smallest or largest item 
    """
    linl.sort()
    if hin=='max':
        m=False
    else:
        m=True
    c=0
    for a in linl:
        e=[]
        f=[]
        for b in linl:
            d=a<b
            i=a>b
            e.append(d)
            f.append(i)
        if list_taker(n=False,j=e,k="in").__len__()==len(linl) and m==False:
            c=a
        elif list_taker(n=False,j=f,k="in").__len__()==len(linl) and m==True:
            c=a
            
    return c
            



    
        
def pplot(x,y:int):
   
    plt.plot(x,label=y,grid=True)
    
               

    
    
def values():
    """initial_capital=float(input('initial_capital:'))
    commision=float(input('commision/charges:'))
    price_sold=float(input('income:'))
    price_bought=float(input('expense:'))
    data_amount=float(input('cost of data:'))
    return initial_capital,commision,price_bought,price_sold,data_amount"""
    initial_capital=random.uniform(0.000,10000.0000)
    commision=random.uniform(0.000,100000.000)
    price_sold=random.uniform(0.000,100000.000)
    price_bought=random.uniform(0.000,10000.000)
    data_amount=random.uniform(0.000,100000.000)
    return initial_capital,commision,price_bought,price_sold,data_amount
       
def get(tickers,startdate,enddate):
    def data(ticker):
        return (pdr.get_data_yahoo(ticker,start=startdate,end=enddate))
    datas=map(data,tickers)
    return(pd.concat(datas,keys=tickers,names=['Ticker','Date']))
    
    

def last(k:list):
    if type(k)==list:
        n=k.__len__()
        return k[n-1]
    elif type(k)==pd.core.frame.DataFrame or type(k)==pd.core.series.Series:
        try:
            list1=k.tail(1)
            list1=last(list1.to_numpy().tolist())
            n=last(list1)
            return n
        except:
            print("Not found")





def check_equal(gh):
    amount=len(gh.columns)
    items=[]
    disdata=pd.DataFrame(index=gh.index)
    for item in gh.columns:
        item=item.strip("")
        items.append(item)
        b=gh[item]
        try:
            for i in range(amount):
                a=gh[items[i]]
                disdata["value"]=np.where(np.equal(disdata["value"],b),disdata["value"],0)
        except:
            c=b
            disdata["value"]=c
            
    return disdata["value"]
"""def list_taker(n,j:list,k:"output"):
    if k=="output":
        try:
            return j[0][n]
    
        except:
            return j[n]
    else:
        k=[]
        for i in range(len(j)):
            if j[i]==n:
                k.append(i)
        return k"""

 
class Ranking(object):
    def __init__(self,average_window=0):
        self.window=average_window
        pass
    def pct_change(self,_input_):
        data=_input_.pct_change()
        return data.sum()
    def last_average(self,_input_):
        uio=0
        data=pd.DataFrame(index=_input_.index)
        data2=[]
        while uio<(len(_input_)-self.window):
            data2.append(list_taker(n=uio,j=_input_.index,k="output"))
            uio+=1
        data["value"]=_input_.drop(data2)
        remove=data["value"]
        upo=remove.dropna()
        value=(upo.sum()/self.window)
        return value
                
    def moving_average(self,_input_):
        uio=0
        data=pd.DataFrame(index=_input_.index)
        data2=[]
        while uio<(len(_input_)-self.window):
            data2.append(list_taker(n=uio,j=_input_.index,k="output"))
            uio+=1
        data["value"]=_input_.drop(data2)
        remove=data["value"]
        upo=remove.dropna()
        value=SimpleMovingAverage(self.window).output_(upo)
        return value.sum()
        
    def rating(self,_input_):
        _input_=_input_.rank(ascending=True)
        #_input_=_input_.sort_value(inplace=True,ascending=False)
        return _input_  
        
class Timer(object):
    """This class is to manipulate,check ime and all"""
    def __init__(self,days,#String containing dates
                 hours#String containing times
                 ):
        #To initialize objects
        self.days=days
        self.hours=hours 
        self.day=datetime.date(year=self.days[0],month=self.days[1],day=self.days[2])
        self.time=datetime.time(hour=self.hours[0],minute=self.hours[1],second=self.hours[2])
        pass
    def check_time(self):
        #This code is to check the time
        time_day=datetime.datetime.today()
        self.split=time_day.hour
        return self.split
        pass
    def check_date(self):
        #This code is to check the day
        time_day=datetime.datetime.today()
        self.today=time_day
        return self.today
    def date_diff(self):
        diffyear=int(self.today.year)-self.days[0]
        diffmonth=int(self.today.month)-self.days[1]
        diffday=365*diffyear+31*diffmonth+int(self.today.day)-self.days[2]
        return diffday

    def date_diff_accurate(self,eam):
        if eam==0:
            eam=[self.today.year,self.today.month,self.today.day]
            date1=self.today
        if type(eam)==list:
            eam=datetime.date(year=eam[0],month=eam[1],day=eam[2])
            date1=eam
            eam=[date1.year,date1.month,date1.day]
        diffyear=int(eam[0])-self.days[0]
        diffmonth=int(eam[1])-self.days[1]
        date2=self.day
        day1_for=datetime.date.strftime(date1,"%a,%b,%y,%m,%d")
        day2_for=datetime.date.strftime(date2,"%a,%b,%y,%m,%d")
        def month_monitor(month,n):
            no=0
            for i in range(n):
                month+=1
                if month==2:
                    no+=28
                if (month==4 or month==6 or month==9 or month==11):
                    no+=30
                if (month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):
                    no+=31
                if month==12:
                    month=0
            return no
        yeardiff=month_monitor(month=self.days[1],n=12)*diffyear
        monthdiff=month_monitor(month=self.days[1],n=diffmonth)
        print(day1_for,day2_for)
        #print(diffyear,diffmonth,yeardiff,monthdiff)
        diffday=yeardiff+monthdiff+(int(date1.day)-self.days[2])
        return diffday


def counter(item:list):
    o=0
    for i in item:
        o+=1
    return o 

#Defining available shares
tickers=['AAPL','MSFT','IBM','GOOG']
#all_data=get(tickers,datetime.datetime(2015,10,1),datetime.datetime(2021,4,1))




returnsk=[0.0]
class CashflowStatementBot(object):
    def __init__(self,initial_capital,commision=0.0,price_bought=0.0,price_sold=0.0,data_amount=0.0):
        self.initial_capital=initial_capital
        self.commision=commision
        self.price_bought=price_bought
        self.price_sold=price_sold
        self.data_amount=data_amount
        self.last_capital=[]
        #super().__init__(initial_capital,commision,price_bought,price_sold,data_amount)
    def _calc_expense(self):
        self.data=pd.DataFrame(index=self.price_bought.index)
        self.data['expense']=self.price_bought+self.data_amount+self.commision
        self.last_capital.append(self.initial_capital)
        return self.data['expense']
    def _calc_profit(self):
        self.price_bought=np.where(np.greater(self.price_bought,last(self.last_capital)),0,self.price_bought)
        self.price_sold=np.where(np.equal(self.price_bought,0),0,self.price_sold)
        self.data["expense"]=np.where(np.equal(self.price_bought,0),0,self.data["expense"])
        self.data['grossprofit']=self.price_sold-self.data['expense']
        self.data['cashflow']=0.2*self.data['grossprofit']
        self.data['cashflow']=np.where(np.less(self.data['cashflow'],0),0,self.data['cashflow'])
        n=self.data.index.values.tolist()
    
        self.data['netprofit']=self.data['grossprofit']-(self.data['cashflow'])
        self.data['capital']=self.return_capital()
        self.data['returns']=self.price_sold-self.data['cashflow']-self.data['capital']
        print('capital is',self.data['capital'])


        returnsk.append(last(returnsk)+self.data['returns'])
        return self.data
        #return self.data['cashflow']
    def return_expense(self):
        return self.data['expense']
    def return_cashflow(self):
        return self.data['cashflow']
    def return_profit(self):
        return self.data['returns'],self.data['netprofit']
    def return_capital(self):
        """changing netprofit to list,creating capital as a list with initial capital"""
        netprofit=self.data['netprofit'].values.tolist()

        lc=[]
        for i in range(len(netprofit)):
            v=last(self.last_capital)+netprofit[i]
            lc.append(v)
            #self.last_capital.append(last(lc)+last(self.last_capital))
            self.last_capital.append(last(lc))
        return lc
    def loop(self):
        self._calc_expense()
        self._calc_profit()
        self.return_expense()
        self.return_cashflow()
        self.return_profit()
        self.data['price_bought']=self.price_bought
        self.data['price_sold']=self.price_sold
        return self.data
 

class MLfundamen(object):
    "import  pretrained ml model to filter all stocks to just 20"
    pass
class Message(object):
    """
    A class to post/send messages to my mail
    Of the result of every transactions.
    """
    def __init__(self,selfmail,selfpass,othermail="karuncioreoluwa@gmail.com"):
        """
        Initialize the mail and your mail

        Parameters
        ----------
        selfmail : TYPE
            DESCRIPTION.
        selfpass : TYPE
            DESCRIPTION.
        othermail : TYPE, optional
            DESCRIPTION. The default is "karuncioreoluwa@gmail.com".

        Returns
        -------
        None.

        """
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        self.sender=selfmail
        self.passw=selfpass
        self.receipent=othermail
        self.prev=""
        message=MIMEMultipart()
        message["From"]="Trading Bot"
        message["To"]=self.receipent
        message["Subject"]="The weeks trade's"  
        
        
    def create_message(self,prev):
        """
        Returns A new message
        -------
        None.
        
        """
        self.prev=prev
        
        pass
    def add_message(self,prev):
        """
        Parameters
        ----------
        prev : TYPE
            DESCRIPTION.

        Returns adds to preiouly created message
        -------
        None.

        """
        self.prev=self.prev+prev
        pass
    def delete_message(self,item):
        """
        Removes item from previous message
        """
        self.prev=self.prev.strip(item)
        pass
    def send_message(self,attachment):
        """
        Sends the item
        Attaches attachment
        """
        ttachment=open(attachment,"rb")
        message.attach(MIMEText(self.prev,"plain"))       
        payload=MIMEBase("application","octate-stream")
        payload.set_payload((ttachment).read())
        encoders.encode_base64(payload)
        payload.add_header("Content-Decomposition","attachment",filename=attachment)
        message.attach(payload)
        session=smtplib.SMTP("smtp.gmail.com",587)
        session.starttls()# Enable security
        session.login(self.sender,self.passw)
        text=message.as_string()
        session.sendmail(self.sender,self.receipent,text)
        session.quit()
        return "Done"
        pass
    def return_message(self):
        return self.prev
class APImode(object):
    def __init__(self,broker,vendor=pdr):
        """
        Initializing variables,

        """
        self.broke=broker
        self.ven=vendor
        self.transaction="Fail"
        self.broker_online=""
        pass
    def datarequest(self,ticker,dates):
        
        """Request data from a source"""
        self.transaction="Fail"
        startdate=dates[0]
        enddate=dates[1]
        try:
            if self.ven=="pdr":
                data=get(ticker,startdate,enddate)
            if type(data) ==list:
                self.transaction="Pass"
        except:
            self.transaction="Fail"
            data=0
            

            
        return data,self.transaction
    def dataprocessor(self,data):
        """Process data and confirms"""
        pass
    def  requestsender(self,signal,amount):
        """Send a request to the chosen broker and confirms"""
        pass
    def create_tickers(self,broker,rulest):
        pass
    def main(self):
        """Main code """
        pass
    
    "1st role is get general data for ml mode"
    "2nd role to get specific data to selector"
    "3rd role to return request from portfolio"
    pass

class BacktestAPi(APImode):
    def __init__(self,apiname,apikeys,broker,vendor="pdr"):
        """
        Initializing variables,

        """
        self.broke=broker
        self.ven=vendor
        self.transaction="Fail"
        api=[apiname,apikeys]
        self.broker_online="Online"
        pass
    def datarequest(self,ticker,dates):
        
        """Request data from a source"""
        self.transaction="Fail"
        startdate=dates[0]
        enddate=dates[1]
        try:
            if self.ven=="pdr":
                data=get(ticker,startdate,enddate)
            if type(data)==list:
                self.transaction="Pass"
        except:
            self.transaction="Fail"
            data=0
            

            
        return data,self.transaction
    def  requestsender(self,signal,amount):
        """Send a request to the chosen broker and confirms"""
        pass
    def create_tickers(self,broker,rulest="hello"):
        headers = {
            'authority': 'api.nasdaq.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'origin': 'https://www.nasdaq.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.nasdaq.com/',
            'accept-language': 'en-US,en;q=0.9',
        }
        
        params = (
            ('tableonly', 'true'),
            ('limit', '25'),
            ('offset', '0'),
            ('download', 'true'),
        )
        
        r = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers, params=params)
        data = r.json()['data']
        tickers = pd.DataFrame(data['rows'], columns=data['headers'])
        return tickers
        pass
    
class BacktestAPi_yf(APImode):
    def __init__(self,apiname,apikeys,broker,vendor="pdr"):
        """
        Initializing variables,

        """
        self.broke=broker
        self.ven=vendor
        self.transaction="Fail"
        api=[apiname,apikeys]
        self.broker_online="Online"
        pass
    def get(self,tickers,startdate,enddate):
        def data(ticker):
            hemp=(yf.Ticker(ticker))
            return hemp.history(start=startdate,end=enddate)
        
        datas=map(data,tickers)
        
        return(pd.concat(datas,keys=tickers,names=['Ticker','Date']))
    def datarequest(self,ticker,dates):
        
        """Request data from a source"""
        self.transaction="Fail"
        startdate=dates[0]
        enddate=dates[1]
        try:
            print("Getting data")
            if self.ven=="pdr":
                data=self.get(ticker,startdate,enddate)
            if type(data) ==list:
                print("Successfully got data")
                self.transaction="Pass"
        except:
            print("Failed")
            self.transaction="Fail"
            data=0
        return data
            

            
        return data,self.transaction
    def  requestsender(self,signal,amount):
        """Send a request to the chosen broker and confirms"""
        pass
    def create_tickers(self,broker,rulest="hello"):
        headers = {
            'authority': 'api.nasdaq.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'origin': 'https://www.nasdaq.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.nasdaq.com/',
            'accept-language': 'en-US,en;q=0.9',
        }
        
        params = (
            ('tableonly', 'true'),
            ('limit', '25'),
            ('offset', '0'),
            ('download', 'true'),
        )
        
        r = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers, params=params)
        data = r.json()['data']
        tickers = pd.DataFrame(data['rows'], columns=data['headers'])
        return tickers
        pass
    
    
class BacktestAPI_yf2(BacktestAPi_yf):
    def get(self,tickers,startdate,enddate):
        def data(ticker):
            hemp=(yf.Ticker(ticker))
            return hemp.history(start=startdate,end=enddate)
        
        #datas=map(data,tickers)
        datas=[]
        for items in tickers:
            f=data(items)
            datas.append(f)
            
        
        return datas 
    def datarequest(self,ticker,dates):
        
        """Request data from a source"""
        self.transaction="Fail"
        startdate=dates[0]
        enddate=dates[1]
        try:
            print("Getting data")
            if self.ven=="pdr":
                data=self.get(ticker,startdate,enddate)
            if type(data)==list:
                print("Successfully got data")
                self.transaction="Pass"
        except:
            print("Failed")
            self.transaction="Fail"
            data=0
        return data
    
class Crypi(APImode):
    def get(ticker,startdate,enddate):
        """Get current data through an api"""
        pass
    def requestsender():
        """Send Orders through here"""
        pass
    def create_tickers():
        """Download crypto tickers"""
        pass
    def dataprocessor():
        """This could include the schematics of the selecting method"""
        pass
    
    
class Indicator(object):
    "Functions to serve as indicator"
    def __init__(self,windows):
        self.window=windows
    def _input(self,_input_):
        "Takes an input a gives a calculation "
        pass
    def output_(self,_input_):
        "Returns input as an output"
        return self._input(_input_)
    pass
class Rule(Indicator):
    """Runs multiple indicator"""
    def __init__(self,windows,inicate):
        self.window=window
        self.indicator=indicate
    def _input(self,_input_):
        "Return a 1-0 signal"
        pass
    def output_(self,_input_):
        "Returns _input"
        return self._input(_input_)

class SimpleMovingAverage(Indicator):
    "Function to perform SMA"
    def __init__(self,windows):
        self.windows=windows
        #super(SimpleMovingAverage).__init__(windows)
        
    def _input(self,_input_,min_periods=0,center=True):
        "Performs the SMA "
        return _input_.rolling(window=self.windows,min_periods=1,center=True).mean()
    pass
class MovingAverageRule(SimpleMovingAverage):
    def __init__(self,windows):
        self.windows=windows
        #super(MovingAverageRule).__init__(windows)
    def _input(self,_input_):
        "Perform MAR "
        #n=last(_input_)
        self.simple=SimpleMovingAverage(self.windows).output_(_input_)
        if self.simple['Adj Close'].loc[self.simple.index[-1]]<self.simple['Adj Close'].loc[self.simple.index[-2]]:
            print('uptrend')
        elif self.simple['Adj Close'].loc[self.simple.index[-1]]>self.simple['Adj Close'].loc[self.simple.index[-2]]:
            print('downtrend')
    pass

class ExponentialMovingAverage(Indicator):
    "Function to perform EMA"
    def __init__(self,windows):
        self.windows=windows
        #super(ExponentialMovingAverage).__init__(windows)
    def _input(self,_input_):
        "Calculates the exponentialaverage"
        try:
            self.simple=SimpleMovingAverage(self.windows).output_(_input_["Adj Close"])
            self.simple=_input_['Adj Close']-self.simple['Adj Close']
            self.simple=np.exp(self.simple)
            self.simple=(2/self.windows)*self.simple
            return self.simple
        except:
            try:
                self.exp=_input_["Adj Close"].ewm(span=self.windows)
            except:
                self.exp=_input_["Close"].ewm(span=self.windows)
            return self.exp.mean()
    pass
class AdatptedMovingAverage(Indicator):
    "Function to perform AMA"
    def __init__(self,windows):
        self.windows=windows
        #super(WeighedMovingAverage).__init__(windows)
    def _input(self,_input_,pow1=2,pow2=30):
        "Calculates the weighed average"
        ''' kama indicator '''    
        ''' accepts pandas dataframe of prices '''
 
        absDiffx = abs(_input_['Close'] - _input_['Close'].shift(1) )
        ER_num=abs(_input_['Close']-_input_['Close'].shift(self.windows))
        ER_den=absDiffx.rolling(self.windows).sum()
        ER=ER_num/ER_den
        self.close=_input_['Close']
        sc=(ER*(2.0/(pow1+1)-2.0/(pow2+1.0))+2.0/(pow2+1.0))**2.0
        _input_['KAMA']=np.zeros(sc.size)
        N=len(_input_['KAMA'])
        first_value=True
        for i in range(N):
            if sc[i]!=sc[i]:
                _input_['KAMA'][i]=np.nan
            else:
                if first_value:
                    _input_['KAMA'][i]=_input_['Close'][i]
                    first_value=False
                else:
                    _input_['KAMA'][i]=_input_['KAMA'][i-1]+sc[i]*(_input_['Close'][i]-_input_['KAMA'][i-1])
        self.answer=_input_['KAMA']
        return self.answer
    def plot_g(self):
        ig,ax=plt.subplots()
        self.answer.plot(ax=ax)
        self.close.plot(ax=ax,secondary_y=True,alpha=0.3)
        plt.show()
    pass
"""
MACD 2 is the real macd
"""
class MACD(SimpleMovingAverage):
    """An indicators that calcualte MACD"""
    def __init__(self,Type:Indicator=SimpleMovingAverage,windows:list=[12,26,9]):
        """Initializing the windows four MACD"""
        self.window1=windows[0]
        self.window2=windows[1]
        self.window3=windows[2]
        self.Type=Type
    def _input(self,_input_):
        tma1=self.Type(self.window1).output_(_input_)
        tma2=self.Type(self.window2).output_(_input_)  
        _input_["crossover"]=0
        _input_["converge"]=0
        _input_["diverge"]=0
        diff=tma1-tma2
        #tma3=self.Type(self.window3).output_(diff)
        """_input_["diverge"]=np.where(np.greater(diff,tma3),1,0)
        _input_["signal"]=np.where(np.equal(_input_["diverge"],0),1,0)
        _input_["positions"]=_input_["signal"].diff()"""
        
        _input_["crossover"]=np.where(np.equal(diff,0),1,0)
        _input_["converge"]=np.where(np.greater(diff,0),1,0)
        _input_["diverge"]=np.where(np.less(diff,0),1,0)
        self.data=pd.DataFrame(index=_input_.index)
        _input_["signal"]=np.where(np.equal(_input_["diverge"],1),1,0)
        self.data["signal"]=_input_["signal"]
        _input_["positions"]=_input_["signal"].diff()
        self.data["position"]=_input_["positions"]
        _input_["dif"]=0
        _input_["dif"]=diff
        
        return _input_
    
        

class MACD2(ExponentialMovingAverage):
    def __init__(self,Type:Indicator=ExponentialMovingAverage,windows:list=[12,26,9]):
        """Initializing the windows four MACD"""
        self.window1=windows[0]
        self.window2=windows[1]
        self.window3=windows[2]
        self.Type=Type
        
    def _input(self,_input_):
        tma1=self.Type(self.window1).output_(_input_)
        tma2=self.Type(self.window2).output_(_input_)
        macd=[]
        counter=0
        while counter<len(tma1):
            macd.append(tma1-tma2)
            counter+=1
        self.signal=pd.DataFrame(index=_input_.index)
        #self.signal["tma"]=macd
        self.signal["tma"]=tma1-tma2
        pos=self.signal["tma"].ewm(span=self.window3).mean()
        _input_["signal"]=np.where(np.greater(pos,self.signal["tma"]),1,0)
        _input_["positions"]=_input_["signal"].diff()
        signal=_input_["signal"].values.tolist()
        return _input_
        
class MACD3(ExponentialMovingAverage):
    def __init__(self,Type:Indicator=ExponentialMovingAverage,windows:list=[12,26,9]):
        """Initializing the windows four MACD"""
        self.window1=windows[0]
        self.window2=windows[1]
        self.window3=windows[2]
        self.Type=Type
        
    def _input(self,_input_):
        tma1=self.Type(self.window1).output_(_input_)
        tma2=self.Type(self.window2).output_(_input_)
        macd=[]
        counter=0
        while counter<len(tma1):
            macd.append(tma1-tma2)
            #macd.append(tma1.iloc[counter,0]-tma2.iloc[counter,0])
            counter+=1
        self.signal=pd.DataFrame(index=_input_.index)
        #self.signal["tma"]=macd
        self.signal["tma"]=tma1-tma2
        pos=self.signal["tma"].ewm(span=self.window3).mean()
        self.signal["signal"]=np.where(np.greater(pos,0),0,1)
        self.signal["positions"]=self.signal["signal"].diff()
        signal=self.signal["signal"].values.tolist()
        return self.signal

class TripleMovingAverage(Indicator):
    """
    Code to simplify trading rule making triple  moving average an indicator
    """
    def __init__(self,windows:list=[9,19,34],Type=SimpleMovingAverage):
        self.window1=windows[0]
        self.window2=windows[1]
        self.window3=windows[2]
        self.Type=Type
    def _input(self,_input_):
        avg1=self.Type(self.window1).output_(_input_)
        avg2=self.Type(self.window2).output_(_input_)
        avg3=self.Type(self.window3).output_(_input_)
        signal=pd.DataFrame(index=avg3.index)
        signal["avg1"]=0
        signal["avg2"]=0
        signal["avg3"]=0
        signal["avg1"]=avg1
        signal["avg2"]=avg2
        signal["avg3"]=avg3
        signal["signal"]=0
        signal['signal']=np.where(np.equal(np.greater(avg1,avg2),np.greater(avg1,avg3)),1,0)
        #signal["signal"][self.window1:]=np.where(np.equal(np.greater(avg1[self.window1:],avg2[self.window1:]),np.greater(avg1[self.window1:],avg3[self.window1:])),1.0,0.0)
        signal["positions"]=signal["signal"].diff()
        return signal
class LinearRegression(Indicator):
    "Function to serve as Linear regression"
    def __init__(self,windows=[10,20,2]):
        self.window=windows
    def _input(self,_input_):
        "Performs a regression "
        close=_input_["Close"]
        atr=AverageTradingRange(self.window[0]).output_(_input_)
        middle=ExponentialMovingAverage(self.window[1]).output_(_input_)
        multipl=self.window[2]
        upperband=middle+multipl*(atr)
        lowerband=middle-multipl*(atr)
        #3signal=np.where()
        pass
    def band_width(self,_input_):
        "Perform operation to give band"
        
        pass
    pass
class Memory(Indicator):
    pass
        
class Momentum(Indicator):
    "Calculate momentum with substraction and normal method"
    def __init__(self,windows,Type:str='normal'):
        self.windows=windows
        self.Type=Type
        #super(Momentum).__init__(windows)
    def _input(self,_input_):
        "Calculates the momentum depending on the type"
        if self.Type=='subtract':
            "Uses the subtract method"
            _input_['moment']=_input_['Close']
            pass
        else:
            "Uses the normal method"
            returns=np.log(_input_["Close"])
            x=np.arange(len(returns))
            slope,_,rvalue,_,_=linregress(x,returns)
            annualized=(1+slope)**252
            self.trend=annualized*(rvalue**2)
            return self.trend
        return _input_["moment"]
    
    def next(self,_input_):
        returns=np.log(self.data.get(size=self.windows))
        x=np.arrang(len(returns))
        slope,_,rvalue,_,_=linregress(x,returns)
        return ((1+slope)**252)*(rvalue**2)
class MomentumRule(Rule):
    pass


class PercentageRateOfChange(Momentum):
    "Calculates the momentum in percentages"
    def __init__(self,windows):
        self.windows=windows
        #super(PercentageRateOfChange).__init__(windows)
    def _input(self,_input_):
        "Calculates the rate of change in persentages"
        _input_["RC"]=_input_["Close"].transform(lambda x:x.pct_change(periods=self.windows))
        return _input_
    pass
class PriceRateRule(Rule):
    pass

class RelativeStrengthIndex(Momentum):
    "Calculates the relative strength index"
    def __init__(self,windows):
        self.windows=windows
        #super(RelativeStrengthIndex).__init__(windows)
    def _input(self,_input_):
        "Calculates the relative strength index"
        self.close=_input_['Close']
        self.dif=self.close.diff()
        self.dif=self.dif[1:]
        #pos_m for positive momentum neg_m for negative
        self.pos_m,self.neg_m=self.dif.copy(),self.dif.copy()
        self.pos_m[self.pos_m<0]=0
        self.neg_m[self.neg_m>0]=0
        #Positive and negative rolling mean exponential average
        prme=self.pos_m.ewm(span=self.windows).mean()
        nrme=self.neg_m.ewm(span=self.windows).mean()
        #RSE is ratio of mag of up ove and down move
        RSE=prme/nrme
        _input_['rsie']=100.0-(100.0/(1.0+RSE))
        return _input_
    pass

class RelativeRule(Rule):
    def __init__(self,window,indicate="Rsi"):
        self.windows=window
        self.indicate=indicate
    def _input(self,_input_):
        rsi=RelativeStrengthIndex(self.windows).output_(_input_)
        respone=np.where(np.logical_and(np.greater(rsi.rsie,30),np.less(rsi.rsie,70)),1,0)
        return respone
        

        
    pass

class StochasticOscillator(Momentum):
    "Calculate the fast and slow "
    def __init(self,windows,Type:str='slow'):
        self.windows=windows
        self.Type=Type
        #super(StochasticOscillator).__init__(windows)
    
    def _input(self,_input_):
        "Depending on the type determing the k and d"
        if self.Type=='fast':
            "Only fast oscillator"
            _input_['14-high']=_input_['High'].rolling(self.windows).max()
            _input_['14-low']=_input_['Low'].rolling(self.windows).min()
            _input_['%K']=(_input_['Close']-_input_['14-low'])*100/(_input_['14-high']-_input_['14-low'])
            return _input_['%K']
        else:
            "Oscillator refined with slow"
            _input_['14-high']=_input_['High'].rolling(self.windows).max()
            _input_['14-low']=_input_['Low'].rolling(self.windows).min()
            _input_['%K']=(_input_['Close']-_input_['14-low'])*100/(_input_['14-high']-_input_['14-low'])
            _input_['%D']=_input_['%K'].rolling(3).mean()
            return _input_['%K'],_input_['%D']
    pass
class StochasticRule(Rule):
    def  __init__(self,window,indicate):
        self.window=window
    def _input(self,_input_):
        ma=SimpleMovingAverage(self.window[0]).output_(_input_)
        stoa=StochasticOscillator(windows=self.window[1],Type="fast").output_(_input_)
        rein=np.where(np.greater(stoa,ma),1,0)
        return rein
        
    pass
class Volume(Indicator):
    """Class to parse indicator using volume"""
    def __init__(self,windows):
        self.windows=windows

    def _input(_input_):
        return _input_["Volume"]
    


        
class OnbalanceVolume(Volume):
    def _input(self,_input_):
        _input_['OB_volume']=(np.sign(_input_['Close'].diff())*_input_['Volume']).fillna(0).cumsum()
        return _input_['OB_volume']
class OBVRule(Rule):
    pass

class AverageTradingRange(Indicator):
    def _input(self,_input_):
       high_low= _input_['High']-_input_['Low']
       high_close=np.abs(_input_['High']-_input_['Close'].shift())
       low_close=np.abs(_input_['Low']-_input_['Close'].shift())
       ranges=pd.concat([high_low,high_close,low_close],axis=1)
       true_range=np.max(ranges,axis=1)
       _input_['Average True Range']=true_range.rolling(self.window).sum()/self.window
       self.true_range=_input_['Average True Range']
       self.close=_input_['Close']
       return self.true_range
       pass
       
   
   
    def plot(self):
        fig,ax=plt.subplots()
        self.true_range.plot(ax=ax)
        self.close.plot(ax=ax,secondary_y=True,alpha=0.3)
        plt.show()
       
class ATRRule(Rule):
    pass
        

class Volatility(Indicator):
    "Calculate/determines the volatility of a stock"
    "I.E volatility in terms of variances"
    def __init__(self,windows,Type:str='ATR'):
        self.windows=windows
        self.Type=Type
        #super(Volatility).__init__(windows)
        
    def _input(self,_input_):
        "Calculates the volatility using the various types"
        if self.Type=='Max':
            "Method for finding maximum move"
            pass
        elif self.Type=='MaxTrend':
            "Method for maximum move with trand"
            pass
        elif self.Type=="SD":
            "Method for finding volatility through standard deviation"
            pass
        elif self.Type=="Bands":
            "Applies Bollingers band to get volatility"
            no_of_std=2
            rolling_mean=SimpleMovingAverage(self.windows).output_(_input_['Close'])
            rolling_std=_input_['Close'].rolling(self.windows).std()
            rolling_vol=SimpleMovingAverage(self.windows).output_(_input_['Volume'])
            _input_['rolling_mean']=rolling_mean
            _input_['Bollinger High']=np.greater_equal((rolling_mean+(rolling_std*no_of_std)),self.windows)
            _input_['Bollinger Low']=rolling_mean-(rolling_std*no_of_std)
            _input_['Rolling Vol']=rolling_vol
            pass
        else:
            "Uses ATR method to find volatility"
            pass
        return _input_
    def plot_confidence_interval(_input_,start_date,end_date):
        plt.figure()
        plt.rcParams['figure.figsize']=[20,10]
        #_input_=_input_[(_input_.index>start_date)&(_input_.index<end_date)]
        date=_input_.index
        _input_['Date']=date
        ohlc=_input_[['Date','Open','High','Low','Close']]
        ohlc['Date']=ohlc['Date'].apply(mpl_date.date2num)
        ohlc=ohlc.astype(float)
        fig,ax=plt.subplots()
        b_mean=_input_['rolling_mean']
        b_high=_input_['Bollinger High']
        b_low=_input_['Bollinger Low']
        plt.plot(date,b_mean,'k-')
        plt.fill_between(date,b_low,b_high,color='#eeeee4')
        candlestick_ohlc(ax,ohlc.values,width=0.6,colorup='green',colordown='red',alpha=0.8)
        plt.title("bollinger Band")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()
    pass
class RuleVolatility(Rule):
    pass
class MultipleRangeAverage(Indicator):
    def __init__(self,window:list=[9,8,7,5],no_of_cat:int=4,cat_type:str="sma"):
        self.window=window
        self.no=no_of_cat
        self.Type=cat_type
    def _input(self,_input_):
        assert len(self.window)==self.no
        cator=[]
        mva=pd.DataFrame(index=_input_.index)
        lo=0
        for i in range(self.no):
            if lo==self.no:
                continue
            if type(self.Type)==list:
                if self.Type[i]=="sma":
                    cator.append(SimpleMovingAverage)
                elif self.Type[i]=="adapt":
                    cator.append(AdaptedMovingAverage)
                elif self.Type[i]=="ema":
                    cator.append(ExponentialMovingAverage)
            if type(self.Type)==str:
                if self.Type=="sma":
                    cator.append(SimpleMovingAverage)
                elif self.Type=="adapt":
                    cator.append(AdaptedMovingAverage)
                elif self.Type=="ema":
                    cator.append(ExponentialMovingAverage)
            lo+=1
            if type(self.Type)==list:
                mva[cator[i]]=cator[i](window=self.window[i]).output_(_input_["Close"])
            elif type(self.Type)==str:
                ok=cator[i](self.window[i]).output_(_input_["Close"])
                mva["sma"+str(i)]=ok
        datr=check_greater(mva)
        datr=np.where(np.greater(datr,0),1,0)

        return datr
        
        pass
    pass
class PriceAction(Rule):
    pass
#Alternative PointFigureChart
class PointFigureChart(Indicator):
    "Goal is to see the security with less noise"
    def __init__(self,windows):
        super(PointFigureChart).__init__(windows)
    def _input(self,_input_):
        "It only record a price move when it a significant move"
        pass
    pass

class Selector(object):
    "Trading rules "
    """Target risk allows you to set stop_loss
        target_profit is target profit,
        stockname is the name of the stock,
        entry are rules for entry and vice_versa for exit,
        windows are the windows for the indicators,
        held is if the selector is holding any shares bool val and works in conjuction with stockname,
        
        Functions:
            _risk to calculate risk,
            _guess_profit sets target profit,
            gestock sets stockname
            trading_rule contains all the rule to get signal,
            riskfa, returns risk,
            profitfa, return proft,
            name, returns name
            stop should return the stop loss,
            spread_entry works in case for multiple entry,
            main runs the selector
            
            """
    def __init__(self,risk=0.05,profit=3.0,entry:list=["macd","macd2","TRMA"],exits=["rsie"],window:list=[12],exit_window=[9]):
        self.target_risk=risk
        self.target_profit=profit
        self.stockname=""
        #self._input_=_input_['Close']
        self.entry=entry
        self.exit=exits
        self.windows=window
        self.held=False
        self.exit_windows=exit_window
        """Target risk allows you to set stop_loss
        target_profit is target profit,
        stockname is the name of the stock,
        entry are rules for entry and vice_versa for exit,
        windows are the windows for the indicators,
        held is if the selector is holding any shares bool val and works in conjuction with stockname,
        
        Functions:
            _risk to calculate risk,
            _guess_profit sets target profit,
            gestock sets stockname
            trading_rule contains all the rule to get signal,
            riskfa, returns risk,
            profitfa, return proft,
            name, returns name
            stop should return the stop loss,
            spread_entry works in case for multiple entry,
            main runs the selector
            
            """
        
        pass
    
    
    def _risk(self,stock:pd.Timestamp):
        "A funtion to calculate risk"
        #U could subtract answer from stock
        self.risk=self.target_risk*stock.Close
        pass
    def _guess_profit(self,stock:pd.Timestamp):
        "A function to calculate possible profit"
        self.target=self.target_profit*stock.Close
        pass
    def _gestock(self,value):

        self.stockname=value
    def trading_rule(self,_input_):
        "Contains all the trading rules"
        no_indicator_entry=len(self.entry)
        signals=0
        m=0
        self.entries=[]
        for item in self.entry:
            if item=="macd":
               self.entries.append(MACD)
            elif item=="macd2":
                self.entries.append(MACD2)
            elif item=="macd3":
                self.entries.append(MACD)
            elif item=="TRMA":
                self.entries.append(TripleMovingAverage)
            elif item=="Moment":
                self.entries.append(Momentum)
            elif item=="PRC":
                self.entries.append(PercentageRateOfChange)
            elif item=="rsie":
                self.entries.append(RelativeStrengthIndex)
            elif item=="stoos":
                self.entries.append(StochasticOscillator)
            elif item=="obv":
                self.entries.append(OnbalanceVolume)
            elif item=="ATR":
                self.entries.append(AverageTradingRange)
            elif item=="volt":
                self.entries.append(Volatility)
            """
            Indicators which have not been implemented
            """
            """elif item=="PFC":
                self.entries.append(PointFigureChart)
            elif item=="Price act":
                self.entries.append(PriceAction)
            elif item=="Memory":
                self.entries.append(Memory)
            elif item=="MAR":
                self.entries.append(MultipleAverage)
            elif item=="PRC_rule":
                self.entries.append(PercentageRateRule)
            elif item=="rsie_Rule":
                self.entries.append(RelativeStrengthRule)
            elif item=="stoos_Rule":
                self.entries.append(StochasticRule)
            elif item=="obv_Rule":
                self.entries.append(OnBalenceRule)
            elif item=="ATRule":
                self.entries.append(ATRRule)
            elif item=="voltRule":
                self.entries.append(RuleVolatility)"""
        cator=pd.DataFrame(index=_input_.index)
        for indicators in self.entries: 
            """Takes all the indicator and gives signals"""
            if self.windows!=None:
                if type(self.windows[0])==list: 
                    frame=self.windows[m]
                    oi=indicators(windows=frame).output_(_input_=_input_)
                    cator["signal"+self.entry[m]]=oi.signal
                    #cator["position"+self.entry[m]]=oi.positions
                    m+=1
                if type(self.windows[0])==int:
                    oi=indicators(windows=self.windows).output_(_input_=_input_)
                    cator["signal"+self.entry[m]]=oi.signal
                    #cator["position"+self.entry[m]]=oi.positions
                    m+=1
            else:
                oi=indicators().output_(_input_=_input_)
                cator["signal"+self.entry[m]]=oi.signal
                #cator["position"+self.entry[m]]=oi.positions
                m+=1
            
        self.exits=[]
        for item in self.exit:
            if item=="macd":
               self.exits.append(MACD)
            elif item=="macd2":
                self.exits.append(MACD2)
            elif item=="macd3":
                self.exits.append(MACD)
            elif item=="TRMA":
                self.exits.append(TripleMovingAverage)
            elif item=="Moment":
                self.exits.append(Momentum)
            elif item=="PRC":
                self.exits.append(PercentageRateOfChange)
            elif item=="rsie":
                self.exits.append(RelativeStrengthIndex)
            elif item=="stoos":
                self.exits.append(StochasticOscillator)
            elif item=="obv":
                self.exits.append(OnbalanceVolume)
            elif item=="ATR":
                self.exits.append(AverageTradingRange)
            elif item=="volt":
                self.exits.append(Volatility)
            """
            Indicators which have not been implemented
            """
            """elif item=="PFC":
                self.exits.append(PointFigureChart)
            elif item=="Price act":
                self.exits.append(PriceAction)
            elif item=="Memory":
                self.exits.append(Memory)
            elif item=="MAR":
                self.exits.append(MultipleAverage)
            elif item=="PRC_rule":
                self.exits.append(PercentageRateRule)
            elif item=="rsie_Rule":
                self.exits.append(RelativeStrengthRule)
            elif item=="stoos_Rule":
                self.exits.append(StochasticRule)
            elif item=="obv_Rule":
                self.exits.append(OnBalenceRule)
            elif item=="ATRule":
                self.exits.append(ATRRule)
            elif item=="voltRule":
                self.exits.append(RuleVolatility)"""
        po=0
        catori=pd.DataFrame(index=_input_.index)
        for indicator in self.exits:
            if self.exit_windows!=None:
                second=indicator(self.exit_windows[po]).output_(_input_)
            else:
                second=indicator().output_(_input_)
            try:
                catori["end_sig"+self.exit[po]]=second["signal"]
            except:
                catori["end_sig"+self.exit[po]]=second[last(second.columns.values.tolist())]
            po+=1
        
        cator["main"]=check_equal(cator)
        cator["position_entry"]=cator["main"].diff()
        cator["end_sig"]=check_equal(catori)
        cator["end_sig_pos"]=cator["end_sig"].diff()
        cator["signal"]=np.where(np.equal(cator["end_sig_pos"],-1),0,cator["main"])
        cator["positions"]=cator["signal"].diff()
        hut=pd.DataFrame()
        hut["signal"]=cator["signal"].tail(1)
        hut["positions"]=cator["positions"].tail(1)
        return cator,hut
        #pass
    def riskfa(self,stock):
        "return risk through risk function"
        self._risk(stock)
        return stock.Close.tail(1)-self.risk.tail(1)
    def profitfa(self,stock):
        "return the expected profit"
        self._guess_profit(stock)
        return self.target.tail(1)
    def name(self,mina):
        """
        Function to return stock name
        """
        self._gestock(mina)
    def stop(self,methods:str="main",percent:float=0.85):
        """Checks if the price of the stock hits or less than certain value"""
        #Methods are the way which it places stops
        if methods=="main":
            return self.risk.tail(1)*percent
        pass
    def spread_entry(self,indicate:AverageTradingRange,_input_):
        """
        Compares a second index to confirm previous signal
        """
        pass1=indicate(windows=self.windows[0])
        pass1.output_(_input_)
        pass2=pass1.plot()
        return pass1
    def main(self,lil1,lil2):
        #lil1 is the name list
        #lil2 is the data list
        assert len(lil1)==len(lil2)
    
        chose=[]
        total=[]
        no=0
        for i in range(len(lil2)):
            leap,like=self.trading_rule(lil2[i])
            total.append(leap)
            chose.append(like)
        names=[]
        comm=[]
        for item in chose:
            if self.held==False:
                if item.signal.all()==1 and item.positions.all()==1:
                    self.stockname=lil1[no]
                    signal="Buy"
                else:
                    self.stockname=""
                    signal="Neutal"
                
            elif self.held==True:
                if item.signal.all()==0 and item.positions.all()==-1:
                    self.stockname=lil1[no]
                    signal=="Sell"
                else:
                    self.stockname=""
                    signal="Neutal"
            comm.append(signal)
            names.append(self.stockname)
            no+=1
        
        return comm,names
                
            
        
        pass
        
       
    pass

class TrendTrade(Selector):
    "More of rules for trend following trading"
    def __init__(self,risk=0.5,profit=4,entry=["macd","macd2"],exits=["TRMA"],window:list=[[12,20,30]]):
        self.stockname=""
        self.target_risk=risk
        self.target_profit=profit
        self.stockname=""
        self.entry=entry
        self.exit=exits
        self.windows=window
    def trading_rule(self,_input_):
        "Contains all the trading rules"
        no_indicator_entry=len(self.entry)
        signals=0
        m=0
        self.entries=[]
        for item in self.entry:
            if item=="macd":
               self.entries.append(MACD)
            elif item=="macd2":
                self.entries.append(MACD2)
            elif item=="macd3":
                self.entries.append(MACD)
            elif item=="TRMA":
                self.entries.append(TripleMovingAverage)
        cator=pd.DataFrame(index=_input_.index)
        for indicators in self.entries: 
            """Takes all the indicator and gives signals"""

            oi=indicators().output_(_input_=_input_)
            cator["signal"+self.entry[m]]=oi.signal
            #cator["position"+self.entry[m]]=oi.positions
            m+=1
            
        self.exits=[]
        for item in self.exit:
            if item=="macd":
               self.exits.append(MACD)
            elif item=="macd2":
                self.exits.append(MACD2)
            elif item=="macd3":
                self.exits.append(MACD)
            elif item=="TRMA":
                self.exits.append(TripleMovingAverage)
            elif item=="rsie":
                self.exits.append(RelativeStrengthIndex)
                                  
        po=0
        catori=pd.DataFrame(index=_input_.index)
        for indicator in self.exits:      
            second=indicator(self.windows[po]).output_(_input_)
            try:
                catori["end_sig"+self.exit[po]]=second["signal"]
            except:
                catori["end_sig"+self.exit[po]]=second[last(second.columns.values.tolist())]
            po+=1
        
        cator["main"]=check_equal(cator)
        cator["position_entry"]=cator["main"].diff()
        cator["end_sig"]=check_equal(catori)
        cator["end_sig_pos"]=cator["end_sig"].diff()
        cator["signal"]=np.where(np.equal(cator["end_sig_pos"],-1),0,cator["main"])
        cator["positions"]=cator["signal"].diff()   
        return cator
        #pass

        
                
        
        
        pass
    pass
class SwingTrade(Selector):
    "More of rules for swing trader"
    def trading_rule(self):
        "Write the rules"
        pass
    pass
class FundamentalTrade(Selector):
    "Rules for a cashflow seeker"
    def trading_rule(self):
        "Write the rules"
        pass
    pass
class TechCashflow(Selector):
    "A Technical selector with reinvestment plans into cashflow"
    def trading_rule(self):
        "Write the rules"
        pass
    
                                                          
class Portfolio(object):
    "Majorly risk management,portfolio selecting"
    def __init__(self,mail,mailpass,n=100,commision=15,data=7,windows=None,broker="Phil",no_of_shre=None,rules=Selector,API=APImode,maximum=0.2,capital:float=1000.0,APIKeys:int=1010,APIname="Reo",period:int=7,no_of_transaction:int=5,rulest=[],time=12,start_date=[2019,5,18]):
        """
        Initializing the model for the selection,
        Api,capital,apikeys
        period and and no of transactions,commision,data_cost,
        windows,times,sartdate
        """
        
        self.commision=commision
        self.data=data
        self.windows=windows
        self.initial_capital=capital
        self.Bot=CashflowStatementBot
        self.rules=rules
        self.keys=APIKeys
        self.name_of_api=APIname
        self.api=API
        self.period=period
        self.stockno=no_of_transaction
        self.transactions=pd.DataFrame()
        self.maximumloss=maximum*capital
        self.quit=False
        self.broker=broker
        self.portofolio=[]
        self.amount_shares=no_of_shre
        self.connected=False
        self.rulest=rulest
        self.settime=time
        self.startdate=datetime.datetime(start_date[0],start_date[1],start_date[2])
        self.api=self.api(broker=self.broker,apikeys=APIKeys,apiname=APIname)
        self.ssage=Message
        self.mail=mail
        self.mailpass=mailpass
        self.n=n
        """
        transaction should be the list of transaction done
        """
        
    def _find_ifbought(self,lil1,lil2):
        mo=0
        print(lil2)
        for item in lil2:
            if item=="Buy":
                return "Buy",lil1[mo],mo
            elif item=="Sell":
                return "Sell",lil1[mo],mo
            mo+=1
        pass
    def _no_of_item(self,input_list):
        new_list=list(chunk_based_on_no(input_list,self.stockno))
        return new_list
   
    
    
    def total_risk(self):
        "Returns summation of the risk of the 5 trade"
        pass
    def amount(self):
        "Returns amount for investment in indivual stock"
        
        pass
    def shares_list(self):
        "Returns the amount of shares currently owned"
        pass
    def owned_shares(self):
        "returns total list of shares owned"
        pass
    def transaction(self):
        "returns a total list of transaction performed"
        pass
    def present_profit(self):
        "Uses cashflow to caalculate profit for the week"
        pass
    def total_value(self):
        "Checks the total value of all transaction"
        pass
    def Order(self,comm,capital,data,no,amount_of_shares):
        
        "receives order from selector, confirm order and send to api"

        data=data[no]
        price=data.Close.tail(1)*amount_of_shares
        print(price)
        #pricing=price.values.to_numpy()
        #pricing=float(last(price.tolist()))
        capital=capital
        #capital=capital.values.to_numpy()
        #capital=float(capital)
        if comm=="Buy":
            print("A")
            
            #price=price
            if price.any()<capital:
                self.api.requestsender(signal="Sell",amount=amount_of_shares)
                return price  
        elif comm=="Sell":
            print("B")
            self.api.requestsender(signal="Sell",amount=amount_of_shares[no])
            return price

            
        pass
    def data_acess(self):
        "Access data from a vendor"
        pass
    def confirm(self):
        "Confirms order has been received by broker"
        pass
    def selfquit(self):
        if self.capital<=self.maximumloss:
            self.quit="True"
    def amount_share_finder(self,capital,price):
        if self.amount_shares==None:
            amount_of_shares=capital/price
            return amount_of_shares
        elif self.amount_shares!=None:
            amount_of_shares=self.amount_shares
            return amount_of_shares
        
    def _update(self,data):
        #Takes data and update them 
        return self.api.datarequest(self, ticker, dates)
    def _updback(self,data):
        pass
    
    
    def main(self,input_list):
        """This is the major function in the code to transacts
        """
        the=[]
        select=[]#Contains all selector
        tickers=["thin","win","aapl",""]
        for i in range(self.stockno):
            #To create rules for all selectors
            the.append(self.rules)
        lop=self._no_of_item(input_list)
        tick=self._no_of_item(tickers)
        np=0
        po=0
        signals=[]
        for item in the:
            try:
                #Code to run selectorclass
                iterl=[]
                iterl.append(item())
            
                inter,_=iterl[np].main(tick,lop[po])
                signals.append(inter)
                select.append(iterl[np])
                po+=1
            except AttributeError:
                continue
        #return signals
        ip=0
        bought=[]
        sold=[]
        stopl=[]
        target=[]
        capital=self.capital/self.stockno
        for items in signals:
            try:
                signal,_,mo=self._find_ifbought(lil1=tickers,lil2=items)
            except TypeError:
                signal="Neutral"  
                continue
            if signal=="Buy":
                price=self.Order(comm="Buy",capital=capital,data=lop,no=mo)
                select[ip].held=True
                bought.append(price)
                self.portofolio.append(tick[mo])
                select[ip].riskfa(lop[mo][ip])
                select[ip].profitfa(lop[mo][ip])
                #print(lop[mo][ip])
                #Trying to remove the data from it,
                stopl.append(lop[mo][ip].Close.tail(1)-select[ip].stop())
                target.append(select[ip].target.tail(1)*self.amount_shares)
            elif signal=="Sell":
                price=self.Order(comm="Sell",capital=capital,data=lop,no=mo)
                select[ip].held=False
                sold.append(price)
                self.portfolio.remove(tick[mo])
            elif stopl[ip]<=bought[ip]:
                price=self.Order(comm="Sell",capital=capital,data=lop,no=mo)
                select[ip].held=False
                sold.append(price)
                self.portfolio.remove(tick[mo])
            elif  target[ip]>=bought[ip]:
                price=self.Order(comm="Sell",capital=capital,data=lop,no=mo)
                select[ip].held=False
                sold.append(price)
                self.portfolio.remove(tick[mo])          
        
        if self.connected==True:
            lop=self._update(lop)
        else:
            lop==self._updback(lop)
            
        return bought,sold,stopl,target
        pass
    def _main(self,save_file="hist.txt",directory="C:\\Users\\user\\python\\Firstbot"):
        import os
        os.chdir(directory)
        try:
            file=open(save_file)
            print(file)
            file.close()
            time_file=pd.read_csv("time_file.csv")
            dat_save=pd.read_csv("dat_save.csv")
            price_values=pd.read_csv("price_values.csv")
            print("B")
            print("File found")
            print("Initializing====>>>")
        except:
            timed=Timer(days=[datetime.date.today().year,datetime.date.today().month,datetime.date.today().day],hours=[datetime.datetime.today().hour,datetime.datetime.today().minute,datetime.datetime.today().second])
            day=0
            the=[]
            tickers=self.api.create_tickers(broker=self.broker)
            tickers=tickers.symbol
            print(tickers.tail())
            #tickers=tickers["symbol"]
            #tickers=["thin","win","aapl","",""]
            for i in range(self.stockno):
                #To create rules for all selectors
                the.append(self.rules)
            print("A")
            tick=self._no_of_item(tickers.values.tolist())
            file=open(save_file,"w")
            print(">-----Creating files")
            file.close()
            data_save={"the":the,"tick":tick}
    
            dat_save=pd.DataFrame(data=data_save)
            dat_save.to_csv("dat_save.csv")
            week=1
            timedata={"times":timed.days,"hours":timed.hours,"day":day,"week":week}
            #time_col=[0,1]
            time_file=pd.DataFrame(data=timedata)
            time_file.to_csv("time_file.csv")
            print("Completed Initializtion")
            print("Developing price format!!!!")
            portfolio=[0]
            bought=[0]
            sold=[0]
            amount=[0]
            self.capital=self.initial_capital
            prices_dict={"portfolio":portfolio,"bought":bought,"sold":sold,"amount":amount,'capital':self.capital}
            price_values=pd.DataFrame(data=prices_dict)
            price_values.to_csv("price_values.csv")
        
        print("Finally the code is running")
        time1=time_file.times.values.tolist()
        hours1=time_file.hours.values.tolist()
        day=time_file.day.values.tolist()
        week=time_file.week.values.tolist()
        day=last(day)
        week=last(week)
        timed=Timer(days=[time1[0],time1[1],time1[2]],hours=[hours1[0],hours1[1],hours1[2]])
        present_time=timed.check_time()
        present_date=timed.check_date()
        the=dat_save.the.to_list()
        tick=dat_save.tick.to_list()
        tick=extracts(df=dat_save,largest=len(the),key="tick")
        #tick=[i.strip("[]").split(",") for i in tick]
        print("Checking the time")
        if present_time==self.settime:#  and bool(self.api.broker_online)==True:
            print("Time is after %d",(self.settime))
            day+=1   
            print("C")
            '''The part of the selector to generate signal and buy and sell on it'''
            np=0
            po=0
            print("Generating signals !!!!!>>")
            lop=[]
            today_time=datetime.datetime.today()
            yesterday_time=today_time.day-1
            for items in tick:
                ticking=listsplit(items,50)
                input_list=self.api.datarequest(ticker=ticking,dates=[self.startdate,datetime.datetime(today_time.year,today_time.month,yesterday_time)])
                lop.append(input_list)
            kim=0
            lop2,tick3=[],[]
            for enit in lop:
                kimp=0
                loo,lab=[],[]
                for enita in enit:
                    if len(enita)!=0:
                        loo.append(enita)
                        lab.append(tick[kim][kimp])
                        
                    kimp+=1
                lop2.append(loo)
                tick3.append(lab)
                kim+=1
            #lop=input_list
            print(counter(tick))
            print(counter(lop))
            #lop=self._no_of_item(input_list)
            select=[]#Contains all selector
            signals=[]
            return lop2,tick3
            '''for item in the:
                try:
                    #Code to run selectorclass
                    iterl=[]
                    print("Generating--------")
                    print(counter(lop[po]),counter(tick[po]))
                    print(lop[po][0].shape)
            
                    item=item.strip("<")
                    item=item.strip(">")
                    item=item.strip("class")
                    item=eval(item)
                    item=item.strip("__")
                    item=item.strip("main")
                    item=item.strip("__")
                    item=item.strip(".")
                    item=eval(item)
                    print(type(item))
                    if self.windows==None:
                        bello=item(window=None)
                    else:
                        bello=item(window=self.windows[np])
                    iterl.append(bello)
                
                    inter,_=iterl[np].main(tick[po],lop[po])
                    signals.append(inter)
                    select.append(iterl[np])
                    po+=1
                except AttributeError:
                    continue
            #return signals
            print("Generated signal ...")
            ip=0
            bought=price_values.bought.tolist()
            sold=price_values.sold.tolist()
            self.portfolio=price_values.portfolio.tolist()
            amount_of_shares=price_values.amount.tolist()
            self.capital=price_values.capital.tail(1)
            stopl=[]
            target=[]
            capital=self.capital/self.stockno
            print("Making a decision !!!")
            print(signals)
            for items in signals:
                print("D--d")
                try:
                    print("On====")
                    signal,_,mo=self._find_ifbought(lil1=tickers,lil2=items)
                    print("It has found")
                except TypeError:
                    signal="Neutral" 
                    print(signal)
                    continue
                if signal=="Buy":
                    cost=lop[mo].Close.tail(1)
                    amount_shares=self.amount_share_finder(capital=capital,price=cost)
                    price=self.Order(comm="Buy",capital=capital,data=lop,no=mo,amount_of_shares=amount_shares)
                    select[ip].held=True
                    bought.append(price)
                    amount_of_shares.append(amount_shares)
                    self.portofolio.append(tick[mo])
                    select[ip].riskfa(lop[mo][ip])
                    select[ip].profitfa(lop[mo][ip])
                    #print(lop[mo][ip])
                    #Trying to remove the data from it,
                    stopl.append(lop[mo][ip].Close.tail(1)-select[ip].stop())
                    target.append(select[ip].target.tail(1)*self.amount_shares)
                elif signal=="Sell":
                    price=self.Order(comm="Sell",capital=capital,data=lop,no=mo,amount_of_shares=amount_of_shares)
                    select[ip].held=False
                    sold.append(price)
                    self.portfolio.remove(tick[mo])
                elif stopl[ip]<=bought[ip]:
                    price=self.Order(comm="Sell",capital=capital,data=lop,no=mo,amount_of_shares=amount_of_shares)
                    select[ip].held=False
                    sold.append(price)
                    self.portfolio.remove(tick[mo])
                elif  target[ip]>=bought[ip]:
                    price=self.Order(comm="Sell",capital=capital,data=lop,no=mo,amount_of_shares=amount_of_shares)
                    select[ip].held=False
                    sold.append(price)
                    self.portfolio.remove(tick[mo])
                elif day/week==7.0:
                    price=self.Order(comm="Sell",capital=capital,data=lop,no=mo,amount_of_shares=amount_of_shares)
                    select[ip].held=False
                    sold.append(price)
                    self.portfolio.remove(tick[mo])
                else:
                    print("Neitral or Error")
                print(signal)
            if day/week==7.0: 
                data={"Price_bought":bought,"Price_sold":sold}
                data_frame=pd.DataFrame(data)
                ep=self.Bot(initial_capital=self.capital,comission=self.commision,price_sold=data_frame["Price_sold"],price_bought=data_frame["Price_bought"],data_amount=self.data).loop()
                ep.to_csv("ep,day"+day+".csv")
                message=Message(selfmail=self.mail,selfpass=self.mailpass)
                message.create_message(prev="Total trade for the week are")
                message.send_message("ep,day"+day+".csv")
                week+=1
                self.capital=ep.capital.sum()
            timedata={"times":timed.days,"hours":timed.hours,"day":day,"week":week}
            time_file=pd.DataFrame(data=timedata)
            time_file.to_csv("time_file.csv")
            prices_dict={"portfolio":portfolio,"bought":bought,"sold":sold,"amount":amount_of_shares,"capital":self.capital}
            price_values=pd.DataFrame(data=prices_dict)
            price_values.to_csv("price_values.csv")
            pass'''
        else:
            print("The time is not %d",(self.settime))
            #quit()
            pass
            
            
            
            
        """The structure remains cashbots exceptions and message/mail etc """
        
            
        
        pass
    
    
    def _main1(self,save_file="hist.txt",directory="C:\\Users\\user\\python\\Firstbot"):
        import os
        os.chdir(directory)
        try:
            file=open(save_file)
            print(file)
            file.close()
            time_file=pd.read_csv("time_file.csv")
            dat_save=pd.read_csv("dat_save.csv")
            price_values=pd.read_csv("price_values.csv")
            print("B")
            print("File found")
            print("Initializing====>>>")
        except:
            timed=Timer(days=[datetime.date.today().year,datetime.date.today().month,datetime.date.today().day],hours=[datetime.datetime.today().hour,datetime.datetime.today().minute,datetime.datetime.today().second])
            day=0
            the=[]
            tickers=self.api.create_tickers(broker=self.broker)
            tickers=tickers["symbol"]
            #tickers=["thin","win","aapl","",""]
            for i in range(self.stockno):
                #To create rules for all selectors
                the.append(self.rules)
            print("A")
            tick=self._no_of_item(tickers.values.tolist())
            file=open(save_file,"w")
            print(">-----Creating files")
            file.close()
            data_save={"the":the,"tick":tick}
    
            dat_save=pd.DataFrame(data=data_save)
            dat_save.to_csv("dat_save.csv")
            week=1
            timedata={"times":timed.days,"hours":timed.hours,"day":day,"week":week}
            #time_col=[0,1]
            time_file=pd.DataFrame(data=timedata)
            time_file.to_csv("time_file.csv")
            print("Completed Initializtion")
            print("Developing price format!!!!")
            portfolio=[0,0,0,0,0]
            bought=[0,0,0,0,0]
            sold=[0,0,0,0,0]
            self.capital=self.initial_capital
            amount=[0,0,0,0,0]
            stop1=[0,0,0,0,0]
            target=[0,0,0,0,0]
            prices_dict={"portfolio":portfolio,"bought":bought,"sold":sold,"amount":amount,'capital':self.capital,'stop1':stop1,'target':target}
            price_values=pd.DataFrame(data=prices_dict)
            price_values.to_csv("price_values.csv")
        
        print("Finally the code is running")
        time1=time_file.times.values.tolist()
        hours1=time_file.hours.values.tolist()
        day=time_file.day.values.tolist()
        week=time_file.week.values.tolist()
        day=last(day)
        week=last(week)
        timed=Timer(days=[time1[0],time1[1],time1[2]],hours=[hours1[0],hours1[1],hours1[2]])
        present_time=timed.check_time()
        present_date=timed.check_date()
        tick=dat_save.tick.to_list()
        #tickers=dat_save.tickers.tolist()
        the=dat_save.the.to_list()
        tick=extracts(df=dat_save,largest=len(the),key="tick")
        print("Checking the time")
        if present_time==self.settime:#  and bool(self.api.broker_online)==True:
            print("Time is after %d",(self.settime))
            day+=1   
            print("C")
            '''The part of the selector to generate signal and buy and sell on it'''
            np=0
            po=0
            print("Generating signals !!!!!>>")
            lop=[]
            tick1=[]
            today_time=datetime.datetime.today()
            yesterday_time=today_time.day-1
            for items in tick:
                ticking=listsplit(items,self.n)
                input_list=self.api.datarequest(ticker=ticking,dates=[self.startdate,datetime.datetime(today_time.year,today_time.month,yesterday_time)])
                lop.append(input_list)
                tick1.append(ticking)
            tick=tick1
            kim=0
            lop2,tick3=[],[]
            for enit in lop:
                kimp=0
                loo,lab=[],[]
                for enita in enit:
                    if len(enita)!=0:
                        loo.append(enita)
                        lab.append(tick[kim][kimp])
                        
                    kimp+=1
                lop2.append(loo)
                tick3.append(lab)
                kim+=1
            tick,lop=tick3,lop2
            print(counter(lop))
            print(counter(tick))
            select=[]#Contains all selector
            signals=[]
            for item in the:
                try:
                    #Code to run selectorclass
                    iterl=[]
                    print("Generating--------")
    
            
                    item=item.strip("<")
                    item=item.strip(">")
                    item=item.strip("class")
                    item=eval(item)
                    item=item.strip("__")
                    item=item.strip("main")
                    item=item.strip("__")
                    item=item.strip(".")
                    item=eval(item)
                    print(type(item))
                    if self.windows==None:
                        bello=item(window=None)
                    else:
                        bello=item(window=self.windows[np])
                    iterl.append(bello)
                    print(counter(tick[po]),counter(lop[po]))
                    inter,_=iterl[np].main(tick[po],lop[po])
                    signals.append(inter)
                    select.append(iterl[np])
                    po+=1
                except AttributeError:
                    continue
            #return signals
            print("Generated signal ...")
            ip=0
            print(item,signals,select)
            bought=price_values.bought.tolist()
            bought2=list_to_str_float_list(bought)
            sold=price_values.sold.tolist()
            sold2=list_to_str_float_list(sold)
            self.portfolio=price_values.portfolio.tolist()
            amount_of_shares=price_values.amount.tolist()
            amount_of_shares2=list_to_str_float_list(amount_of_shares)
            self.capital=price_values.capital.tolist()          
            stopl=price_values.stop1.tolist()
            target=price_values.target.tolist()
            capital=last(self.capital)/self.stockno
            print("Making a decision !!!")
            zeus=0
            for athena in self.portfolio:
                if athena !=0:
                    select[zeus].held=True
                zeus+=1

            tickno=0
            fakeport=[]
            for items in signals:
                try:
                    signal,_,mo=self._find_ifbought(lil1=tick[tickno],lil2=items)
                except TypeError:
                    signal="Neutral"  
                    continue
                if signal=="Buy" and select[ip]==False:# and select[i].held==False:
                    cost=lop[tickno][mo].Close.tail(1)
                    amount_shares=self.amount_share_finder(capital=capital,price=cost)
                    price=self.Order(comm="Buy",capital=capital,data=lop[tickno],no=mo,amount_of_shares=amount_shares)
                    select[ip].held=True
                    bought[ip]=cost
                    print("amount is:",amount_shares)
                    print("cost is:",cost)
                    print("bought:",amount_shares)
                    amount_of_shares[ip]=amount_shares
                    #self.portofolio[ip]=tick[tickno]#[mo]
                    fakeport.append(tick[tickno][mo])
                    select[ip].riskfa(lop[tickno][mo])
                    select[ip].profitfa(lop[tickno][mo])
                    #print(lop[mo][ip])
                    #Trying to remove the data from it,
                    stopl[ip]=lop[tickno][mo].Close.tail(1)-select[ip].stop()
                    targetino=select[ip].target*amount_shares#select[ip].target_risk*cost*amount_of_shares)
                    target[ip]=targetino
                    self.portfolio[ip]=fakeport[ip]
                    
                elif signal=="Sell":
                    price=self.Order(comm="Sell",capital=capital,data=lop[tickno],no=mo,amount_of_shares=amount_of_shares2[tickno])
                    select[ip].held=False
                    sold[ip]=price
                    self.portfolio[ip]=0#tick[tickno][mo])
                    stopl[ip]=0#remove(lop[tickno][mo])
                    target[ip]=0#.remove(target[ip])
                    amount_of_shares[ip]=0
                elif stopl[ip]<=bought[ip]:
                    price=self.Order(comm="Sell",capital=capital,data=lop[tickno],no=mo,amount_of_shares=amount_of_shares2[tickno])
                    select[ip].held=False
                    sold[ip]=price#append(price)
                    self.portfolio[ip]=0#.remove(tick[tickno][mo])
                    stopl[ip]=0#.remove(lop[tickno][mo])
                    target[ip]=0#.remove(target[ip])
                    amount_of_shares[ip]=0
                elif  target[ip]>=bought[ip]:
                    price=self.Order(comm="Sell",capital=capital,data=lop[tickno],no=mo,amount_of_shares=amount_of_shares2[tickno])
                    select[ip].held=False
                    sold[ip]=price#.append(price)
                    self.portfolio[ip]=0#.remove(tick[tickno][mo])
                    stopl[ip]=0#.remove(lop[tickno][mo])
                    target[ip]=0#.remove(target[ip])
                    amount_of_shares[ip]=0
                elif day/week==7.0:
                    price=self.Order(comm="Sell",capital=capital,data=lop[tickno],no=mo,amount_of_shares=amount_of_shares2[tickno])
                    select[ip].held=False
                    sold[ip]=price#.append(price)
                    self.portfolio[ip]=0#.remove(tick[tickno][mo])
                    stopl[ip]=0#.remove(lop[tickno][mo])
                    target[ip]=0#.remove(target[ip])
                    amount_of_shares[ip]=0
                else:
                    print("NO move made")
                tickno+=1
                ip+=1
            if day/week==7.0: 
                data={"Price_bought":bought,"Price_sold":sold}
                data_frame=pd.DataFrame(data)
                ep=self.Bot(initial_capital=self.capital,comission=self.commision,price_sold=data_frame["Price_sold"],price_bought=data_frame["Price_bought"],data_amount=self.data).loop()
                ep.to_csv("ep,day"+day+".csv")
                message=Message(selfmail=self.mail,selfpass=self.mailpass)
                message.create_message(prev="Total trade for the week are")
                message.send_message("ep,day"+day+".csv")
                print("Delivered mail")
                week+=1
                self.capital=ep.capital.sum()
            #timedata={"times":timed.days,"hours":timed.hours,"day":day,"week":week}
            timedata={"times":time1,"hours":hours1,"day":day,"week":week}
            time_file=pd.DataFrame(data=timedata)
            time_file.to_csv("time_file.csv")
            print("bought:",bought)
            print("sold:",sold)
            print("capital",self.capital)
            print("bought",len(bought),"portfolio",len(self.portfolio),"sales",len(sold),"amount",len(amount_of_shares),"target",len(target),"capital",len(self.capital))
            prices_dict={"portfolio":self.portfolio,"bought":bought,"sold":sold,"amount":amount_of_shares,"capital":self.capital,"stop1":stopl,'target':target}
            price_values=pd.DataFrame(data=prices_dict)
            price_values.to_csv("price_values.csv")
            print("Completed")
            pass
        else:
            print("The time is not %d",(self.settime))
            #quit()
            pass
            
            
            
            
        """The structure remains cashbots exceptions and message/mail etc""" 
        
            
        
        pass
    
    def _main2(self,save_file="hist.txt",directory="C:\\Users\\user\\python\\Firstbot"):
        import os
        os.chdir(directory)
        try:
            file=open(save_file)
            print(file)
            file.close()
            time_file=pd.read_csv("time_file.csv")
            dat_save=pd.read_csv("dat_save.csv")
            price_values=pd.read_csv("price_values.csv")
            print("B")
            print("File found")
            print("Initializing====>>>")
        except:
            timed=Timer(days=[datetime.date.today().year,datetime.date.today().month,datetime.date.today().day],hours=[datetime.datetime.today().hour,datetime.datetime.today().minute,datetime.datetime.today().second])
            day=0
            the=[]
            tickers=self.api.create_tickers(broker=self.broker)
            tickers=tickers["symbol"]
            #tickers=["thin","win","aapl","",""]
            for i in range(self.stockno):
                #To create rules for all selectors
                the.append(self.rules)
            print("A")
            tick=self._no_of_item(tickers.values.tolist())
            file=open(save_file,"w")
            print(">-----Creating files")
            file.close()
            dataframetor(the,tickers)
            dataframetor(tick,tickers)
            data_save={"the":the,"tick":tick,"tickers":tickers}
    
            dat_save=pd.DataFrame(data=data_save)
            dat_save.to_csv("dat_save.csv")
            week=1
            timedata={"times":timed.days,"hours":timed.hours,"day":day,"week":week}
            #time_col=[0,1]
            time_file=pd.DataFrame(data=timedata)
            time_file.to_csv("time_file.csv")
            print("Completed Initializtion")
            print("Developing price format!!!!")
            portfolio=[]
            bought=[]
            sold=[]
            amount=[]
            self.capital=self.initial_capital
            prices_dict={"portfolio":portfolio,"bought":bought,"sold":sold,"amount":amount,'capital':self.capital}
            price_values=pd.DataFrame(data=prices_dict)
            price_values.to_csv("price_values.csv")
        
        print("Finally the code is running")
        time1=time_file.times.values.tolist()
        hours1=time_file.hours.values.tolist()
        day=time_file.day.values.tolist()
        week=time_file.week.values.tolist()
        day=last(day)
        week=last(week)
        timed=Timer(days=[time1[0],time1[1],time1[2]],hours=[hours1[0],hours1[1],hours1[2]])
        present_time=timed.check_time()
        present_date=timed.check_date()
        the,tickers=pd_editzero(dat_save,x="the",y="tickers")
        tick,_=pd_editzero(dat_save,x="tick",y="tickers")
        #tick=dat_save.tick.to_list()
        #tickers=dat_save.tickers.tolist()
        #the=dat_save.the.to_list()
        print("Checking the time")
        if present_time==self.settime:#  and bool(self.api.broker_online)==True:
            print("Time is after %d",(self.settime))
            day+=1   
            print("C")
            '''The part of the selector to generate signal and buy and sell on it'''
            np=0
            po=0
            print("Generating signals !!!!!>>")
            input_list=self.api.datarequest(ticker=tickers,dates=[self.startdate,datetime.datetime.today()])
            lop=self._no_of_item(input_list)
            print(counter(lop))
            print(counter(tick))
            select=[]#Contains all selector
            signals=[]
            for item in the:
                try:
                    #Code to run selectorclass
                    iterl=[]
                    print("Generating--------")
    
                    print(counter(tick[po]),counter(lop[po]))
                    item=item.strip("<")
                    item=item.strip(">")
                    item=item.strip("class")
                    item=eval(item)
                    item=item.strip("__")
                    item=item.strip("main")
                    item=item.strip("__")
                    item=item.strip(".")
                    item=eval(item)
                    print(type(item))
                    if self.windows==None:
                        bello=item(window=None)
                    else:
                        bello=item(window=self.windows[np])
                    iterl.append(bello)
                
                    inter,_=iterl[np].main(tick,lop[po])
                    signals.append(inter)
                    select.append(iterl[np])
                    po+=1
                except AttributeError:
                    continue
            #return signals
            print("Generated signal ...")
            ip=0
            bought=price_values.bought.tolist()
            sold=price_values.sold.tolist()
            self.portfolio=price_values.portfolio.tolist()
            amount_of_shares=price_values.amount.tolist()
            self.capital=price_values.capital.tail(1)
            stopl=[]
            target=[]
            capital=self.capital/self.stockno
            print("Making a decision !!!")
            for items in signals:
                try:
                    signal,_,mo=self._find_ifbought(lil1=tickers,lil2=items)
                except TypeError:
                    signal="Neutral"
                    print("Neutral")
                    continue
                if signal=="Buy":
                    cost=lop[mo].Close.tail(1)
                    amount_shares=self.amount_share_finder(capital=capital,price=cost)
                    price=self.Order(comm="Buy",capital=capital,data=lop,no=mo,amount_of_shares=amount_shares)
                    select[ip].held=True
                    bought.append(price)
                    amount_of_shares.append(amount_shares)
                    self.portofolio.append(tick[mo])
                    select[ip].riskfa(lop[mo][ip])
                    select[ip].profitfa(lop[mo][ip])
                    #print(lop[mo][ip])
                    #Trying to remove the data from it,
                    stopl.append(lop[mo][ip].Close.tail(1)-select[ip].stop())
                    target.append(select[ip].target.tail(1)*self.amount_shares)
                elif signal=="Sell":
                    price=self.Order(comm="Sell",capital=capital,data=lop,no=mo,amount_of_shares=amount_of_shares)
                    select[ip].held=False
                    sold.append(price)
                    self.portfolio.remove(tick[mo])
                elif stopl[ip]<=bought[ip]:
                    price=self.Order(comm="Sell",capital=capital,data=lop,no=mo,amount_of_shares=amount_of_shares)
                    select[ip].held=False
                    sold.append(price)
                    self.portfolio.remove(tick[mo])
                elif  target[ip]>=bought[ip]:
                    price=self.Order(comm="Sell",capital=capital,data=lop,no=mo,amount_of_shares=amount_of_shares)
                    select[ip].held=False
                    sold.append(price)
                    self.portfolio.remove(tick[mo])
                elif day/week==7.0:
                    price=self.Order(comm="Sell",capital=capital,data=lop,no=mo,amount_of_shares=amount_of_shares)
                    select[ip].held=False
                    sold.append(price)
                    self.portfolio.remove(tick[mo])
            if day/week==7.0: 
                data={"Price_bought":bought,"Price_sold":sold}
                data_frame=pd.DataFrame(data)
                ep=self.Bot(initial_capital=self.capital,comission=self.commision,price_sold=data_frame["Price_sold"],price_bought=data_frame["Price_bought"],data_amount=self.data).loop()
                ep.to_csv("ep,day"+day+".csv")
                message=Message(selfmail=self.mail,selfpass=self.mailpass)
                message.create_message(prev="Total trade for the week are")
                message.send_message("ep,day"+day+".csv")
                week+=1
                self.capital=ep.capital.sum()
            timedata={"times":time1,"hours":hours1,"day":day,"week":week}
            time_file=pd.DataFrame(data=timedata)
            time_file.to_csv("time_file.csv")
            prices_dict={"portfolio":portfolio,"bought":bought,"sold":sold,"amount":amount_of_shares,"capital":self.capital}
            price_values=pd.DataFrame(data=prices_dict)
            price_values.to_csv("price_values.csv")
            print("Done")
            pass
        else:
            print("The time is not %d",(self.settime))
            #quit()
            pass
            
            
            
            
        """The structure remains cashbots exceptions and message/mail etc""" 
        
            
        
        pass
    
    
class Backtester(object):
    "Class to backtest the  tradingrules or selector and give you the plotted results"
    def __init__(self,amount=100.0,initial_caps=1000.0,comms=0.0,data_amount=0.0,window:list=[[10,25,190],10,40,250]):
        """Function to initialize the
        starting capital,commition,amountofshares,data_amount"""
        self.amount_of_shares=amount
        self.initial_capital=initial_caps
        self.commition=comms
        self.data=data_amount
        self.windows=window
    def rbacktest(self,_input_):
        """Function to majorly perform the backtest"""
        #Rbacktest uses adj close
        trade=TrendTrade(window=self.windows)
        self.signals=trade.trading_rule(_input_)
        self.signals['positions']=self.signals['positions']*self.amount_of_shares
        
        pos_diff=self.signals['positions'].diff()
        portfolio=pd.DataFrame(index=self.signals.index)
        portfolio["transacts"]=self.signals['positions']*_input_['Adj Close']
        portfolio['holdings']=(self.signals['positions']*_input_['Adj Close']).sum(axis=0)
        #portfolio['cash']=self.initial_capital-(pos_diff*_input_['Adj Close']).sum(axis=0).cumsum()
        #portfolio['total']=portfolio['cash']+portfolio['holdings']
        
        
        
        return  portfolio
    
    def backtest(self,entry,exits,_input_):
        trade=TrendTrade(entry,exits,window=self.windows)
        self.signals=trade.trading_rule(_input_)
        self.price=pd.DataFrame(index=self.signals.index)
        try:
            self.price['price_bought']=np.where(np.equal(self.signals['positions'],1),_input_['Adj Close']*self.amount_of_shares,0)
            self.price['price_sold']=np.where(np.equal(self.signals['positions'],-1),_input_['Adj Close']*self.amount_of_shares,0)
        except:
            self.price['price_bought']=np.where(np.equal(self.signals['positions'],1),_input_['Close']*self.amount_of_shares,0)
            self.price['price_sold']=np.where(np.equal(self.signals['positions'],-1),_input_['Close']*self.amount_of_shares,0)
        #g=self.price.values.tolist()
        sell,buy=pd_editzero(self.price)
        #buy,sell=list_extractor(g)
        buy,sell=dataframetor(buy,sell)
        data={'Price_bought':buy,'Price_sold':sell}
        self.amount=pd.DataFrame(data=data)
        ep=CashflowStatementBot(initial_capital=self.initial_capital,commision=self.commition,price_sold=self.amount['Price_sold'],price_bought=self.amount['Price_bought'],data_amount=self.data).loop()
        
        return ep
    def macdbacktest(self,_input_,Type:Indicator=SimpleMovingAverage,ma_type=MACD2):
        if ma_type!=MACD2 and ma_type!=MACD3:
            trade=ma_type(Type)
        else:
            trade=ma_type()
        self.signals=trade.output_(_input_)
        self.price=pd.DataFrame(index=self.signals.index)
        self.price['price_bought']=np.where(np.equal(self.signals['positions'],1),_input_['Close']*self.amount_of_shares,0)
        self.price['price_sold']=np.where(np.equal(self.signals['positions'],-1),_input_['Close']*self.amount_of_shares,0)
        #g=self.price.values.tolist()
        sell,buy=pd_editzero(self.price)
        #buy,sell=list_extractor(g)
        buy,sell=dataframetor(buy,sell)
        data={'Price_bought':buy,'Price_sold':sell}
        self.amount=pd.DataFrame(data=data)
        ep=CashflowStatementBot(initial_capital=self.initial_capital,commision=self.commition,price_sold=self.amount['Price_sold'],price_bought=self.amount['Price_bought'],data_amount=self.data).loop()
        return ep
    def rulestest(self,_input_):
        pass
        
    def _netprofit(self,_input_):
        #Function to calculate on netprofit 
         
        #pct_change=_input_["netprofit"].pct_change().sum()
        """
        The below code removes the zero's and places them in contrast"""
        prof2=pd.DataFrame(index=_input_.index)
        prof2["winning_trade"]=0
        prof2["losing_trade"]=0
        prof2["winning_trade"]=np.where(np.greater(_input_["netprofit"],0),_input_["netprofit"],0)
        prof2["losing_trade"]=np.where(np.less(_input_["netprofit"],0),_input_["netprofit"],0)
        wi,los=pd_editzero(prof2,x="winning_trade",y="losing_trade")
        win1,loss1=wi,los
        removzerset(0,win1)
        removzerset(0,loss1)
        loss,win=dataframetor(loss1,win1)
        data={'lossing_trade':loss,'winning_trade':win}
        pof3=pd.DataFrame(data=data)
        """
        This calculates number of trades
        """
        prof2["trade"]=0
        prof2["trades"]=np.where(np.equal(_input_["price_sold"],0),0,_input_["netprofit"])
        no_of_trade=prof2["trades"].values.tolist().__len__()
        
        """
        Here we continue our profit
        """
        profit=pd.DataFrame()
        profit["tnetprofit"]=(pof3["winning_trade"]+pof3["lossing_trade"])
        profit["totalnetprofit"]=profit["tnetprofit"].sum()

        pct_change=(pof3["winning_trade"]+pof3["lossing_trade"])/((win.__len__()+loss.__len__()))
        profit["pct_change"]=pct_change.pct_change().sum()/1000
        profit["winning_trade"]=win1.__len__()
        profit["lossing_trades"]=loss1.__len__()
        profit["Max_win"]=isgreatest(win)
        profit["Max_loss"]=isgreatest(loss,hin='min')
        profit["Total_win"]=pof3.winning_trade.sum()
        profit["Total_loss"]=pof3.lossing_trade.sum()
        profit["Average_totalnetprofit"]=profit["totalnetprofit"]/no_of_trade
        profit["Average_netloss"]=(pof3["lossing_trade"]/loss1.__len__()).sum()
        profit["Average_netprofit"]=(pof3["winning_trade"]/win1.__len__()).sum()
        profit["Average win %"]=profit["Total_win"]/((win1.__len__()+loss.__len__()*100))
        profit["Average lose %"]=profit["Total_loss"]/((win1.__len__()+loss.__len__())*100)
        profit["Max Concecutive win"]=range_concencutive(wi)
        profit["Max Concecutive loss"]=range_concencutive(los)
        profit["Ratio of average prof-loss"]=profit["Average_netprofit"]/profit["Average_netloss"]
        profit["Expentancy"]=(profit["Average win %"]*profit["Average_netprofit"]+profit["Average lose %"]*profit["Average_netloss"])/(-profit["Average_netloss"])
        #Add tharpe,profit factor, expentancy,
        
        return profit,pof3
    def _grossprofit(self,_input_):
        #Performs operations on gross profit
        """
        The below code removes the zero's and places them in contrast"""
        prof2=pd.DataFrame(index=_input_.index)
        prof2["winning_trade"]=0
        prof2["losing_trade"]=0
        prof2["winning_trade"]=np.where(np.greater(_input_["grossprofit"],0),_input_["grossprofit"],0)
        prof2["losing_trade"]=np.where(np.less(_input_["grossprofit"],0),_input_["grossprofit"],0)
        win1,loss1=pd_editzero(prof2,x="winning_trade",y="losing_trade")
        loss,win=dataframetor(loss1,win1)
        data={'lossing_trade':loss,'winning_trade':win}
        pof3=pd.DataFrame(data=data)
        """
        This calculates number of trades
        """
        prof2["trade"]=0
        prof2["trades"]=np.where(np.equal(_input_["price_sold"],0),0,_input_["grossprofit"])
        no_of_trade=prof2["trades"].values.tolist().__len__()
        
        """
        Here we continue our profit
        """
        profit=pd.DataFrame()
        profit["tgrossprofit"]=(pof3["winning_trade"]+pof3["lossing_trade"])
        profit["totalgrossprofit"]=profit["tgrossprofit"].sum()

        pct_change=(pof3["winning_trade"]+pof3["lossing_trade"])/((win.__len__()+loss.__len__()))
        profit["pct_change"]=pct_change.pct_change().sum()/1000
        profit["winning_trade"]=win1.__len__()
        profit["lossing_trades"]=loss1.__len__()
        profit["Max_win"]=isgreatest(win)
        profit["Max_loss"]=isgreatest(loss,hin='min')
        profit["Total_win"]=pof3.winning_trade.sum()
        profit["Total_loss"]=pof3.lossing_trade.sum()
        profit["Average_totalgrossprofit"]=profit["totalgrossprofit"]/no_of_trade
        profit["Average_grossloss"]=(pof3["lossing_trade"]/loss1.__len__()).sum()
        profit["Average_grossprofit"]=(pof3["winning_trade"]/win1.__len__()).sum()
        profit["Average win %"]=profit["Total_win"]/((win1.__len__()+loss.__len__()*100))
        profit["Average lose %"]=profit["Total_loss"]/((win1.__len__()+loss.__len__())*100)
        profit["Ratio of average prof-loss"]=profit["Average_grossprofit"]/profit["Average_grossloss"]
        profit["Expentancy"]=(profit["Average win %"]*profit["Average_grossprofit"]+profit["Average lose %"]*profit["Average_grossloss"])/(-profit["Average_grossloss"])
        #Add tharpe,profit factor, expentancy,
        
        return profit,pof3
    def _cashflow(self,_input_):
        #Performs an operation on cashflow
        cashflow=_input_.cahflow
        profit=pd.DataFrame()
        profit["total_cash_flow"]=cashflow.sum()
        profit["pct_change"]=cashflow.pct_change().sum()
        return profit
        
        
    
    pass
    
class FractionalShares(Portfolio):
    "Major class for your stocks using a fintech company"
    def __init__(self,Bot:CashflowStatementBot,rules:Selector,API:APImode,model:MLfundamen,stocklist:pd.Timestamp,capital:float=10000.0,APIKeys:list=[],period:str='1 week'):
        self.rules=TrendTrade
        self.stocklist=stocklist
        self.capital=capital
        self.Bot=CashflowStatementBot
        self.keys=APIKeys
        self.model=MLfundamen
        self.api=APImode
        self.period=period
        
        super(FractionalShares).__init__(Bot,)
    def total_risk(self):
        return self.rules.riskfa
        
        
'''aapl=pdr.get_data_yahoo('AAPL',
                        start=datetime.datetime(2006,10,1),
                        end=datetime.datetime(2020,1,1))'''

#df=pd.read_csv("aapl_ohoc.csv")


    
 

