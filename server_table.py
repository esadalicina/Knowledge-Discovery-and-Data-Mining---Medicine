import numpy as np
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
start = 0
length = 0
order = 0
leftAttribute = "None"
rigthAttribute = "None"
search_lift = ">0"
search_confidence = ">0"
direction = True


@app.route('/')
def index():
    with open("association2NoFilter.csv", "r") as f:
        df = pd.read_csv(f)
    column_names = list(df.columns)

    # Get the unique values in each column
    unique_values = {}
    for column in column_names:
        unique_values[column] = list(df[column].unique())
    first = df["lhs_attribute"].unique()
    second = df["rhs_attribute"].unique()
    first = np.insert(np.asarray(first), 0, "None")
    second = np.insert(np.asarray(second), 0, "None")

    return render_template('server_table.html', title='Assosiation Table', column_names=first,
                           r_column_names=second)


@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    global start, length, direction, order, leftAttribute, rigthAttribute, search_confidence, search_lift
    with open("association2NoFilter.csv", "r") as f:

        data_filter = pd.read_csv(f)

    pre_len = len(data_filter)
    # TODO query the 5 textfields and filter accordingly
    # Get the search query

    search_lift_ = request.args.get('lift_search')
    search_confidence_ = request.args.get('confidence_search')
    if search_lift_ is not None or search_lift != "":
        if search_lift_ != "":
            try:
                data_filter = data_filter.query('lift {}'.format(search_lift_))
                print(data_filter)
                search_lift = search_lift_
            except:
                try:
                    data_filter = data_filter.query('lift {}'.format(search_lift))
                except:
                    pass
        else:
            search_lift = ""

    if search_confidence_ is not None:
        if search_confidence_ != "":
            try:
                data_filter = data_filter.query('confidence'.format(search_confidence_))
                search_lift = search_confidence_
            except:
                try:
                    data_filter = data_filter.query('confidence'.format(search_confidence))
                except:
                    pass
        else:
            search_lift = ""
    req = request.args.to_dict()

    if req is not None and 'order[0][column]' in req:
        order = int(req["order[0][column]"])
        direction = req["order[0][dir]"] == "asc"
    if "latt" in req and req["latt"] is not None:
        leftAttribute = req["latt"]
    if "ratt" in req and req["ratt"] is not None:
        rigthAttribute = req["ratt"]
    if leftAttribute != "None":
        data_filter = data_filter.query('lhs_attribute == "{}"'.format(leftAttribute))
    if rigthAttribute != "None":
        data_filter = data_filter.query('rhs_attribute == "{}"'.format(rigthAttribute))

    to_be_filter = data_filter.columns[order]
    data_filter.sort_values(by=to_be_filter, axis="index", ascending=direction, inplace=True)
    # Get the number of filtered records
    total_filtered = pre_len - len(data_filter)

    # TODO order attribute

    # Get the pagination parameters and slice the data
    start_ = request.args.get('start', type=int)
    length_ = request.args.get('length', type=int)
    if start_ is not None:
        start = start_
    if length_ is not None:
        length = length_
    print(data_filter)
    data_page = data_filter.iloc[start:start + length]
    print(data_page)
    # Format the response
    response = {
        'data': data_page.to_dict('records'),
        'recordsFiltered': total_filtered,
        'recordsTotal': pre_len,
        'draw': request.args.get('draw', type=int)
    }

    return response


if __name__ == '__main__':
    app.run()
