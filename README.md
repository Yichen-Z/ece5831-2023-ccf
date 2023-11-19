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

3) To make the transactions data take up less space, first run src/processs_data.py from the terminal:
    ```
    cd src
    python -m process_data
    ```

    Then run src/combine_data.py from the terminal:
    ```
    python -m combine_data
    ```
