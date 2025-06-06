import mysql.connector
import plotly.express as px
import pandas as pd
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
                keyword_col, year_col, pub_count_col = [], [], []
                current_keyword = ""
                current_year = -1
                for (keyword, year, pub_count) in cur:
                    year = int(year)
                    if keyword != current_keyword:
                        current_keyword = keyword
                        current_year = year
                    else:
                        while current_year < year:
                            keyword_col.append(current_keyword)
                            year_col.append(current_year)
                            pub_count_col.append(0)
                            current_year += 1
                    keyword_col.append(keyword)
                    year_col.append(year)
                    pub_count_col.append(pub_count)
                    current_year += 1
            except Exception as e:
                print(e)
    df = pd.DataFrame(data={'Keyword': keyword_col, 'Year': year_col, 'Number of Related Publications': pub_count_col})
    fig = px.line(df, x="Year", y="Number of Related Publications", color='Keyword')
    return fig
