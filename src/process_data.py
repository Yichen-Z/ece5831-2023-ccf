import joblib
import pandas as pd


def save_space(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(columns=['Merchant Name'], inplace=True)

    df['MCC'] = df['MCC'].astype('int32')

    df['Amount'] = df['Amount'].apply(lambda value: float(value[1:]))
    df['Amount'] = df['Amount'].astype('float32')

    df['Use Chip'] = df['Use Chip'].apply(lambda word: word.split()[0])

    return df


def get_zero_padded(input_number: int) -> str:
    return f"{input_number:02}"


def set_zero_padded_cols(columns: list, df: pd.DataFrame) -> None:
    for col in columns:
        df[col] = df[col].apply(get_zero_padded)


def combine_date_cols(columns: list, result_col: str, format_str: str, df: pd.DataFrame, error_option: str = 'coerce') -> None:
    df[result_col] = pd.to_datetime(df[columns], format=format_str, errors=error_option)
    df.drop(columns=columns, inplace=True)


if __name__ == '__main__':
    raw_df = pd.read_csv('../data/credit_card_transactions-ibm_v2.csv')
    raw_df = save_space(df=raw_df)
    set_zero_padded_cols(columns=['Month', 'Day'], df=raw_df)
    combine_date_cols(columns=['Year', 'Month', 'Day'], result_col='transaction_datetime',
                      format_str='%Y-%m-%d')
