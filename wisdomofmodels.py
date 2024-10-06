import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy.stats import t
from scipy import stats

def getPvalue (roi,totBFSP,numOfBets):

  y = roi / 100
  pvalue = '?'
  if numOfBets > 0:
    avgOdds = totBFSP / numOfBets
    stdev = ((1 + y)*(avgOdds - 1 - y)) ** 0.5
    try:
      tstat = y * (numOfBets ** 0.5) / stdev
    except:
      return '?'
    pvalue = round(t.sf(abs(tstat), df=numOfBets - 1),2)

  return pvalue

##################### end getPvalue #########################

def plotRes(data):

  with resColDisplay:
    showRank =st.selectbox('Show',options=['Top Rated','2nd Top Rated','3rd Top Rated'])

  rankPos = {}
  rankPos['Top Rated'] = 1
  rankPos['2nd Top Rated'] = 2
  rankPos['3rd Top Rated'] = 3

  possCols = [malRank,hdemetRank,EMSAIRank,SMSAIRank,poultodRank,rstjRank,BFSPRank]
  colText = ['malRank','hdemetRank','EMSAIRank','SMSAIRank','poultodRank','rstjRank','BFSPRank']
  colList = []
  colListText = []
  for acol in possCols:
    if acol:
      colList.append(True)
    else:
      colList.append(False)
  row = 0
  for bool in colList:
    if bool:
      colListText.append(colText[row])
    row += 1

  if len(colListText) > 0:
    data['totRank'] = data[colListText].sum(axis=1)
    data = data[data['totRank'] != 0]
    data = data.sort_values(['tracktime', 'totRank'], ascending=[True, True])
    data['totRankPos'] = data.groupby(['tracktime']).cumcount()
    data['totRankPos'] = data['totRankPos'] + 1
    data['PL'] = (data['finPos'] * (data['BFSP'] - 1) * 0.98) + ((data['finPos'] - 1))

    if showRank:
      pl = round(data[data['totRankPos'] == rankPos[showRank]].PL.sum(),2)
    
      bets = data[data['totRankPos'] == 1].totRankPos.sum()
      totBFSP = data[data['totRankPos'] == rankPos[showRank]].BFSP.sum()
      roi = ""
      if bets > 0:
        roi = round(pl / bets * 100, 2)
      pValue = getPvalue(roi,totBFSP,bets)

      with resColDisplay:
        sign = ''
        if pl > 0:
          sign = '+'

        data = data[data['totRankPos'] == rankPos[showRank]]
        binpls = data.groupby(pd.cut(data.BFSP, [0,5,10,15,20,30,40,50,100,1000])).PL.sum()
        cut_bins = [0, 5, 10, 15, 20, 30,40,100,200,9999]
        cut_labels = ['upto5','6-10','10-15','15-20','20-30','30-40','40-100','100-200','200-']
        data['BFSPBin'] = pd.cut(data.BFSP, bins=cut_bins, labels=cut_labels) #.PL.sum()
        binpls = data.groupby('BFSPBin').PL.sum()

        outLine = showRank + ' ' + str(colListText) + ' Bets ' + str(bets) + ' PL ' + sign + str(pl) + ' ROI ' + str(roi) + '%' + ' p value ' + str(pValue)
        binBetCount = data.groupby('BFSPBin').PL.count()
        barTops = np.array(binBetCount)
        outLine = outLine + ' Bets per bin ' + str(barTops)
        st.write(outLine)
        
        xnp = np.array(cut_labels)
        ynp = np.array(binpls)
        plt.bar(xnp,ynp)
        plt.title('Flat Stakes PL by Price Bins')
        plt.xlabel('Price Bins')
        plt.ylabel('£1 PL')
        st.pyplot(plt.gcf())

#########################################################

header = st.container()

results = st.container()
dataset = st.container()

with header:
  st.title('Wisdom Of Models Dashboard')

with dataset:
  st.header('Wisdom Data')
  #data = pd.read_csv('../wom/todayswom/finalres/mergedallratfilesBFSP2324.csv')
  data = pd.read_csv('http://www.smartersig.com/mergedallratfilesBFSP2324.csv')
  st.write(data.head(3))

with results:
  st.header('Wisdom Results') # + str(startdate)) # + ' - ' + str(enddate))
  resColSel, resColDisplay = st.columns([0.3,0.7])
  try:
    resChoice
  except:
    resChoice = ""
  with resColSel:
    malRank = st.checkbox('malRank')
    hdemetRank = st.checkbox('hdemetRank')
    EMSAIRank = st.checkbox('EMSAIRank')
    SMSAIRank = st.checkbox('SMSAIRank')
    poultodRank = st.checkbox('poultodRank')
    rstjRank = st.checkbox('rstjRank')
    BFSPRank = st.checkbox('BFSPRank')
    plotRes(data)
