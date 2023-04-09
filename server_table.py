from flask import Flask, render_template, request
import pandas as pd
from assosiation import df_results

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('server_table.html', title='Assosiation Table')


@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    data_filter = df_results

    # Get the search query
    search_lift = request.args.get('lift_search')
    search_confidence = request.args.get('confidence_search')
    print(search_lift)
    print(search_confidence)

    # Filter the data if a search query is provided
    if search_lift or search_confidence:
        lift_filter = data_filter['lift'].apply(str).str.lower().str.contains(
            search_lift.lower()) if search_lift else pd.Series(True, index=data_filter.index)
        confidence_filter = data_filter['confidence'].apply(str).str.lower().str.contains(
            search_confidence.lower()) if search_confidence else pd.Series(True, index=data_filter.index)
        data_filter = data_filter[lift_filter & confidence_filter]

    # Get the number of filtered records
    total_filtered = len(data_filter)

    # Get the sorting columns and sort the data
    order_cols = []
    i = 1
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        descending = request.args.get(f'order[{i}][dir]', '') == 'desc'
        order_cols.append((col_name, descending))
        i += 1

    if order_cols:
        data_filter = data_filter.sort_values(order_cols, ignore_index=True)

    # Get the pagination parameters and slice the data
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    data_page = data_filter.iloc[start:start+length]

    # Format the response
    response = {
        'data': data_page.to_dict('records'),
        'recordsFiltered': total_filtered,
        'recordsTotal': len(df_results),
        'draw': request.args.get('draw', type=int),
    }

    return response

if __name__ == '__main__':
    app.run()