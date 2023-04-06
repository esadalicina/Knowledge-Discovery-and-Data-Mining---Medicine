import pandas as pd

with open("association1.csv","r") as f:
    df = pd.read_csv(f)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

df_rules_sorted = df.sort_values(by=['support'], ascending=False)
print(df_rules_sorted)
df_rules_sorted = df.sort_values(by=['confidence'], ascending=False)
print(df_rules_sorted)
df_rules_sorted = df.sort_values(by=['lift'], ascending=False)
print(df_rules_sorted.head())
df_rules_sorted = df.sort_values(by=['frequency'], ascending=False)
print(df_rules_sorted.head())