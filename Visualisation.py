import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans



def distribution_data(title):
    df = pd.read_csv("Cleaned.csv")
    df = df[df['Diabetes'] == True]
    plt.title(title)
    sns.pairplot(df)

    plt.show()


def distribution_TwoCol(col1, col2, title):

    df = pd.read_csv("Cleaned.csv")
    df = df[df['Diabetes'] == True]
    age_column = col1
    gender_column = col2

    sns.histplot(data=df, x=age_column, hue=gender_column,multiple="dodge", shrink=.8)
    plt.title(title)

    plt.show()


def diagnostic_types():

    df = pd.read_csv('Cleaned.csv')
    df = df[df['Diabetes'] == True]
    x = df.copy()


    sns.set(font_scale=1.5)
    cm = sns.color_palette("Blues", as_cmap=True)
    confusion_matrix = pd.crosstab(x['Type1'], x['Type2'], rownames=['Type1'], colnames=['Type2'])
    sns.heatmap(confusion_matrix, cmap=cm, annot=True, fmt='g')
    plt.title('Confusion Matrix for Diabetes Diagnosis')
    plt.show()


def distribution_change_medikament():

    df = pd.read_csv('Cleaned.csv')
    x = df.copy()

    df_selected = x[['change', 'metformin','repaglinide','nateglinide','chlorpropamide','glimepiride','acetohexamide','glipizide','glyburide','tolbutamide','pioglitazone','rosiglitazone','acarbose','miglitol','troglitazone','tolazamide','insulin','glyburide-metformin','glipizide-metformin','glimepiride-pioglitazone','metformin-rosiglitazone','metformin-pioglitazone']]
    df = df_selected.replace({'Ch': True,'Steady': True, 'Up': True,'Down': True,'No': False, 'Steady ': True, 'No ': False,'Up ': True,'Down ': True, 'Ch ': True}, regex=True)

    sns.set(font_scale=1.2)
    plt.figure(figsize=(12, 10))
    sns.heatmap(df.corr(), cmap='YlGnBu', annot=True, fmt='.2f',
                annot_kws={'size': 10, 'weight': 'bold', 'color': 'green'}, linewidths=.5)
    plt.title('Co-Occurrence of Diabetes with Other Diseases')
    plt.show()


distribution_data("Data distribution")
distribution_TwoCol("age","gender","Age-Gender Distribution")
distribution_TwoCol("change","gender","Change-Gender Distribution")
distribution_TwoCol("age","change","Age-Change Distribution")
diagnostic_types()
distribution_change_medikament()



