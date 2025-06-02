import mysql.connector
import plotly.express as px
import config
import time

def make_consecutive_years(data):
    new_years, new_pub_counts = [], []
    y = -1
    for year, pub_count in data:
        year, pub_count = int(year), int(pub_count)
        if y == -1:
            y = year
        while year != y:
            new_years.append(y)
            new_pub_counts.append(0)
            y += 1
        new_years.append(year)
        new_pub_counts.append(pub_count)
        y += 1
    return new_years, new_pub_counts

def get_popularity_figure(seed_keyword):
    query = (
        "SELECT p.year, COUNT(*) "
        "FROM keyword k "
        "JOIN Publication_Keyword pk ON k.id = pk.keyword_id "
        "JOIN publication p ON pk.publication_id = p.ID "
        "WHERE k.name = %s "
        "GROUP BY p.year "
        "ORDER BY p.year")
    with mysql.connector.connect(
        user=config.MYSQL_USER, 
        password=config.MYSQL_PASSWORD, 
        database=config.MYSQL_DATABASE, 
        host=config.MYSQL_HOST
    ) as cnx:
        with cnx.cursor(buffered=True) as cur:
            try:
                cur.execute(query, [seed_keyword])
                years, pub_counts = make_consecutive_years(cur)
            except Exception as e:
                print(e)
    fig = px.line(x=years, y=pub_counts)
    fig.update_layout(xaxis_title='Year', yaxis_title='Number of Related Publications')
    return fig

def get_trending_figure():
    query = ('''
        SELECT * 
        FROM trending_keywords
        WHERE year >= 1990;
    ''')
    with mysql.connector.connect(
        user=config.MYSQL_USER, 
        password=config.MYSQL_PASSWORD, 
        database=config.MYSQL_DATABASE, 
        host=config.MYSQL_HOST
    ) as cnx:
        with cnx.cursor(buffered=True) as cur:
            try:
                cur.execute(query)
                keyword_to_data = {}
                for (keyword, year, pub_count) in cur:
                    if keyword in keyword_to_data:
                        keyword_to_data[keyword]['years'].append(year)
                        keyword_to_data[keyword]['pub_counts'].append(pub_count)
                    else:
                        keyword_to_data[keyword] = {'years': [year], 'pub_counts': [pub_count]}
                for keyword in keyword_to_data.keys():
                     keyword_to_data[keyword]['years'], keyword_to_data[keyword]['pub_counts'] = \
                        make_consecutive_years(zip(keyword_to_data[keyword]['years'], keyword_to_data[keyword]['pub_counts']))
            except Exception as e:
                print(e)
    fig = {
        'data': [
            {
                'x': keyword_to_data[keyword]['years'],
                'y': keyword_to_data[keyword]['pub_counts'],
                'type': 'line',
                'name': keyword
            }
        for keyword in keyword_to_data.keys()],
        'layout': {
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Number of Related Publications'},
        }
    }
    return fig
