import pandas as pd
import numpy as np
#from mlxtend.frequent_patterns import apriori, association_rules

df = pd.read_csv("Cleaned.csv", names=['patient_nbr'])
df.head()


print(df.head())