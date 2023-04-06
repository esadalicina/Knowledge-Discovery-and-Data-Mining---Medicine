from flask import Flask, render_template
import plotly.graph_objs as go
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    # Create some data
    x = [1, 2, 3, 4, 5]
    y = [10, 8, 6, 4, 2]

    # Create a plotly graph
    fig = go.Figure(data=[go.Scatter(x=x, y=y, mode='lines')])

    # Render the template with the plotly graph
    return render_template('index.html', plot=fig.to_html())



if __name__ == '__main__':
    app.run(debug=True)



