# ece5831-2023-ccf
Collaboration repo for Pattern Recognition &amp; NN course final project on synthetic credit card fraud data

## Setup

### Conda Environment

1) Install pandas and numpy for dataframe management
2) Install tensoflow for the model training
3) Install matplotlib for the graphing

For additional testing:
4) Install seaborn for heatmap graphing
5) Install pickle for the file loading

### Data

1) After cloning this repository, create nested folders in the following structure:

    |--- data

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
## Model Building

### Data Preparation
1) The data needs to be read and processed in order to make the training and validation sets. The dataframe_loading.py script takes care of most of the process.
2) Finally, execute the model_dataframe_building.ipynb notebook.
   It will import the user data, card data, and transaction data, and make a training set and a validation set from it. The result will be:
    - normalized_train_data.pkl
    - normalized_validation_data.pkl
   It will also produce two additional files. These are just backup files, so if something went wrong during normalization one wouldn't have to execute the entire file again:
    - train_data.pkl
    - validation_data.pkl
      
### Model Training
1) Ensure that normalized_train_data.pkl and normalized_validation_data.pkl are in the same folder as model_training.ipynb
2) Open and execute model_training.ipynb
3) The data will be separated into sets and labels to train the network. Tensorflow should fit the model in about 5 minutes using GPU.
4) You should see the results of the model displayed at the end.
5) The model will be saved as CreditCardFraudDetection.keras

### Additional Model for Testing
We re-trained the model after its second iteration to run some tests, and produced some additional graphs from its results. The resulting model was not saved. If you would like to replicate this process:
1) Open and execute model_training_changes.ipynb
2) It will load and evaluate the CreditCardFraudDetection.keras file produced during training
3) The data will be loaded from normalized_train_data.pkl, normalized_validation_data.pkl, and bal_validation_data.
4) The data will be separated into sets and labels to train the network. Tensorflow should fit the model in about 5 minutes using GPU.
5) You should see the results of the model displayed at the end. It should display the results from using:
    - Balanced data (bal_validation_data)
    - Unbalanced data (normalized_validation_data)
