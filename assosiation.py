import pandas as pd

# load the dataset
df = pd.read_csv("Cleaned.csv")
df.drop("patient_nbr",inplace=True,axis=1)
# list of column names
col_names = df.columns.tolist()

# find all possible value combinations for each column
possible_value_combinations = {}

for col in col_names:
    possible_values = list(set(df[col].values))
    possible_value_combinations[col] = possible_values

# create a list of all possible association rules
association_rules_list = []
for col in col_names:
    if col in possible_value_combinations:
        for val in possible_value_combinations[col]:
            assoc_rule = (col, val)
            association_rules_list.append(assoc_rule)

# create a list to store the results
results = []

# iterate through all possible association rules
counter = 0
total = len(association_rules_list)
for lhs_col, lhs_val in association_rules_list:
    print("Counter is at {}/{}".format(counter,total))
    counter += 1
    # create a mask for rows where lhs_col is equal to lhs_val
    lhs_mask = (df[lhs_col] == lhs_val)
    lhs_count = lhs_mask.sum()

    # iterate through all other columns
    for rhs_col in col_names:
        # skip the same column or columns with no possible value combinations
        if rhs_col == lhs_col or rhs_col not in possible_value_combinations:
            continue

        # iterate through all possible values for rhs_col
        for rhs_val in possible_value_combinations[rhs_col]:
            # create a mask for rows where rhs_col is equal to rhs_val
            rhs_mask = (df[rhs_col] == rhs_val)
            rhs_count = rhs_mask.sum()

            # create a mask for rows where both lhs_col is equal to lhs_val and rhs_col is equal to rhs_val
            joint_mask = lhs_mask & rhs_mask
            joint_count = joint_mask.sum()

            # calculate support, confidence, lift, and frequency
            support = joint_count / len(df)
            confidence = joint_count / lhs_count
            lift = support / (lhs_count / len(df)) / (rhs_count / len(df))
            frequency = joint_count / rhs_count

            # add the result to the list
            result = {
                "lhs_attribute": lhs_col,
                "lhs_value": lhs_val,
                "rhs_attribute": rhs_col,
                "rhs_value": rhs_val,
                "support": support,
                "confidence": confidence,
                "lift": lift,
                "frequency": frequency
            }
            results.append(result)

# create a dataframe from the results
df_results = pd.DataFrame(results)

with open("association2NoFilter.csv","w") as f:
    df_results.to_csv(f,index=False,lineterminator="\n")

# print the first 10 rows of the dataframe
print(df_results.head(10))
