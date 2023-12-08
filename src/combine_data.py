import joblib
import os
import pandas as pd

from process_data import TO_DIR, PART_NAME


if __name__ == '__main__':
    dfs = []
    parts = [f for f in os.listdir(TO_DIR)]
    
    for part in parts:
        dfs.append(joblib.load(os.path.join(TO_DIR, part)))
    
    tdf = pd.concat(dfs)
    tdf = tdf.sort_values(by=['Datetime'])
    joblib.dump(tdf, f'../data/{PART_NAME}')
