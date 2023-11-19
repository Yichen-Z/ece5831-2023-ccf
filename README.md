# ece5831-2023-ccf
Collaboration repo for Pattern Recognition &amp; NN course final project on synthetic credit card fraud data

## Setup

### Conda Environment

TODO

### Data

1) After cloning this repository, create nested folders in the following structure:

    |--- data

        |--- slim
        |--- split

2) Download data from [IBM Synthetic Credit Card Transactions Dataset on Kaggle](https://www.kaggle.com/datasets/ealtman2019/credit-card-transactions), unzip, and move into the **data/** directory

3) Ease processing by first splitting up the transactions csv into smaller chunks. In the terminal:
    ```
    cd data
    ./split_transactions.sh
    ```

4) Delete the header line from data/split/part00.csv. Then, to make the transactions data take up less space, first run in the terminal:
    ```
    cd ../src
    python -m process_data
    python -m combine_data
    ```
