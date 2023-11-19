import joblib
import numpy as np
import os
import pandas as pd


def save_space(df: pd.DataFrame) -> pd.DataFrame:
    df['User'] = df['User'].astype(np.int8)
    df['Card'] = df['Card'].astype(np.int8)
    df = get_slimmed_numerics(df)
    df['Use_Chip'] = df['Use_Chip'].apply(lambda word: word.split()[0])
    return df


def get_numeric_amount(df: pd.DataFrame) -> None:
    df['Amount'] = df['Amount'].apply(lambda value: float(value[1:]))
    df['Amount'] = df['Amount'].astype('float32')


def get_slimmed_numerics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.astype({col: 'int32' for col in df.select_dtypes('int64').columns})
    df = df.astype({col: 'float32' for col in df.select_dtypes('float64').columns})
    return df


def combine_date_cols(columns: list, result_col: str, df: pd.DataFrame, format_str: str = '%Y-%m-%d %H:%M', error_option: str = 'coerce') -> None:
    df[result_col] = df[columns[0]].astype(str) + '-' + df[columns[1]].astype(str) + '-' + \
        df[columns[2]].astype(str) + ' ' + df[columns[3]]
    df[result_col] = pd.to_datetime(df[result_col], format=format_str, cache=True, errors=error_option)
    df.drop(columns=columns, inplace=True)


if __name__ == '__main__':
    COL_NAMES = ['User','Card','Year','Month','Day','Time','Amount','Use_Chip',
                 'Merchant_Name','Merchant_City','Merchant_State','Zip','MCC','Errors','Is_Fraud']
    PARSE_DATES = ['Year', 'Month', 'Day', 'Time']
    parts = [f for f in os.listdir('../data/split/') if f.endswith('.csv')]
    i = 0
    for part in parts:
        temp_df = pd.read_csv(part, header=None, names=COL_NAMES)
        combine_date_cols(columns=PARSE_DATES, result_col='Datetime', df=temp_df)
        get_numeric_amount(df=temp_df)
        temp_df = save_space(temp_df)
        joblib.dump(temp_df, f'../data/slim/transactions_{i}')
        i += 1
