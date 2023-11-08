import joblib
import pandas as pd


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
    set_zero_padded_cols(columns=['Month', 'Day'], df=raw_df)
    combine_date_cols(columns=['Year', 'Month', 'Day'], result_col='transaction_datetime',
                      format_str='%Y-%m-%d')
