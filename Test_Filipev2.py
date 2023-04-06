import pandas as pd
import numpy as np

with open("data.csv", "r") as f:
    df = pd.read_csv(f, name=['diabetesMed'], sep=',')


print(df.head())