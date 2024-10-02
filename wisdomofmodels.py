import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plotRes(data):
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
    data = data.sort_values(['tracktime', 'totRank'], ascending=[True, True])
    data['totRankPos'] = data.groupby(['tracktime']).cumcount()
    data['totRankPos'] = data['totRankPos'] + 1
    data['PL'] = (data['finPos'] * (data['BFSP'] - 1) * 0.98) + ((data['finPos'] - 1))
    pl = round(data[data['totRankPos'] == 1].PL.sum(),2)
    bets = data[data['totRankPos'] == 1].totRankPos.sum()
    roi = ""
    if bets > 0:
      roi = round(pl / bets * 100, 2)
  
    with resColDisplay:
      sign = ''
      if pl > 0:
        sign = '+'
      outLine = str(colListText) + ' Bets ' + str(bets) + ' PL ' + sign + str(pl) + ' ROI ' + str(roi) + '%'
      st.write(outLine)
      data = data[data['totRankPos'] == 1]
      binpls = data.groupby(pd.cut(data.BFSP, [0,5,10,15,20,30,40,50,100,1000])).PL.sum()
      cut_bins = [0, 5, 10, 15, 20, 30,40,100,200,9999]
      cut_labels = ['upto5','6-10','10-15','15-20','20-30','30-40','40-100','100-200','200-']
      data['BFSPBin'] = pd.cut(data.BFSP, bins=cut_bins, labels=cut_labels) #.PL.sum()
      binpls = data.groupby('BFSPBin').PL.sum()
      xnp = np.array(cut_labels)
      ynp = np.array(binpls)
      plt.bar(xnp,ynp)
      plt.title('Flat Stakes PL by Price Bins')
      plt.xlabel('Price Bins')
      plt.ylabel('£1 PL')
      st.pyplot(plt.gcf())

  #except:
    #pass

header = st.container()
dataset = st.container()
results = st.container()

with header:
  st.title('Wisdom Of Models Dashboard')

with dataset:
  st.header('Wisdom Data')
  #data = pd.read_csv('../wom/todayswom/finalres/mergedratfilesbfsp2324.csv')
  data = pd.read_csv('http://www.smartersig.com/mergedratfilesBFSP2324.csv')
  #firstline = data.head(1)
  #datebits = firstline['tracktime']
  #datebits = datebits[0].split('_')
  #startdate = datebits[2]
  #datebits = data.tail(1)['tracktime']
  #print (data.tail(1))
  #datebits = lastline['tracktime']
  #print ('datebits ',datebits)
  #datebits = datebits[0].split('_')
  #enddate = datebits[2]
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
