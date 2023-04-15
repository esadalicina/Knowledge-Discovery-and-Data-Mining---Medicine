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
search_support = ">0"
search_frequency = ">0"
search_lhs_value = ">0"
search_rhs_value = ">0"
direction = True

# ---------------------------------------- Attribute columns ----------------------------------------


@app.route('/')
def index():
    with open("association2NoFilter.csv", "r") as f:
        df = pd.read_csv(f)
    
    first = df["lhs_attribute"].unique()
    second = df["rhs_attribute"].unique()
    first = np.insert(np.asarray(first), 0, "None")
    second = np.insert(np.asarray(second), 0, "None")

    return render_template('server_table.html', title='Assosiation Table', l_column_names=first, r_column_names=second)


# ---------------------------------------- Column Search Fields ----------------------------------------

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    global start, length, direction, order, leftAttribute, rigthAttribute, search_confidence, search_lift, search_support, search_frequency, search_rhs_value, search_lhs_value
    with open("association2NoFilter.csv", "r") as f:

        data_filter = pd.read_csv(f)

    pre_len = len(data_filter)
    # Get the search query

    search_lift_ = request.args.get('lift_search')
    search_confidence_ = request.args.get('confidence_search')
    search_support_ = request.args.get('support_search')
    search_frequency_ = request.args.get('frequency_search')
    search_lhs_value_ = request.args.get('lhs_value_search')
    search_rhs_value_ = request.args.get('rhs_value_search')

    if search_lift_ is not None or search_lift != "":
        if search_lift_ != "":
            try:
                data_filter = data_filter.query('lift {}'.format(search_lift_))
                search_lift = search_lift_
            except:
                try:
                    data_filter = data_filter.query('lift {}'.format(search_lift))
                except:
                    pass
        else:
            data_filter = data_filter
            search_lift = ""

    if search_confidence_ is not None or search_confidence != "":
        if search_confidence_ != "":
            try:
                data_filter = data_filter.query('confidence {}'.format(search_confidence_))
                search_confidence = search_confidence_
            except:
                try:
                    data_filter = data_filter.query('confidence {}'.format(search_confidence))
                except:
                    pass
        else:
            data_filter = data_filter
            search_confidence = ""

    if search_support_ is not None or search_support != "":
        if search_support_ != "":
            try:
                data_filter = data_filter.query('support {}'.format(search_support_))
                search_support = search_support_
            except:
                try:
                    data_filter = data_filter.query('support {}'.format(search_support))
                except:
                    pass
        else:
            data_filter = data_filter
            search_support = ""

    if search_frequency_ is not None or search_frequency != "":
        if search_frequency_ != "":
            try:
                data_filter = data_filter.query('frequency {}'.format(search_frequency_))
                search_frequency = search_frequency_
            except:
                try:
                    data_filter = data_filter.query('frequency {}'.format(search_frequency))
                except:
                    pass
        else:
            data_filter = data_filter
            search_frequency = ""

    if search_lhs_value_ is not None or search_lhs_value != "":
        if search_lhs_value_ != "":
            try:
                data_filter = data_filter.query('lhs_value {}'.format(search_lhs_value_))
                search_lhs_value = search_lhs_value_
            except:
                try:
                    data_filter = data_filter.query('lhs_value {}'.format(search_lhs_value))
                except:
                    pass
        else:
            # If the search value is an empty string, clear the search filter
            data_filter = data_filter
            search_lhs_value = ""

    if search_rhs_value_ is not None or search_rhs_value != "":
        if search_rhs_value_ != "":
            try:
                data_filter = data_filter.query('rhs_value {}'.format(search_rhs_value_))
                search_rhs_value = search_rhs_value_
            except:
                try:
                    data_filter = data_filter.query('rhs_value {}'.format(search_rhs_value))
                except:
                    pass
        else:
            data_filter = data_filter
            search_rhs_value = ""

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
    else:
        data_filter = data_filter
            
    if rigthAttribute != "None":
        data_filter = data_filter.query('rhs_attribute == "{}"'.format(rigthAttribute))
    else:
        data_filter = data_filter

    to_be_filter = data_filter.columns[order]
    data_filter.sort_values(by=to_be_filter, axis="index", ascending=direction, inplace=True)
    # Get the number of filtered records
    total_filtered = pre_len - len(data_filter)

    # -------------------------------------- Pagination parameters and data slice -----------------------------------

    start_ = request.args.get('start', type=int)
    length_ = request.args.get('length', type=int)
    if start_ is not None:
        start = start_
    if length_ is not None:
        length = length_
    data_page = data_filter.iloc[start:start + length]

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
