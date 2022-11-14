#!/usr/bin/env python
# coding: utf-8

# In[40]:


from pandas_datareader import data as pdr
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import time
from pykrx import stock
import seaborn as sns

import matplotlib
from matplotlib import font_manager, rc
import platform
try : 
    if platform.system() == 'Windows':
    # 윈도우인 경우
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
    else:    
    # Mac 인 경우
        rc('font', family='AppleGothic')
except : 
    pass
   


# In[42]:


def backtest(code, k, start='2021-01-01'):
    code = str(code)+".KS"
    df=pd.DataFrame()
    df = pdr.get_data_yahoo(code, start)
    
    df['변동폭'] = df['High'] - df['Low']
    df['목표가'] = df['Open'] + df['변동폭'].shift(1)*k
    df['어제종가'] = df['Close'].shift(1)
    df['내일시가'] = df['Open'].shift(-1)
    df['어제거래량'] = df['Volume'].shift(1)
    df['그제거래량'] = df['Volume'].shift(2)
    df['시가-어제종가'] = df['Open']-df['어제종가']
    df['어제거래변동률'] = df['어제거래량'] / df['그제거래량']
    df['MA3_yes'] = df['Close'].rolling(window=3).mean().shift(1)
    df['std3_yes'] = df['Close'].rolling(window=3).std().shift(1)
    df['upper'] = df['MA3_yes']+2*df['std3_yes']
    
   #매수
    cond = ( df['High'] > df['목표가'] ) & ( df['목표가'] > df['MA3_yes'] ) &(df['목표가'] > df['upper'])
    df=df[cond]
    
    num_of_cond = df.shape[0] # 변동성 발생
    df['수익률'] = df['내일시가']/df['목표가'] - 0.0032
    df['수익률_당일'] = df['Close']/df['목표가'] - 0.0032
    df=df.iloc[:-2]
    기간수익률 = df.수익률.cumprod().iloc[-1] 
  
    print("종목명 : ", code)
    print("변동성이 발생하는 시점 : {}".format(num_of_cond))
    print("검토기간 보유 수익률 : {:.2f}%".format((df['Close'][-1]/df['Close'][0]-1)*100))
    print("익일 시가 매도 수익률 : {:.2f}%".format((df.수익률.cumprod()[-1]-1)*100))
    print("당일 종가 매도 수익률 : {:.2f}%".format((df.수익률_당일.cumprod()[-1]-1)*100))
    print("최대 수익률 : {:.2f}%".format((df.loc[df.수익률.idxmax()].수익률-1)*100),df.수익률.idxmax())
    print("최대 손해율 : {:.2f}%".format((df.loc[df.수익률.idxmin()].수익률-1)*100),df.수익률.idxmin())
    print("-"*50)
    return df

# 익일시가매도 or 당일종가매도
# 2021-01-01~ ,k=0.5일 때 현재까지 다음 5가지 종목의 수익 비교
#삼성전자,현대차,네이버,카카오,기아차
codes = ['005930','005380','035420','035720','000270']
for code in codes:
    df = backtest(code,k=0.5,start='2021-01-01')
    time.sleep(1)
    


# In[ ]:




