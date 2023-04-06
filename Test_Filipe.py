import base64
import io

import flask
import matplotlib
from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly

app = Flask(__name__)


def convert_age_to_int(age_str):
    age_range = age_str.strip('[]').split('-')
    return int(age_range[0])

# Read in the data from the CSV file


# Define the routes for the application
@app.route('/')
def index():
    # Create a bar chart using Matplotlib and save it to a file
    """

    fig = plt.pyplot.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(df['gender'][1:10], df['age'][1:10])
    plt.pyplot.title('Age Distribution by Gender')
    plt.pyplot.xlabel('Gender')
    plt.pyplot.ylabel('Age')
    mpl_fig1 = plt.pyplot.gcf()

    plotly_fig1 = plotly.tools.mpl_to_plotly(mpl_fig1)

    plotly_fig1.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
    )
    """
    # Create a histogram using Seaborn and save it to a file


    with open("Cleaned.csv", "r") as f:
        df = pd.read_csv(f)
    # Create a new column to group the ages
    df['age'] = df['age'].apply(convert_age_to_int)
    df['Age Group'] = pd.cut(df['age'], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], right=False)

    # Group the data by age group and gender, and get the sum of each group
    grouped_df = df.groupby(['Age Group', 'gender']).size().unstack()
    grouped_df.index = grouped_df.index.astype(str)
    # Create a plotly bar chart with the grouped data
    fig = go.Figure()
    fig.add_trace(go.Bar(x=grouped_df.index, y=grouped_df['Female'], name='Female'))
    fig.add_trace(go.Bar(x=grouped_df.index, y=grouped_df['Male'], name='Male'))
    fig.update_layout(title='Age and Gender Distribution', xaxis_title='Age Group', yaxis_title='Count')
    # Convert the chart to HTML and pass it to the template

    return render_template('index.html', plot=fig.to_html())


if __name__ == '__main__':
    app.run(debug=True)
