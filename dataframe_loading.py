
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.process_data import get_zero_padded
import datetime as dt

CARDS_FILENAME = 'data/sd254_cards.csv'
USERS_FILENAME = 'data/sd254_users.csv'
TRANSACTIONS_FILENAME = 'data/credit_card_transactions-ibm_v2.csv'

def EncodeColumns(df, cols, target_column_name):
    target_encoding_map = {}

    for col in cols:
        encoding = df.groupby(col)[target_column_name].mean().to_dict()

        df[col + "_target_encoded"] = df[col].map(encoding)

        target_encoding_map[col] = encoding

    df.drop(columns=cols, inplace=True)

    return df

def LoadUsers():
    df = pd.read_csv(USERS_FILENAME)
    df.columns = [x.lower() for x in df.columns]
    df.columns = [x.replace(' - ', ' ') for x in df.columns]
    df.columns = [x.replace(' ', '_') for x in df.columns]
    #df.columns = [x.replace(' ', '_') for x in df.columns]

    df['per_capita_income_zipcode'] = df['per_capita_income_zipcode'].apply(lambda value: float(value[1:]))
    df['yearly_income_person'] = df['yearly_income_person'].apply(lambda value: float(value[1:]))
    df['total_debt'] = df['total_debt'].apply(lambda value: float(value[1:]))
    

    df = df.drop('person', axis=1)
    df = df.drop('address', axis=1)
    df = df.drop('apartment', axis=1)
    df = df.drop('latitude', axis=1)
    df = df.drop('longitude', axis=1)
    
    return df

def LoadCards():
    df = pd.read_csv(CARDS_FILENAME)
    df.columns = [x.lower() for x in df.columns]
    df.columns = [x.replace(' ', '_') for x in df.columns]

    #df.acct_open_date = df.apply(lambda x: dt.datetime.strptime(str(x), '%d/%m/%Y').date())
    #print(df.acct_open_date.apply(lambda x: dt.datetime.strptime(str(x), '%m/%Y').date()))
    df['acct_open_month'] = pd.DatetimeIndex(df['acct_open_date']).month
    df['acct_open_year'] = pd.DatetimeIndex(df['acct_open_date']).year
    df = df.drop('acct_open_date', axis=1)

    df['expires_month'] = pd.DatetimeIndex(df['expires']).month
    df['expires_year'] = pd.DatetimeIndex(df['expires']).year
    df = df.drop('expires', axis=1)
    #print(df.acct_open_date.apply(lambda x: print(str(x))))

    df['has_chip'] = df['has_chip'].replace('YES', 1)
    df['has_chip'] = df['has_chip'].replace('NO', 0)

    df['card_on_dark_web'] = df['card_on_dark_web'].replace('Yes', 1)
    df['card_on_dark_web'] = df['card_on_dark_web'].replace('No', 0)

    df['credit_limit'] = df['credit_limit'].apply(lambda value: float(value[1:]))

    df = df[['user','card_index','card_brand','card_type','card_number','expires_month', 'expires_year', 
             'cvv', 'has_chip', 'cards_issued', 'credit_limit', 'acct_open_month', 'acct_open_year', 'year_pin_last_changed', 'card_on_dark_web']]

    return df

def LoadRawTransactions():
    tdf = pd.read_csv(TRANSACTIONS_FILENAME)
    return tdf

def refactorTransactions(tdf):

    tdf.columns = [x.lower() for x in tdf.columns]
    tdf.columns = [x.replace(' ', '_') for x in tdf.columns]
    print("Column names made lowercase and spaces removed.")

    tdf.drop(columns=['merchant_name'], inplace=True)

    for col in tdf.columns:
        if tdf[col].dtype == 'int64':
            tdf[col] = tdf[col].astype(np.int32)
        elif tdf[col].dtype == 'float64':
            tdf[col] = tdf[col].astype(np.float32)

    tdf['use_chip'] = tdf['use_chip'].apply(lambda word: word.split()[0])
    print("Space removed from card method")

    tdf['amount'] = tdf['amount'].apply(lambda value: float(value[1:]))
    tdf['amount'] = tdf['amount'].astype('float32')
    print("Amount parsed into float.")
    
    timeColumn = tdf['time']
    tdf['hour'] =  timeColumn.apply(lambda word: word.split(':')[0])
    tdf['minute'] =  timeColumn.apply(lambda word: word.split(':')[1])

    print("Time split into month, day, hour, and minute")

    tdf['is_fraud'] = tdf['is_fraud?'].replace('Yes', 1)
    tdf['is_fraud'] = tdf['is_fraud'].replace('No', 0)
    print("Fraud column changed to 1 and 0")

    tdf['errors'] = tdf['errors?']
    print("Error column fixed.")
    
    tdf['errors'].fillna('None', inplace=True)
    tdf['merchant_state'].fillna('None', inplace=True)
    tdf['zip'].fillna(0, inplace=True)

    tdf = tdf.drop(columns=["time", "is_fraud?", "errors?"])
    
    return tdf