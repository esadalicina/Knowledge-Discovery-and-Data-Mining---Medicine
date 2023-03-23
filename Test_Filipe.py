from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# Read in the data from the CSV file
df = pd.read_csv('data.csv')

# Define the routes for the application
@app.route('/')
def index():
    # Create a bar chart using Matplotlib and save it to a file
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(100)
    ax.bar(df['gender'], df['age'])
    plt.title('Age Distribution by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Age')
    plt.savefig('static/bar_chart.png')

    # Create a histogram using Seaborn and save it to a file
    sns.histplot(data=df, x='age', hue='gender', kde=True)
    plt.title('Age Distribution by Gender')
    plt.savefig('static/histogram.png')

    # Render the HTML template with the two charts embedded
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)