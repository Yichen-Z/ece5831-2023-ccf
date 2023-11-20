import joblib
import numpy as np
import os
import pandas as pd

COL_NAMES = ['User','Card','Year','Month','Day','Time','Amount','Use_Chip',
             'Merchant_Name','Merchant_City','Merchant_State','Zip','MCC','Errors','Is_Fraud']
PARSE_DATES = ['Year', 'Month', 'Day', 'Time']
FROM_DIR = '../data/split'
TO_DIR = '../data/slim'
PART_NAME = 'transactions'


def save_space(df: pd.DataFrame, basic: bool) -> pd.DataFrame:
    df = get_slimmed_numerics(df, basic)
    df['Is_Fraud'] = df['Is_Fraud'].apply(lambda word: True if word.lower() == 'yes' else False)
    df['Use_Chip'] = df['Use_Chip'].apply(lambda word: word.split()[0])
    return df


def get_numeric_amount(df: pd.DataFrame) -> None:
    df['Amount'] = df['Amount'].apply(lambda value: float(value[1:]))
    df['Amount'] = df['Amount'].astype('float32')


def get_slimmed_numerics(df: pd.DataFrame, basic: bool) -> pd.DataFrame:
    """Adapted from Konrad Banachewicz reduce_mem_usage"""
    if basic:
        df = df.astype({col: 'int32' for col in df.select_dtypes('int64').columns})
        df = df.astype({col: 'float32' for col in df.select_dtypes('float64').columns})
    else:
        for col in df.select_dtypes(include=[np.number]).columns:
            col_type = df[col].dtype
            col_min = df[col].min()
            col_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if col_min >= np.iinfo(np.int8).min and col_max <= np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif col_min >= np.iinfo(np.int64).min and col_max <= np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if col_min >= np.finfo(np.float16).min and col_max <= np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif col_min >= np.finfo(np.float32).min and col_max <= np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                elif col_min >= np.finfo(np.float64).min and col_max <= np.finfo(np.float64).max:
                    df[col] = df[col].astype(np.float64)
    return df


def combine_date_cols(columns: list, result_col: str, df: pd.DataFrame, format_str: str = '%Y-%m-%d %H:%M', error_option: str = 'coerce') -> None:
    df[result_col] = df[columns[0]].astype(str) + '-' + df[columns[1]].astype(str) + '-' + \
        df[columns[2]].astype(str) + ' ' + df[columns[3]]
    df[result_col] = pd.to_datetime(df[result_col], format=format_str, cache=True, errors=error_option)
    df.drop(columns=columns, inplace=True)


if __name__ == '__main__':
    parts = [f for f in os.listdir(FROM_DIR)]
    print(parts)
    i = 0
    for part in parts:
        temp_df = pd.read_csv(os.path.join(FROM_DIR, part), header=None, names=COL_NAMES)
        combine_date_cols(columns=PARSE_DATES, result_col='Datetime', df=temp_df)
        get_numeric_amount(df=temp_df)
        temp_df = save_space(df=temp_df, basic=False)
        joblib.dump(temp_df, f'{TO_DIR}/{PART_NAME}_{i}')
        i += 1
