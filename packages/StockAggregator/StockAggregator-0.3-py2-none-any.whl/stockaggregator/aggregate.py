#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import FundamentalAnalysis as fa
import pandas as pd
import numpy as np
import re

def for_stocks(stocks,func,period=['annual','quarter'],
               axis=['Document','Firm','Type','Account','Period'],
               cols={0:'Value'},*args,**kwargs):
    func_available = {'balance_sheet_statement':{'call':fa.balance_sheet_statement,'params':period},
                    'cash_flow_statement':{'call':fa.cash_flow_statement,'params':period},
                    'income_statement':{'call':fa.income_statement,'params':period},
                    'key_metrics':{'call':fa.key_metrics,'params':period},
                    'financial_ratios':{'call':fa.financial_ratios,'params':{}},
                    'financial_statement_growth':{'call':fa.financial_statement_growth,'params':period}}
    df={}
    if isinstance(period, str):
        period=[period]
    for f in func:
        if f in func_available:
            df.update({f:{}})
            for stock in stocks:
                df[f].update({stock:{}})
                for p in func_available[f]['params']:
                    df[f][stock].update({p : func_available[f]['call'](stock,p)})
                if not func_available[f]['params']:
                    df[f][stock].update({'NoType' : func_available[f]['call'](stock)})
                df[f][stock]=pd.concat(df[f][stock])
            df[f]=pd.concat(df[f])
    df=pd.concat(df).stack().rename_axis(index=axis)
    df = df.reset_index().rename(columns=cols).set_index(axis)
    df.Value = pd.to_numeric(df.Value,errors='coerce')
    return df
