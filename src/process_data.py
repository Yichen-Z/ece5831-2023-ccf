import joblib
import numpy as np
import os
import pandas as pd

import utils

COL_NAMES = ['User','Card','Year','Month','Day','Time','Amount','Use_Chip',
             'Merchant_Name','Merchant_City','Merchant_State','Zip','MCC','Errors','Is_Fraud']
PARSE_DATES = ['Year', 'Month', 'Day', 'Time']
FROM_DIR = '../data/split'
TO_DIR = '../data/slim'
PART_NAME = 'transactions'


def normalize_transaction_data(df: pd.DataFrame, err_col: str = 'Errors') -> None:
    distinct_errors = get_unique_errors(df=df, err_col=err_col)
    get_onehot_errors(df=df, err_col=err_col, err_set=distinct_errors)

    df = get_slimmed_numerics(df)


def save_space(df: pd.DataFrame, basic: bool) -> pd.DataFrame:
    df['Is_Fraud'] = df['Is_Fraud'].apply(lambda word: 1. if word.lower() == 'yes' else 0.)
    df['Use_Chip'] = df['Use_Chip'].apply(lambda word: word.split()[0])
    df = get_slimmed_numerics(df)
    return df


# Refine raw transactions dataframe
def get_numeric_amount(df: pd.DataFrame) -> None:
    df['Amount'] = df['Amount'].apply(lambda value: float(value[1:]))
    df['Amount'] = df['Amount'].astype('float32')


def get_slimmed_numerics(df: pd.DataFrame) -> pd.DataFrame:
    """Save space by converting int64 and float64 columns to 32 where possible. Adapted from Konrad Banachewicz reduce_mem_usage"""
    for col in df.select_dtypes(include=[np.number]).columns:
        col_type = df[col].dtype
        col_min = df[col].min()
        col_max = df[col].max()
        if str(col_type)[:3] == 'int':
            if col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                df[col] = df[col].astype(np.int32)
        else:
            if col_min >= np.finfo(np.float32).min and col_max <= np.finfo(np.float32).max:
                df[col] = df[col].astype(np.float32)
    return df


def combine_date_cols(columns: list, result_col: str, df: pd.DataFrame, format_str: str = '%Y-%m-%d %H:%M', error_option: str = 'coerce') -> None:
    """Splice together the Year, Month, Day, and Time columns into one column."""
    df[result_col] = df[columns[0]].astype(str) + '-' + df[columns[1]].astype(str) + '-' + \
        df[columns[2]].astype(str) + ' ' + df[columns[3]]
    df[result_col] = pd.to_datetime(df[result_col], format=format_str, cache=True, errors=error_option)
    df.drop(columns=columns, inplace=True)


# One-hot encode and normalize data helper functions
def get_unique_errors(df: pd.DataFrame, err_col: str, nan_fill: 'str' = 'None') -> set:
    df[err_col] = df[err_col].fillna(nan_fill)
    errors = df[err_col].unique().tolist()
    unique_errors = set()
    for jumbled in errors:
        for piece in jumbled.strip().split(','):
            unique_errors.add(piece)
    unique_errors.remove(nan_fill)
    return unique_errors


def get_onehot_errors(df: pd.DataFrame, err_col: str, err_set: set) -> None:
    for error in err_set:
        error_col_name = '_'.join(error.strip().lower().split(' '))
        df[error_col_name] = df[err_col].apply(lambda jumble: 1. if error in jumble else 0.)
    df.drop(columns=[err_col], inplace=True)


if __name__ == '__main__':
    parts = [f for f in os.listdir(FROM_DIR)]
    print(parts)
    i = 0
    for part in parts:
        temp_df = pd.read_csv(os.path.join(FROM_DIR, part), header=None, names=COL_NAMES)
        combine_date_cols(columns=PARSE_DATES, result_col='Datetime', df=temp_df)
        get_numeric_amount(df=temp_df)
        temp_df = save_space(df=temp_df, basic=True)
        joblib.dump(temp_df, f'{TO_DIR}/{PART_NAME}_{i}')
        i += 1
